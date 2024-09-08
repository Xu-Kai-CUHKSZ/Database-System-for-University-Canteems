import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
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
    username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username()
    if username_of_forgotten_username:
        st.success('Username to be sent securely')
        # The developer should securely transfer the username to the user.
    elif username_of_forgotten_username == False:
        st.error('Email not found')
except Exception as e:
    st.error(e)
    
## update config files
with open('D:/Study/CSC3170/project/user/user.config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)