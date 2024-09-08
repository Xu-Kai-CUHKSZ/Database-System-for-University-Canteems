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

def user_menu():
    authenticator.login()
    authenticator.logout(location="sidebar")
    if not st.session_state["authentication_status"]:
        st.switch_page("app.py")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/user_info.py", label="🥷 User information")
    st.sidebar.page_link("pages/reset_password.py", label="  reset password")
    st.sidebar.page_link("pages/update.py", label="  update")
