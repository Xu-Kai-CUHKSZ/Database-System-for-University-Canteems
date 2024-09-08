import streamlit as st
from menu import menu
import pymysql
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from background import set_background

menu()

db_config = pymysql.connect(
        host='localhost',
        user='root',
        password='allen@JL',
        database='cuhk_sz',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def search(table, key, id):
    
    with db_config.cursor() as cursor:
        sql= f"SELECT * FROM {table} WHERE {key} = '{id}';"
        #st.write(sql)
        cursor.execute(sql)
        pure_result=cursor
        result = cursor.fetchone()
        frame_result=pd.DataFrame([result])
        html=frame_result.to_html(index=False)
        with st.container():
            if result:
                st.dataframe(frame_result, use_container_width=True)
            else:
                st.write("Cannot Find any result match")    
           
#set_background(r'C:\Users\林钰周\Pictures\Saved Pictures\canteen4.png', 0.35)

with st.container():
    st.title("Search the Food Right Now! ") 
    option = None            
    option = st.selectbox(
            "Select the type of information you are looking for?",
            ("Food", "Stand", "Canteen"),
            index=None,
            placeholder="Select contact method...",
            )
    
if option:
    with st.form("sub_option", border=False):

        place = st.empty()
        if option=='Food' or option=='Stand':
            id=place.text_input('Please enter the ID you want to search')
        
        if option=='Canteen':
            id=place.selectbox(
                "Select which canteen you are looking for?",
                ("Canteen 5", "学生活动中心二楼食堂", "快乐食间", 
                "海月廷", "逸夫食堂"),
                index=None,
                placeholder="Select contact method...",
                )

        submitted = st.form_submit_button("Search")
        
        if submitted:
            #st.write("looking for ", option, " with parameter ", id)
            
            if option=="Food":
                table='dish'
                key='dish_id'
            elif option=='Canteen':
                table='canteen'
                key='canteen_name'
            elif option=='Stand':
                table='stand'
                key='stand_id'
            search(table, key, id)
        

