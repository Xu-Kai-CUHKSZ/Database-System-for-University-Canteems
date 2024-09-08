import streamlit as st
from menu import menu
import pymysql
import pandas as pd
from datetime import date
from background import set_background

menu()

PRE_PASSWORD='123'


db_config = pymysql.connect(
        host='localhost',
        user='root',
        password='allen@JL',
        database='cuhk_sz',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )



def detail_record(id):
    with db_config.cursor() as cursor:
        sql = f"SELECT user_id, score, date FROM grade WHERE dish_id = '{id}' ORDER BY date DESC;"
        cursor.execute(sql)
        result= cursor.fetchall()
        #st.write(result)
        if result:
            st.dataframe(pd.DataFrame(result), use_container_width=True)
    
def search_rate(id):
    
    with db_config.cursor() as cursor:
        grade_sql = f"SELECT AVG(score), COUNT(*) FROM grade WHERE dish_id = '{id}';"
        cursor.execute(grade_sql)
        grade_result= cursor.fetchone()
        dish_sql = f"SELECT dish_id, dish_name FROM dish WHERE dish_id = '{id}';"
        cursor.execute(dish_sql)
        dish_result= cursor.fetchone()
        if not grade_result or not dish_result:
            id_waring.warning("Food not found! Please check the ID.")
            return
        
        average_score = grade_result['AVG(score)']
        record_count = grade_result['COUNT(*)']
    
        
        dish_id = dish_result['dish_id']
        dish_name = dish_result['dish_name']
        
        search_rate_table = pd.DataFrame({
            "Dish ID": [dish_id],
            "Dish Name": [dish_name],
            "Average Rate": [average_score],
            "Number of Rater": [record_count]
        })
        st.dataframe(search_rate_table, use_container_width=True)
        
 
def upload_rate(user_id, dish_id, score):
    current_date = date.today()
    format_date = current_date.strftime("%Y-%m-%d")
    with db_config.cursor() as cursor:
        sql = f"INSERT INTO grade (user_id, dish_id, score, date) VALUES ('{user_id}', '{dish_id}', {score}, '{format_date}');"
        cursor.execute(sql)
        db_config.commit()
    st.success("Thank you for rating!") 
        
                           
with st.container():
    show_detail_records=False
    
    st.title("See The Rating Right Now!")
    food_id  = st.text_input('ID of the food you want to search', value=None)
    id_waring=st.empty()
    show_detail_records=st.toggle("See detail records")
    


if  food_id:
    with st.form("detailed_records", border=False):
        search_password=None
        if show_detail_records:
            search_password = st.text_input('Input the password to obtain permission to see details', value=None, type='password')

        submitted = st.form_submit_button("Search")
        
        if submitted:
            search_rate(food_id)
            if search_password==PRE_PASSWORD:
                detail_record(food_id)
            elif search_password:
                st.warning("Wrong passward")


#set_background(r'C:\Users\林钰周\Pictures\Saved Pictures\canteen4.png', 0.35)
st.title("Upload  Your Own rate!")
     
with st.form("upload_rating", border=False):
    
    user_id = st.text_input('Your ID', value=None)
    food_id = st.text_input('ID of the food you want to rate', value=None)
    food_rating=st.text_input('Rate', value=None)
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not user_id or not food_id or not food_rating:
            st.warning("Please fill the blank! ")
        #st.write("Rate for food ", food_id, " with rating ", food_rating)
        else:
            upload_rate(user_id, food_id, food_rating)