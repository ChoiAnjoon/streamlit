import streamlit as st
import os.path
import random
import time
import warnings
import glob 
from PIL import Image
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

dessert = ['Americano', 'sandwich', 'waffle', 'Soboro bread', 'Cheese bread', 
'Red bean shaved ice', 'frappe', 'Vanilla latte', 'Milk Shake', 'Lemonade', 'croissant', 
'croquette', 'cookie', 'Walnut cookie']


def food_to_img()->dict:
    paths = glob.glob('./data/food_img/*')

    try:
        food2img = { i.split('.')[-2].split('\\')[-1] : i for i in paths}
    except:
        food2img = { i.split('.')[-2].split('/')[-1] : i for i in paths}

    return food2img

food2img = food_to_img()


def cross_selling():
    cross_selling = random.sample(dessert, 3)
    return cross_selling

def app():
#############################################################################
# 분기 처리
    st.header('최종 선택 품목')

    if len(st.session_state['first']) == 0:

        col1, col2, col3 = st.columns(3)

        with col1:
            pass

        with col2:
            st.header(f"{st.session_state['picked_food']}")
            image = Image.open(food2img[st.session_state['picked_food']])
            st.image(image)

        with col3:
            pass

    elif len(st.session_state['first']) == 1:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pass

        with col2:
            st.header(f"{st.session_state['picked_food']}")
            image = Image.open(food2img[st.session_state['picked_food']])
            st.image(image)

        with col3:
            st.header(f"{st.session_state['first'][0]}")
            image = Image.open(food2img[st.session_state['first'][0]])
            st.image(image)

        with col4:
            pass

    elif len(st.session_state['first']) == 2:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header(f"{st.session_state['picked_food']}")
            image = Image.open(food2img[st.session_state['picked_food']])
            st.image(image)

        with col2:
            st.header(f"{st.session_state['first'][0]}")
            image = Image.open(food2img[st.session_state['first'][0]])
            st.image(image)

        with col3:
            st.header(f"{st.session_state['first'][1]}")
            image = Image.open(food2img[st.session_state['first'][1]])
            st.image(image)


    elif len(st.session_state['first']) == 3:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header(f"{st.session_state['picked_food']}")
            image = Image.open(food2img[st.session_state['picked_food']])
            st.image(image)


        with col2:
            st.header(f"{st.session_state['first'][0]}")
            image = Image.open(food2img[st.session_state['first'][0]])
            st.image(image)


        with col3:
            st.header(f"{st.session_state['first'][1]}")
            image = Image.open(food2img[st.session_state['first'][1]])
            st.image(image)

        
        with col4:
            st.header(f"{st.session_state['first'][2]}")
            image = Image.open(food2img[st.session_state['first'][2]])
            st.image(image)

    

    
############################################################################

    st.subheader('Cross Selling items')
    col1, col2, col3 = st.columns(3)

    cross_selling_items = cross_selling()

    with col1:

        st.header(f"{cross_selling_items[0]}")
        image = Image.open(food2img[cross_selling_items[0]])
        st.image(image)
    
    with col2:

        st.header(f"{cross_selling_items[1]}")
        image = Image.open(food2img[cross_selling_items[1]])
        st.image(image)

    with col3:

        st.header(f"{cross_selling_items[2]}")
        image = Image.open(food2img[cross_selling_items[2]])
        st.image(image)


        # st.write(st.session_state['picked_food'])
        # st.write(st.session_state['first'])

