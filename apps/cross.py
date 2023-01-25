import streamlit as st
import os.path
import random
import time
import warnings
import glob 
from PIL import Image
warnings.filterwarnings('ignore')

dessert = ['Americano', 'sandwich', 'waffle', 'Soboro bread', 'Cheese bread', 
'Red bean shaved ice', 'frappe', 'Vanilla latte', 'Milk Shake', 'Lemonade', 'croissant', 
'croquette', 'cookie', 'Walnut cookie']


def food_to_img()->dict:
    paths = glob.glob('../data/food_img/*')

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
    # st.header('최종 선택 품목')
    time.sleep(1)
    st.markdown("""
    <style>
    .small-font {
        font-size:24px !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: black;'>purchase is complete</h1>", unsafe_allow_html=True)
    st.balloons()

    if len(st.session_state['first']) == 0:

        col1, col2, col3 = st.columns(3)

        with col1:
            pass

        with col2:
            # st.header(f"{st.session_state['picked_food']}")
            image = Image.open(food2img[st.session_state['picked_food']])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['picked_food'] + '</p>', unsafe_allow_html=True)

        with col3:
            pass

    elif len(st.session_state['first']) == 1:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            pass

        with col2:
            # st.header(f"{st.session_state['picked_food']}")
            image = Image.open(food2img[st.session_state['picked_food']])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['picked_food'] + '</p>', unsafe_allow_html=True)

        with col3:
            # st.header(f"{st.session_state['first'][0]}")
            image = Image.open(food2img[st.session_state['first'][0]])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['first'][0] + '</p>', unsafe_allow_html=True)

        with col4:
            pass

    elif len(st.session_state['first']) == 2:

        col1, col2, col3 = st.columns(3)

        with col1:
            # st.header(f"{st.session_state['picked_food']}")
            image = Image.open(food2img[st.session_state['picked_food']])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['picked_food'] + '</p>', unsafe_allow_html=True)

        with col2:
            # st.header(f"{st.session_state['first'][0]}")
            image = Image.open(food2img[st.session_state['first'][0]])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['first'][0] + '</p>', unsafe_allow_html=True)

        with col3:
            # st.header(f"{st.session_state['first'][1]}")
            image = Image.open(food2img[st.session_state['first'][1]])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['first'][1] + '</p>', unsafe_allow_html=True)


    elif len(st.session_state['first']) == 3:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # st.header(f"{st.session_state['picked_food']}")
            image = Image.open(food2img[st.session_state['picked_food']])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['picked_food'] + '</p>', unsafe_allow_html=True)


        with col2:
            # st.header(f"{st.session_state['first'][0]}")
            image = Image.open(food2img[st.session_state['first'][0]])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['first'][0] + '</p>', unsafe_allow_html=True)


        with col3:
            # st.header(f"{st.session_state['first'][1]}")
            image = Image.open(food2img[st.session_state['first'][1]])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['first'][1] + '</p>', unsafe_allow_html=True)

        
        with col4:
            # st.header(f"{st.session_state['first'][2]}")
            image = Image.open(food2img[st.session_state['first'][2]])
            st.image(image)
            st.markdown('<p class="small-font">' + st.session_state['first'][2] + '</p>', unsafe_allow_html=True)

    

    
############################################################################
    st.subheader('================================================')
    st.markdown('<p class="small-font">"Dessert Cross Selling Recommendation"</p>', unsafe_allow_html=True)
    # st.subheader('Cross Selling items')

    if st.button("Click to Cross Selling button"):
        col1, col2, col3 = st.columns(3)

        cross_selling_items = cross_selling()

        with col1:

            # st.header(f"{cross_selling_items[0]}")
            image = Image.open(food2img[cross_selling_items[0]])
            st.image(image)
            st.markdown('<p class="small-font">' + cross_selling_items[0] + '</p>', unsafe_allow_html=True)
        
        with col2:

            # st.header(f"{cross_selling_items[1]}")
            image = Image.open(food2img[cross_selling_items[1]])
            st.image(image)
            st.markdown('<p class="small-font">' + cross_selling_items[1] + '</p>', unsafe_allow_html=True)

        with col3:

            # st.header(f"{cross_selling_items[2]}")
            image = Image.open(food2img[cross_selling_items[2]])
            st.image(image)
            st.markdown('<p class="small-font">' + cross_selling_items[2] + '</p>', unsafe_allow_html=True)

    
    st.caption('10% discount if you buy now')
