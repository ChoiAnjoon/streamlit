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
    st.subheader('꼭! F5 쳐누르고 다시처음부터 하세요')
    try:
        st.write('Choose please')
        st.session_state['rec_predict']

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.header(f"{st.session_state['rec_predict'][0]}")
            image = Image.open(food2img[st.session_state['rec_predict'][0]])
            st.image(image)

        with col2:
            st.header(f"{st.session_state['rec_predict'][1]}")
            image = Image.open(food2img[st.session_state['rec_predict'][1]])
            st.image(image)

        with col3:
            st.header(f"{st.session_state['rec_predict'][2]}")
            image = Image.open(food2img[st.session_state['rec_predict'][2]])
            st.image(image)

        with col4:
            st.header(f"{st.session_state['rec_predict'][3]}")
            image = Image.open(food2img[st.session_state['rec_predict'][3]])
            st.image(image)

        with col5:
            st.header(f"{st.session_state['rec_predict'][4]}")
            image = Image.open(food2img[st.session_state['rec_predict'][4]])
            st.image(image)

        col1, col2, col3, col4, col5 = st.columns(5)


        with col1:
            # a1 = [st.checkbox(i) for i in buddling.get(f"{st.session_state['rec_predict'][0]}")])

            # button_a = st.button('Click here', key='but_a')
            # st.write("State of button:", button_a)

            # if button_a:
            #     con = st.container()
            #     con.caption("Bundling Result:")
            #     stocks = ["ST", "STR", "STREAM", "STREAMLIT"]
            #     check_boxes = [st.checkbox(stock, key=stock) for stock in stocks]

            # ---------------------------------------------------------------------------------------------
            # button_a = st.radio("State of button1:", ['I Want Bundling', "I don't want Bundling"])
            # if button_a == 'I Want Bundling':
            #     con = st.container()
            #     con.caption("Bundling Result")
            #     [st.checkbox(stock1) for stock1 in buddling.get(f"{st.session_state['rec_predict'][0]}")]

            # if button_a == "I don't want Bundling":
            #     st.write("Okay.")

            # ---------------------------------------------------------------------------------------------

            # def show_checkboxes(containers, q_no):
            #     containers[0].checkbox("Answer 1", value=False, key=f"q{q_no}_1")
            #     containers[1].checkbox("Answer 2", value=False, key=f"q{q_no}_2")
            #     containers[2].checkbox("Answer 3", value=False, key=f"q{q_no}_3")
            #     containers[3].checkbox("Answer 4", value=False, key=f"q{q_no}_4")
            #     containers[4].checkbox("Answer 5", value=False, key=f"q{q_no}_5")


            # question_number = 1
            # containers = [st.empty(), st.empty(), st.empty(), st.empty(), st.empty()]

            # show_checkboxes(containers, question_number = 1)

            # if st.button("Submit"):
            #     question_number += 1
            #     show_checkboxes(containers, question_number)
        
        # ---------------------------------------------------------------------------------------------
            if "button_clicked1" not in st.session_state:
                st.session_state.button_clicked1 = False

            def callback1():
                #Button was clicked!
                st.session_state.button_clicked1 = True

            if (
                st.button("Bundling_1", on_click=callback1)
                or st.session_state.button_clicked1
            ):
                
                con = st.container()
                con.caption("Bundling Result")
                # [st.checkbox(stock1, key=f"food_{index}") for index, stock1 in enumerate(buddling.get(f"{st.session_state['rec_predict'][0]}"))]

                z1 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][0]}")[0], key="s1")
                z2 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][0]}")[1], key="s2")
                z3 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][0]}")[2], key="s3")

                st.session_state['first'] = []

                if z1:
                    # st.write(buddling.get(st.session_state['rec_predict'][0])[0])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][0])[0])

                if z2:
                    # st.write(buddling.get(st.session_state['rec_predict'][0])[1])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][0])[1])

                if z3:
                    # st.write(buddling.get(st.session_state['rec_predict'][0])[2])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][0])[2])

                
                # st.write(st.session_state['first'])
                st.session_state['picked_food'] = st.session_state['rec_predict'][0]
            
                
    
        with col2: 

            if "button_clicked2" not in st.session_state:
                st.session_state.button_clicked2 = False

            def callback2():
                #Button was clicked!
                st.session_state.button_clicked2 = True

            if (
                st.button("Bundling_2", on_click=callback2)
                or st.session_state.button_clicked2
            ):
                
                con = st.container()
                con.caption("Bundling Result")
                # [st.checkbox(stock1, key=f"food_{index}") for index, stock1 in enumerate(buddling.get(f"{st.session_state['rec_predict'][0]}"))]

                z4 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][1]}")[0], key="s4")
                z5 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][1]}")[1], key="s5")
                z6 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][1]}")[2], key="s6")

                st.session_state['first'] = []

                if z4:
                    # st.write(buddling.get(st.session_state['rec_predict'][1])[0])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][1])[0])

                if z5:
                    # st.write(buddling.get(st.session_state['rec_predict'][1])[1])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][1])[1])

                if z6:
                    # st.write(buddling.get(st.session_state['rec_predict'][1])[2])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][1])[2])

                
                # st.write(st.session_state['first'])
                st.session_state['picked_food'] = st.session_state['rec_predict'][1]

        with col3:

            if "button_clicked3" not in st.session_state:
                st.session_state.button_clicked3 = False

            def callback3():
                #Button was clicked!
                st.session_state.button_clicked3 = True

            if (
                st.button("Bundling_3", on_click=callback3)
                or st.session_state.button_clicked3
            ):
                
                con = st.container()
                con.caption("Bundling Result")
                # [st.checkbox(stock1, key=f"food_{index}") for index, stock1 in enumerate(buddling.get(f"{st.session_state['rec_predict'][0]}"))]

                z7 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][2]}")[0], key="s7")
                z8 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][2]}")[1], key="s8")
                z9 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][2]}")[2], key="s9")

                st.session_state['first'] = []

                if z7:
                    # st.write(buddling.get(st.session_state['rec_predict'][2])[0])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][2])[0])

                if z8:
                    # st.write(buddling.get(st.session_state['rec_predict'][2])[1])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][2])[1])

                if z9:
                    # st.write(buddling.get(st.session_state['rec_predict'][2])[2])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][2])[2])

                
                # st.write(st.session_state['first'])
                st.session_state['picked_food'] = st.session_state['rec_predict'][2]

        with col4:

            if "button_clicked4" not in st.session_state:
                st.session_state.button_clicked4 = False

            def callback4():
                #Button was clicked!
                st.session_state.button_clicked4 = True

            if (
                st.button("Bundling_4", on_click=callback4)
                or st.session_state.button_clicked4
            ):
                
                con = st.container()
                con.caption("Bundling Result")
                # [st.checkbox(stock1, key=f"food_{index}") for index, stock1 in enumerate(buddling.get(f"{st.session_state['rec_predict'][0]}"))]

                z10 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][3]}")[0], key="s10")
                z11 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][3]}")[1], key="s11")
                z12 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][3]}")[2], key="s12")

                st.session_state['first'] = []

                if z10:
                    # st.write(buddling.get(st.session_state['rec_predict'][3])[0])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][3])[0])

                if z11:
                    # st.write(buddling.get(st.session_state['rec_predict'][3])[1])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][3])[1])

                if z12:
                    # st.write(buddling.get(st.session_state['rec_predict'][3])[2])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][3])[2])

                
                # st.write(st.session_state['first'])
                st.session_state['picked_food'] = st.session_state['rec_predict'][3]

        with col5:

            if "button_clicked5" not in st.session_state:
                st.session_state.button_clicked5 = False

            def callback5():
                #Button was clicked!
                st.session_state.button_clicked5 = True

            if (
                st.button("Bundling_5", on_click=callback5)
                or st.session_state.button_clicked5
            ):
                
                con = st.container()
                con.caption("Bundling Result")
                # [st.checkbox(stock1, key=f"food_{index}") for index, stock1 in enumerate(buddling.get(f"{st.session_state['rec_predict'][0]}"))]

                z13 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][4]}")[0], key="s13")
                z14 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][4]}")[1], key="s14")
                z15 = st.checkbox(buddling.get(f"{st.session_state['rec_predict'][4]}")[2], key="s15")

                st.session_state['first'] = []

                if z13:
                    # st.write(buddling.get(st.session_state['rec_predict'][4])[0])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][4])[0])

                if z14:
                    # st.write(buddling.get(st.session_state['rec_predict'][4])[1])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][4])[1])

                if z15:
                    # st.write(buddling.get(st.session_state['rec_predict'][4])[2])
                    st.session_state['first'].append(buddling.get(st.session_state['rec_predict'][4])[2])

                
                # st.write(st.session_state['first'])
                st.session_state['picked_food'] = st.session_state['rec_predict'][4]

            # if a1:
            #     st.write("Select!")
            # st.image("https://static.streamlit.io/examples/cat.jpg")



    except KeyError:
            st.error("Enter your data before computing. Go to the Input Page")