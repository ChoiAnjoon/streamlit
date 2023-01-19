import streamlit as st
import os.path
import random
import time
import glob 
from PIL import Image
import warnings
warnings.filterwarnings('ignore')


def food_to_img()->dict:
    paths = glob.glob('./data/food_img/*')

    try:
        food2img = { i.split('.')[-2].split('\\')[-1] : i for i in paths}
    except:
        food2img = { i.split('.')[-2].split('/')[-1] : i for i in paths}

    return food2img

food2img = food_to_img()



def app():
    st.markdown("""
    <style>
    .small-font {
        font-size:20px !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: black;'>Apply membership discount service</h1>", unsafe_allow_html=True)
    st.markdown('<h2 class="small-font">"5% discount when applying membership"</h2>', unsafe_allow_html=True)
    # st.header('멤버십 할인 서비스 적용')
    # st.subheader('멤버십 적용시 5% 할인')

    try:
        st.session_state['first']
        col1, col2, col3 = st.columns(3)

        st.markdown("""
        <style>
        .small-font {
            font-size:24px !important;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

        with col1:
            # st.header("University student")
            st.image("https://static.streamlit.io/examples/cat.jpg")
            st.markdown('<p class="small-font">"University student"</p>', unsafe_allow_html=True)

        with col2:
            # st.header("soldier")
            st.image("https://static.streamlit.io/examples/dog.jpg")
            st.markdown('<p class="small-font">"soldier"</p>', unsafe_allow_html=True)

        with col3:
            # st.header("vulnerable social groups")
            st.image("https://static.streamlit.io/examples/cat.jpg")
            st.markdown('<p class="small-font">"vulnerable social groups"</p>', unsafe_allow_html=True)

        
        col1, col2, col3 = st.columns(3)

        with col1:
            student = st.checkbox("University student")

            if student:
                con = st.container()
                con.caption("Membership Benefits")
                st.success("10% student discount")

        with col2:
            soldiar = st.checkbox("soldier")

            if soldiar:
                con = st.container()
                con.caption("Membership Benefits")
                st.success("10% military discount")

        with col3:
            location = st.checkbox("vulnerable social groups")

            if location:
                con = st.container()
                con.caption("Membership Benefits")
                st.success("10% base discount")

        
        col1, col2, col3 = st.columns(3)

        with col1:
            pass

        with col2:
            sol = st.checkbox("No applicable membership")

            if sol:
                con = st.container()
                con.caption("Membership benefits not applied")
                st.success("Membership application X")    

        with col3:
            pass



        


    except KeyError:
            st.error("Please select food on the bundling page.")
