import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import time
from menu import menu

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

menu()

try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
    st.write(email_of_registered_user, username_of_registered_user, name_of_registered_user)
    if email_of_registered_user:
        st.success('User registered successfully')
        with open('D:/Study/CSC3170/project/user/user.config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        
    #time.sleep(2)
    #st.switch_page("app.py")
        
except Exception as e:
    st.error(e)
    
