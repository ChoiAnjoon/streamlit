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

buddling = {
'Chicken': ['Cola', 'Cajun potatoes', 'draft beer'],
'Pizza': ['pasta', 'Cola', 'Chicken tender'],
'Jajangmyeon': ['Sweet and sour pork', 'dumpling', 'Cola'],
'Champon': ['Sweet and sour pork', 'fried rice', 'Cola'],
'Tteokbokki': ['Assorted Tempura', 'kimbap', 'fish cake'],
'hamburger': ['Cajun potatoes', 'Chicken tender', 'Cola'],
'Sweet and sour pork': ['Jajangmyeon', 'Champon', 'dumpling'],
'fried rice': ['Sweet and sour pork', 'Champon broth', 'Cola'],
'kimbap': ['Tteokbokki', 'ramen', 'fish cake'],
'pork cutlet': ['Udon', 'salad', 'Cola'],
'Udon': ['pork cutlet', 'Assorted Tempura', 'fish cake'],
'Bul Gogi': ['egg roll', 'draft beer', 'Water cold noodle'],
'Maratang': ['Sweet and sour pork', 'fried rice', 'Cola'],
'Water cold noodle': ['beef', 'Bul Gogi', 'Bossam'],
'Bossam': ['Water cold noodle', 'Makguksu', 'Cola'],
'beef': ['Water cold noodle', 'wine', 'egg roll'],
'Steamed chicken': ['kimbap', 'salad', 'Cola'],
'Gamjatang': ['soju', 'egg roll', 'Bul Gogi'],
'pasta': ['Cola', 'salad', 'Chicken tender'],
'sushi': ['Udon', 'pork cutlet', 'Cola'],
'Mara Xiang Guo': ['wine', 'draft beer', 'Kwubaro'],
'rice noodles': ['dumpling', 'Cola', 'egg roll'],
'Abalone porridge': ['sushi', 'Cola', 'Group'],
'sashimi platter': ['soju', 'Maeuntang', 'draft beer'],
'Pork feet': ['Cola', 'soju', 'Makguksu'],
'kebab': ['Cola', 'hamburger', 'soup'],
'Grilled Fish': ['draft beer', 'soju', 'Bul Gogi'],
'Curry': ['soup', 'pork cutlet', 'Cola'],
'lamb skewers': ['draft beer', 'Kwubaro', 'Champon'],
'ramen': ['kimbap', 'dumpling', 'hamburger']
}

def food_to_img()->dict:
    paths = glob.glob('./data/food_img/*')

    try:
        food2img = { i.split('.')[-2].split('\\')[-1] : i for i in paths}
    except:
        food2img = { i.split('.')[-2].split('/')[-1] : i for i in paths}

    return food2img

food2img = food_to_img()

def recommendation(items):
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
    st.header('Food Recommendation System')
    st.subheader("재시작시, 꼭 F5룰 누르시오.")
    items = st.multiselect(
        'What are your favorite foods',
        foods, max_selections=4)

    if st.button('Show Recommendation'):
        try:
            rec_predict = recommendation(items)
            # st.write('추천 시작:', rec_predict)
            st.session_state['rec_predict'] = rec_predict


            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.header(f"{rec_predict[0]}")
                image = Image.open(food2img[rec_predict[0]])
                st.image(image)

            with col2:
                st.header(f"{rec_predict[1]}")
                image = Image.open(food2img[rec_predict[1]])
                st.image(image)

            with col3:
                st.header(f"{rec_predict[2]}")
                image = Image.open(food2img[rec_predict[2]])
                st.image(image)

            with col4:
                st.header(f"{rec_predict[3]}")
                image = Image.open(food2img[rec_predict[3]])
                st.image(image)

            with col5:
                st.header(f"{rec_predict[4]}")
                image = Image.open(food2img[rec_predict[4]])
                st.image(image)

        except TypeError:
            st.info("4개를 채워라.")


# 이미지 출력 
# from PIL import Image
# image = Image.open('img.jpg')

# st.image(image)