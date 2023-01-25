import streamlit as st
from multiapp import MultiApp
import random
import time
import warnings
warnings.filterwarnings('ignore') 
from apps import bundling, recommend, cross, membership, video # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Food Recommend", recommend.app)
app.add_app("Food Bundling", bundling.app)
app.add_app("Membership Discount", membership.app)
app.add_app("Food Cross Selling", cross.app)
app.add_app("More GCI", video.app)

# The main app
app.run()



# 이미지 출력 
# from PIL import Image
# image = Image.open('img.jpg')

# st.image(image)