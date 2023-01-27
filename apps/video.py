import streamlit as st
import os.path
import random
import time
import glob 
from PIL import Image
import webbrowser
import warnings
warnings.filterwarnings('ignore')

def app():
    st.markdown("""
    <style>
    .small-font {
        font-size:20px !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: black;'>More GCI</h1>", unsafe_allow_html=True)
    # st.markdown('<h2 class="small-font">"5% discount when applying membership"</h2>', unsafe_allow_html=True)
    # st.header('멤버십 할인 서비스 적용')
    # st.subheader('멤버십 적용시 5% 할인')

    try:
        video_file = open('./data/transformrec.mp4', 'rb')
        video_bytes = video_file.read()

        st.video(video_bytes)

        link = 'https://harex4029-my.sharepoint.com/:p:/g/personal/harex_harex4029_onmicrosoft_com/EcSbvLX-jV5BgSpGUK4jCc8BnONe74nI0Kvm18sWa7AY1g?e=eMIxcU%5C'
        st.markdown(link, unsafe_allow_html=True)
        # webbrowser.open_new_tab(link)

    except KeyError:
            st.error("Please select food on the bundling page.")