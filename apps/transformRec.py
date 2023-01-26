from tqdm.notebook import tqdm 
import tensorflow_datasets as tfds
import tensorflow as tf
import re
import os
import json

import numpy as np
import pandas as pd

import random
from random import sample
import warnings 

warnings.filterwarnings('ignore')


# transformRec 모델 

def scaled_dot_product_attention(query, key, value, mask):
    """Calculate the attention weights. """
    matmul_qk = tf.matmul(query, key, transpose_b=True)

    depth = tf.cast(tf.shape(key)[-1], tf.float32)
    logits = matmul_qk / tf.math.sqrt(depth)

    # padding을 위해 mask 추가
    if mask is not None:
        logits += (mask * -1e9)

    attention_weights = tf.nn.softmax(logits, axis=-1)

    output = tf.matmul(attention_weights, value)

    return output


# Multi-head attention 클래스
class MultiHeadAttention(tf.keras.layers.Layer):

    def __init__(self, d_model, num_heads, name="multi_head_attention"):
        super(MultiHeadAttention, self).__init__(name=name)
        self.num_heads = num_heads
        self.d_model = d_model

        assert d_model % self.num_heads == 0

        self.depth = d_model // self.num_heads

        self.query_dense = tf.keras.layers.Dense(units=d_model)
        self.key_dense = tf.keras.layers.Dense(units=d_model)
        self.value_dense = tf.keras.layers.Dense(units=d_model)

        self.dense = tf.keras.layers.Dense(units=d_model)

    def split_heads(self, inputs, batch_size):
        inputs = tf.reshape(inputs, shape=(batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(inputs, perm=[0, 2, 1, 3])

    def call(self, inputs):
        query, key, value, mask = inputs['query'], inputs['key'], inputs['value'], inputs['mask']
        batch_size = tf.shape(query)[0]

        query = self.query_dense(query)
        key = self.key_dense(key)
        value = self.value_dense(value)

        query = self.split_heads(query, batch_size)
        key = self.split_heads(key, batch_size)
        value = self.split_heads(value, batch_size)

        scaled_attention = scaled_dot_product_attention(query, key, value, mask)

        scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])

        # head 합치기
        concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.d_model))

        outputs = self.dense(concat_attention)

        return outputs

    
# masking 함수
def create_padding_mask(x):
    mask = tf.cast(tf.math.equal(x, 0), tf.float32)
    # (batch_size, 1, 1, sequence length)
    return mask[:, tf.newaxis, tf.newaxis, :]

def create_look_ahead_mask(x):
    seq_len = tf.shape(x)[1]
    look_ahead_mask = 1 - tf.linalg.band_part(tf.ones((seq_len, seq_len)), -1, 0)
    padding_mask = create_padding_mask(x)
    return tf.maximum(look_ahead_mask, padding_mask)


# Positional encoding 클래스
class PositionalEncoding(tf.keras.layers.Layer):

    def __init__(self, position, d_model):
        super(PositionalEncoding, self).__init__()
        self.pos_encoding = self.positional_encoding(position, d_model)

    def get_angles(self, position, i, d_model):
        angles = 1 / tf.pow(10000, (2 * (i // 2)) / tf.cast(d_model, tf.float32))
        return position * angles

    def positional_encoding(self, position, d_model):
        angle_rads = self.get_angles(
            position=tf.range(position, dtype=tf.float32)[:, tf.newaxis],
            i=tf.range(d_model, dtype=tf.float32)[tf.newaxis, :],
            d_model=d_model)
        # 짝수에 sin 적용
        sines = tf.math.sin(angle_rads[:, 0::2])
        # 홀수에 cos 적용
        cosines = tf.math.cos(angle_rads[:, 1::2])

        pos_encoding = tf.concat([sines, cosines], axis=-1)
        pos_encoding = pos_encoding[tf.newaxis, ...]
        return tf.cast(pos_encoding, tf.float32)

    def call(self, inputs):
        return inputs + self.pos_encoding[:, :tf.shape(inputs)[1], :]

    
def encoder_layer(units, d_model, num_heads, dropout, name="encoder_layer"):
    inputs = tf.keras.Input(shape=(None, d_model), name="inputs")
    padding_mask = tf.keras.Input(shape=(1, 1, None), name="padding_mask")

    attention = MultiHeadAttention(
        d_model, num_heads, name="attention")({
            'query': inputs,
            'key': inputs,
            'value': inputs,
            'mask': padding_mask
        })
    attention = tf.keras.layers.Dropout(rate=dropout)(attention)
    attention = tf.keras.layers.LayerNormalization(epsilon=1e-6)(inputs + attention)

    outputs = tf.keras.layers.Dense(units=units, activation='relu')(attention)
    outputs = tf.keras.layers.Dense(units=d_model)(outputs)
    outputs = tf.keras.layers.Dropout(rate=dropout)(outputs)
    outputs = tf.keras.layers.LayerNormalization(epsilon=1e-6)(attention + outputs)

    return tf.keras.Model(inputs=[inputs, padding_mask], outputs=outputs, name=name)
  
    
# Encoder 함수
def encoder(vocab_size, 
            num_layers,
            units,
            d_model,
            num_heads,
            dropout,
            name="encoder"):
    inputs = tf.keras.Input(shape=(None,), name="inputs")
    padding_mask = tf.keras.Input(shape=(1, 1, None), name="padding_mask")

    embeddings = tf.keras.layers.Embedding(vocab_size, d_model)(inputs)
    embeddings *= tf.math.sqrt(tf.cast(d_model, tf.float32))
    embeddings = PositionalEncoding(vocab_size, d_model)(embeddings)

    outputs = tf.keras.layers.Dropout(rate=dropout)(embeddings)

    for i in range(num_layers):
        outputs = encoder_layer(
            units=units,
            d_model=d_model,
            num_heads=num_heads,
            dropout=dropout,
            name="encoder_layer_{}".format(i),
        )([outputs, padding_mask])

    return tf.keras.Model(inputs=[inputs, padding_mask], outputs=outputs, name=name)
  
def decoder_layer(units, d_model, num_heads, dropout, name="decoder_layer"):
    inputs = tf.keras.Input(shape=(None, d_model), name="inputs")
    enc_outputs = tf.keras.Input(shape=(None, d_model), name="encoder_outputs")
    look_ahead_mask = tf.keras.Input(shape=(1, None, None), name="look_ahead_mask")
    padding_mask = tf.keras.Input(shape=(1, 1, None), name='padding_mask')

    attention1 = MultiHeadAttention(
        d_model, num_heads, name="attention_1")(inputs={
            'query': inputs,
            'key': inputs,
            'value': inputs,
            'mask': look_ahead_mask
        })
    attention1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)(attention1 + inputs)

    attention2 = MultiHeadAttention(
        d_model, num_heads, name="attention_2")(inputs={
            'query': attention1,
            'key': enc_outputs,
            'value': enc_outputs,
            'mask': padding_mask
        })
    attention2 = tf.keras.layers.Dropout(rate=dropout)(attention2)
    attention2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)(attention2 + attention1)

    outputs = tf.keras.layers.Dense(units=units, activation='relu')(attention2)
    outputs = tf.keras.layers.Dense(units=d_model)(outputs)
    outputs = tf.keras.layers.Dropout(rate=dropout)(outputs)
    outputs = tf.keras.layers.LayerNormalization(epsilon=1e-6)(outputs + attention2)

    return tf.keras.Model(
        inputs=[inputs, enc_outputs, look_ahead_mask, padding_mask],
        outputs=outputs,
        name=name)

    
# Decoder 함수
def decoder(vocab_size,
            num_layers,
            units,
            d_model,
            num_heads,
            dropout,
            name='decoder'):
    inputs = tf.keras.Input(shape=(None,), name='inputs')
    enc_outputs = tf.keras.Input(shape=(None, d_model), name='encoder_outputs')
    look_ahead_mask = tf.keras.Input(shape=(1, None, None), name='look_ahead_mask')
    padding_mask = tf.keras.Input(shape=(1, 1, None), name='padding_mask')

    embeddings = tf.keras.layers.Embedding(vocab_size, d_model)(inputs)
    embeddings *= tf.math.sqrt(tf.cast(d_model, tf.float32))
    embeddings = PositionalEncoding(vocab_size, d_model)(embeddings)

    outputs = tf.keras.layers.Dropout(rate=dropout)(embeddings)

    for i in range(num_layers):
        outputs = decoder_layer(
            units=units,
            d_model=d_model,
            num_heads=num_heads,
            dropout=dropout,
            name='decoder_layer_{}'.format(i),
        )(inputs=[outputs, enc_outputs, look_ahead_mask, padding_mask])

    return tf.keras.Model(
        inputs=[inputs, enc_outputs, look_ahead_mask, padding_mask],
        outputs=outputs,
        name=name)


# Transforemr 함수
def transformer(vocab_size,
                num_layers,
                units,
                d_model,
                num_heads,
                dropout,
                name="transformer"):
    inputs = tf.keras.Input(shape=(None,), name="inputs")
    dec_inputs = tf.keras.Input(shape=(None,), name="dec_inputs")

    enc_padding_mask = tf.keras.layers.Lambda(
        create_padding_mask, output_shape=(1, 1, None),
        name='enc_padding_mask')(inputs)
    look_ahead_mask = tf.keras.layers.Lambda(
        create_look_ahead_mask,
        output_shape=(1, None, None),
        name='look_ahead_mask')(dec_inputs)
    dec_padding_mask = tf.keras.layers.Lambda(
        create_padding_mask, output_shape=(1, 1, None),
        name='dec_padding_mask')(inputs)

    enc_outputs = encoder(
        vocab_size=vocab_size,
        num_layers=num_layers,
        units=units,
        d_model=d_model,
        num_heads=num_heads,
        dropout=dropout,
    )(inputs=[inputs, enc_padding_mask])

    dec_outputs = decoder(
        vocab_size=vocab_size,
        num_layers=num_layers,
        units=units,
        d_model=d_model,
        num_heads=num_heads,
        dropout=dropout,
    )(inputs=[dec_inputs, enc_outputs, look_ahead_mask, dec_padding_mask])

    outputs = tf.keras.layers.Dense(units=vocab_size, name="outputs")(dec_outputs)

    return tf.keras.Model(inputs=[inputs, dec_inputs], outputs=outputs, name=name)


# Evaluate 함수

def preprocess_sentence(sentence):
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = sentence.strip()
    return sentence


# 검증 관련 함수

def evaluate(sentence, tokenizer, top_n, model):
    sentence = preprocess_sentence(sentence)

    sentence = tf.expand_dims(
        START_TOKEN + tokenizer.encode(sentence) + END_TOKEN, axis=0)

    sentence = tf.keras.preprocessing.sequence.pad_sequences(
        sentence, maxlen=MAX_LENGTH, padding='post')

    first_argmax = []
    item_encoder = []
    for i in range(top_n):
        first_step = True
        output = tf.expand_dims(START_TOKEN, 0)
    
        # 디코더의 예측 시작
        for j in range(MAX_LENGTH):
            predictions = model(inputs=[sentence, output], training=False)

            predictions = predictions[:, -1:, :]
            predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)
            tmp_index = predicted_id.numpy()[0][0]
            
            if first_step:
                tmp_arr = predictions.numpy()[0][0]
                for k in first_argmax:
                    tmp_arr[k] = tmp_arr.min()
                predictions = tf.expand_dims(tmp_arr.reshape(1, -1), axis=0)
                
                predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)
                first_step = False

            if tf.equal(predicted_id, END_TOKEN[0]):
                break
            output = tf.concat([output, predicted_id], axis=-1)
            if j == 0:
                if i == 0:
                    first_argmax.append(tmp_index)
                else:
                    first_argmax.append(predicted_id.numpy()[0][0])
        item_encoder.append(tf.squeeze(output, axis=0))
        # sentence = output
    return item_encoder


def predict(sentence, model, tokenizer, top_n=10):
    prediction = evaluate(sentence, tokenizer, top_n, model)

    item_name = []
    for pred in prediction:
        item_name.append(tokenizer.decode([i for i in pred if i < tokenizer.vocab_size]))

#     print('Input: {}'.format(sentence))
#     print('Output: {}'.format(predicted_sentence))

#     return ' <sep> '.join(item_name)
    return [i.replace(' sep ', ' ').replace('sep ', '').replace(' sep', '') for i in item_name]




# 모델 load

def haha():
    model_version = 1
    data_version = 1
    column = 'tokenized_'
    ulsan_preprocessing_data_path = './data/시연용데이터.csv'

    import pprint
    names = []
    with open('model_name.txt', 'r') as f:
        for name in f:
            names.append(name)
    name = names[-1][:-1]

    with open('{}/configuration.json'.format(name), 'r') as f:
        cfg = json.load(f)

    print('*' * 30)
    print(name)
    pprint.pprint(cfg)
    print('*' * 30)

    START_TOKEN = cfg['START_TOKEN']
    END_TOKEN = cfg['END_TOKEN']
    MAX_LENGTH = cfg['MAX_LENGTH']

    ulsan_filtering_test_df = pd.read_csv('./data/test_시연용.csv')
    print('Tokenizing ...')
    print('Loading model ...')

        
    ulsan_model = transformer(
        vocab_size=cfg['VOCAB_SIZE'],
        num_layers=cfg['NUM_LAYERS'],
        units=cfg['UNITS'],
        d_model=cfg['D_MODEL'],
        num_heads=cfg['NUM_HEADS'],
        dropout=cfg['DROPOUT'])

    ulsan_model.load_weights('{}/model.h5'.format(name))
    print('Loaded model ...')


# ----------------------------------------------------------------------
# # Jaccard 유사도 함수 정의 및 item_list 불러오기
# df = pd.read_csv(ulsan_preprocessing_data_path)
# item_list = list(set(sum([i.split(' sep ') for i in df['train']], [])))
# item_list.extend(list(set(df['label'])))
# item_list = list(set(item_list))

# def jaccard_similarity(s1, s2):
#     s1 = set(s1.split()) 
#     s2 = set(s2.split())
#     return len(s1 & s2) / len(s1 | s2)


def inference(sentence, model, tokenizer):
    
    import time
    start = time.time()
#     sentence = 
    predict(sentence, model, tokenizer, 5)
#     print("WorkingTime: {} sec".format(round(time.time()-start, 3)))


    print('입력되는 이전 구매 기록: ', sentence)
    print()
    print('자카드 X 모델 추천')
    print(predict(sentence, model, tokenizer, 5))
    a = predict(sentence, model, tokenizer, 5)
    
    # ----------------------------------------------------------------------
    # # 중복 고려해서, 자카드 유사도를 통해 실제 있는 아이템으로 치환
    # tmp_list = a.copy()
    # for index, pred in enumerate(a):
    #     if pred not in item_list or a.count(pred) > 1:
    #         # 전체 상품 목록과 잘못된 상품 이름과 자카드 유사도를 구한 뒤
    #         jaccar_score = {i:jaccard_similarity(pred, i) for i in item_list if (pred != i) and (jaccard_similarity(pred, i) != 0)}
    #         # 나온 자카드 결과를 내림차순 정렬
    #         jaccar_score = sorted(jaccar_score.items(), key=lambda x: x[1], reverse=True)
    #         if len(jaccar_score) != 0:
    #             tmp_list[index] = jaccar_score[0][0]
    #             k = 0
    #             while True:
    #                 if tmp_list.count(jaccar_score[k][0]) > 1:
    #                     k += 1
    #                     tmp_list[index] = jaccar_score[k][0]

    #                 else:
    #                     break

    #         else:
    #             tmp_list[index] = ''
                
    
    # print()
    # print('자카드 O 모델 추천')
    # print(tmp_list)
    # end = time.time()
    # print()
    # print()
    # print("WorkingTime: {} sec".format(round(end - start, 3)))