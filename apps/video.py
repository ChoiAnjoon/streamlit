import streamlit as st
import os.path
import random
import time
import glob 
from PIL import Image
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
    except KeyError:
            st.error("Please select food on the bundling page.")