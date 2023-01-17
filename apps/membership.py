import streamlit as st
import os.path
import random
import time
import warnings
warnings.filterwarnings('ignore')


def app():
    st.header('멤버십 할인 서비스 적용')
    st.subheader('멤버십 적용시 5% 할인')

    try:
        st.session_state['first']
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("대학생")
            st.image("https://static.streamlit.io/examples/cat.jpg")

        with col2:
            st.header("군인")
            st.image("https://static.streamlit.io/examples/dog.jpg")

        with col3:
            st.header("근거지 인증")
            st.image("https://static.streamlit.io/examples/cat.jpg")

        
        col1, col2, col3 = st.columns(3)

        with col1:
            con = st.container()
            con.caption("Bundling Result")
            student = st.checkbox("대학생")

            if student:
                st.write("학생 할인 10%")

        with col2:
            con = st.container()
            con.caption("Bundling Result")
            soldiar = st.checkbox("군인")

            if soldiar:
                st.write("군인 할인 10%")

        with col3:
            con = st.container()
            con.caption("Bundling Result")
            location = st.checkbox("근거지 거주")

            if location:
                st.write("근거지 할인 10%")

        
        col1, col2, col3 = st.columns(3)

        with col1:
            pass

        with col2:
            con = st.container()
            con.caption("Bundling Result")
            sol = st.checkbox("해당되는 멤버십 없음")

            if sol:
                st.write("멤버십 적옹 X")          

        with col3:
            pass



        


    except KeyError:
            st.error("Enter your data before computing. Go to the Input Page")
