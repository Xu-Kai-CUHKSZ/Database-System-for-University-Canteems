import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from user_menu import user_menu
#import authentication_scratch as authentication_scratch  

##scrtch the information

#authenticator, config = authentication_scratch.authenticator_state()
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

try:
    if authenticator.reset_password(st.session_state["username"]):
        st.success('Password modified successfully')
except Exception as e:
    st.error(e)

with open('D:/Study/CSC3170/project/user/user.config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
#authentication_scratch.authenticator_state_update(config)
## update config files
