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



user_menu()
## update user details

try:
    if authenticator.update_user_details(st.session_state["username"]):
        st.success('Entries updated successfully')
except Exception as e:
    st.error(e)

## update config files
with open('D:/Study/CSC3170/project/user/user.config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)