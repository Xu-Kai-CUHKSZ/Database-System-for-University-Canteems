import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import time
from background import set_background

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

def canteen_menu():
    authenticator.login()
    authenticator.logout(location="sidebar")
    if not st.session_state["authentication_status"]:
        st.switch_page("app.py")
    
    #set_background(r'C:\Users\林钰周\Pictures\Saved Pictures\kitchen.jpg', 0.35)
        
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/canteen_info.py", label="🍗 Canteens")
    st.sidebar.page_link("pages/1_学生活动中心二楼食堂.py", label="学生活动中心二楼食堂")
    st.sidebar.page_link("pages/2_快乐食间.py", label="快乐食间")
    st.sidebar.page_link("pages/3_海月廷.py", label="海月廷")
    st.sidebar.page_link("pages/4_赛百味餐厅.py", label="赛百味餐厅")
    st.sidebar.page_link("pages/5_逸夫食堂.py", label="逸夫食堂")