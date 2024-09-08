import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from user_menu import user_menu

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


## reset password 

user_menu()

st.write(f'Name: *{st.session_state["name"]}*',size=30)
#st.write(f'Email: *{st.session_state["email"]}*', size=30)

## update config files
with open('D:/Study/CSC3170/project/user/user.config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
    