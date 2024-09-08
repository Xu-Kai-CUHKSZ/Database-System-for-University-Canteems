import base64
import streamlit as st

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file, alpha):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
    background-image: linear-gradient(rgba(255, 255, 255, {alpha}), rgba(255, 255, 255, {alpha})), url("data:image/png;base64,%s");
    background-size: cover;
    }}
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

#set_background(r'C:\Users\林钰周\Pictures\Saved Pictures\canteen2.jpg')