import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import time

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


def authenticated_menu(page_name='app'):
    
    authenticator.logout(location="sidebar")
    
    if not st.session_state["authentication_status"]:
        st.switch_page("app.py")
    
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/user_info.py", label="🥷 User information")
    
    st.sidebar.page_link("pages/canteen_info.py", label="🍗 Canteens")
    st.sidebar.page_link("pages/Snapshot of Food.py", label="👀 Snapshot of Food")
    st.sidebar.page_link("pages/food_rating.py", label="✏ Rating For Food")  
    st.sidebar.page_link("pages/food_search.py", label="🔍 Search For Food")



def unauthenticated_menu():
    
    st.sidebar.page_link("app.py", label="login")
    st.sidebar.page_link("pages/registery.py", label="registery")
    st.sidebar.page_link("pages/forget_password.py", label="forget password?")
    st.sidebar.page_link("pages/forget_username.py", label="forget username?")
    with open('D:/Study/CSC3170/project/user/user.config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def menu():
    
    if st.session_state["authentication_status"]:
        authenticated_menu()
    else:
        unauthenticated_menu()
        