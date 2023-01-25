import streamlit as st
from PIL import Image
import os.path
import random
import time
import warnings
import glob
warnings.filterwarnings('ignore')

foods = ['Chicken', 'Pizza', 'Jajangmyeon', 'Champon', 'Tteokbokki', 'hamburger', 'Sweet and sour pork', 
'fried rice', 'kimbap', 'pork cutlet', 'Udon', 'Bul Gogi', 'Maratang', 'Water cold noodle', 'Bossam', 'beef', 
'Steamed chicken', 'Gamjatang', 'pasta', 'sushi', 'Mara Xiang Guo', 'rice noodles', 'Abalone porridge', 
'sashimi platter', 'Pork feet', 'kebab', 'Grilled Fish', 'Curry', 'lamb skewers', 'ramen']

def food_to_img()->dict:
    paths = glob.glob('./data/food_img/*')

    if "\\" in paths[0]:
        food2img = { i.split('.')[-2].split('\\')[-1] : i for i in paths}
    else:
        food2img = { i.split('.')[-2].split('/')[-1] : i for i in paths}

    return food2img

    # try:
    #     food2img = { i.split('.')[-2].split('\\')[-1] : i for i in paths}
    # except:
    #     food2img = { i.split('.')[-2].split('/')[-1] : i for i in paths}

    # return food2img

food2img = food_to_img()

def recommendation(items):
    # important
    if len(items) == 4:
        rec_list = []
        seed = []
        for food in foods:
            if food not in items:
                rec_list.append(food)

        for i in items:
            seed.append(str(foods.index(i) + 1))

        seed = int(''.join(seed))
        random.seed(seed)
        rec_predict = random.sample(rec_list, 5)
        time.sleep(2)
        return rec_predict

def app():
    st.markdown("""
    <style>
    .small-font {
        font-size:20px !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: black;'>Food Recommendation System</h1>", unsafe_allow_html=True)
    # st.subheader("When restarting, be sure to press F5.")
    st.markdown('<h2 class="small-font">"When restarting, be sure to press F5."</h2>', unsafe_allow_html=True)
    items = st.multiselect(
        'What are your favorite foods',
        foods, max_selections=4)


    if st.button('Show Recommendation'):
        try:
            rec_predict = recommendation(items)
            # st.write('추천 시작:', rec_predict)
            st.session_state['rec_predict'] = rec_predict


            col1, col2, col3, col4, col5 = st.columns(5)

            st.markdown("""
            <style>
            .small-font {
                font-size:24px !important;
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)

            with col1:
                image = Image.open(food2img[rec_predict[0]])
                st.image(image)
                st.markdown('<p class="small-font">' + rec_predict[0] + '</p>', unsafe_allow_html=True)

            with col2:
                image = Image.open(food2img[rec_predict[1]])
                st.image(image)
                st.markdown('<p class="small-font">' + rec_predict[1] + '</p>', unsafe_allow_html=True)

            with col3:
                image = Image.open(food2img[rec_predict[2]])
                st.image(image)
                st.markdown('<p class="small-font">' + rec_predict[2] + '</p>', unsafe_allow_html=True)

            with col4:
                image = Image.open(food2img[rec_predict[3]])
                st.image(image)
                st.markdown('<p class="small-font">' + rec_predict[3] + '</p>', unsafe_allow_html=True)

            with col5:
                image = Image.open(food2img[rec_predict[4]])
                st.image(image)
                st.markdown('<p class="small-font">' + rec_predict[4] + '</p>', unsafe_allow_html=True)

            st.balloons()

        except TypeError:
            st.info("Please select four items.")


# 이미지 출력 
# from PIL import Image
# image = Image.open('img.jpg')

# st.image(image)