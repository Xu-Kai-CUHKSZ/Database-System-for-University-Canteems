import streamlit as st
import pymysql
import pandas as pd
from canteen_menu import canteen_menu

st.set_page_config(
    page_title='Canteens',
    page_icon='🍚',
    layout='wide',
    initial_sidebar_state='expanded'
)

canteen_menu()

st.title("Overview of Canteen Information")

# connect database
db = pymysql.connect(host='localhost', user='root', password='allen@JL', db='cuhk_sz', charset='utf8')
cursor = db.cursor()

# print CANTEEN infomation
selCanteen = 'select * from CANTEEN'
cursor.execute(selCanteen)
column=[col[0] for col in cursor.description]
data = cursor.fetchall()
data_df=pd.DataFrame(list(data), columns=column)
st.write(data_df)