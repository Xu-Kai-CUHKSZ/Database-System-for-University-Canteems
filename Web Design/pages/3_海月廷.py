import streamlit as st
import pymysql
from canteen_menu import canteen_menu
# canteen name
canName = '海月廷'
st.set_page_config(page_title=canName, page_icon='🫖', layout='wide', initial_sidebar_state='expanded')
st.title(canName)
canteen_menu()

# connect database
db = pymysql.connect(host='localhost', user='root', password='allen@JL', db='cuhk_sz', charset='utf8')
cursor = db.cursor()

# get location, capacity
canInfo = 'select location, capacity from CANTEEN where canteen_name="{}"'.format(canName)
cursor.execute(canInfo)
row = cursor.fetchone()
location, capacity = row[0], row[1]
st.write('*🧭Location: {}*'.format(location))
st.write('*👣Capacity: {}*'.format(capacity))

# get STAND infomation
standInfo = 'select stand_id, stand_name from STAND where canteen_name="{}"'.format(canName)
standNum = cursor.execute(standInfo)
standData = cursor.fetchall()
# convert to list
standId = []
standName = []
for idi, namei in standData:
    standId.append(idi)
    standName.append('**'+namei+'**')


# function to get dish infomation
def get_dish_info(sid):
    dishinfo = 'select dish_name, price, description from DISH where stand_id={}'.format(sid)
    cursor.execute(dishinfo)
    dishdata = cursor.fetchall()
    # convert to list
    dishname = []
    dishprice = []
    dishdes = []
    for namei, pricei, desi in dishdata:
        dishname.append(namei)
        dishprice.append(pricei)
        dishdes.append(desi)
    return dishname, dishprice, dishdes


# create tabs and show DISH data
tabs = st.tabs(standName)
for i, tab in enumerate(tabs):
    with tab:
        dishName, dishPrice, dishDes = get_dish_info(standId[i])
        if not dishName:
            st.caption('*There is no dish for now.*')
        else:
            for j, dish in enumerate(dishName):
                exp = st.expander(dish)
                exp.write('💲*Price:* **:orange[{}]**'.format(dishPrice[j]))
                exp.write('✒ *Description:* :blue[{}]'.format(dishDes[j]))
db.close()