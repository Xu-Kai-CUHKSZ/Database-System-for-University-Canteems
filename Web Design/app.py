import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import time
from menu import menu
import pymysql
import pandas as pd
from background import set_background

st.set_page_config(
    page_title='Canteens',
    page_icon='🍚',
    layout='wide',
    initial_sidebar_state='expanded'
)

##scrtch the information
with open('D:/Study/CSC3170/project/user/user.config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)


#set_background(r'C:\Users\林钰周\Pictures\Saved Pictures\canteen2.jpg', 0.35)

st.title(':rainbow[Welcome to the CUHK(SZ) Food Rating System]')



authenticator.login()
with open('D:/Study/CSC3170/project/user.config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

##authentication
if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

else:
    st.markdown('''

    Welcome to our culinary paradise! Here, you can embark on a journey of gastronomic exploration, delving into a world of diverse flavors and tantalizing dishes. Our system isn't just a repository of recipes; it's a comprehensive culinary guide designed to ignite your imagination and spark your creativity.

    ## Discover Gastronomic Delights

    Whether you're a food enthusiast, a cooking aficionado, or a health-conscious eater, our system has something for you. With our powerful search feature, you can effortlessly discover a myriad of culinary delights, ranging from traditional favorites to cutting-edge creations. Let your taste buds sail through this sea of culinary wonders and uncover your unique flavor profile!

    ## Dive Deep into Food Knowledge

    Beyond recipes and dish information, our system provides in-depth food ratings and reviews, helping you gain insights into the taste and quality of each dish. Whether you're seeking healthy options or indulging in decadent treats, we've curated the freshest and most authentic culinary information to ensure your table is always brimming with freshness and excitement!

    ## Ignite Your Culinary Creativity

    Ignite your culinary creativity and embark on a culinary adventure! Whether you're looking to try new cuisines or unravel the stories behind your favorite dishes, we've curated an infinite world of possibilities for you. Let's embark on this culinary journey together, explore uncharted flavors, and embark on a brand-new cooking odyssey!
    ''')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://www.cuhk.edu.cn/sites/webmaster.prod1.dpsite04.cuhk.edu.cn/files/styles/crop_freeform/public/2020-03/%E9%80%B8%E5%A4%AB%E9%A3%9F%E5%A0%82.JPG?itok=t4WiOoJ_")
    with col2:
        st.image("https://www.cuhk.edu.cn/sites/webmaster.prod1.dpsite04.cuhk.edu.cn/files/styles/crop_freeform/public/2020-03/%E6%BD%98%E5%A4%9A%E6%8B%89%E9%A3%9F%E5%A0%82%20%283%29_0.jpg?itok=bOp3CTQK")
    with col3:
        st.image("https://www.cuhk.edu.cn/sites/webmaster.prod1.dpsite04.cuhk.edu.cn/files/styles/crop_freeform/public/2020-03/FE0A0185_0.JPG?itok=cthB7bU8")


menu()





    
