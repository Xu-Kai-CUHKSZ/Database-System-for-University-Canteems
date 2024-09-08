import streamlit as st
import pymysql
import numpy as np
import matplotlib.pyplot as plt
from menu import menu 
from background import set_background

st.set_page_config(page_title='Snapshot of Food', page_icon='📊')
st.title('Snapshot of Food')
#set_background(r'C:\Users\林钰周\Pictures\Saved Pictures\canteen4.png', 0.35)
menu()

# connect database
db = pymysql.connect(host='localhost', user='root', password='allen@JL', db='cuhk_sz', charset='utf8')
cursor = db.cursor()

# get food data
# grade part
gradeInfo = 'select dish_id, score from grade'
cursor.execute(gradeInfo)
gradeData = cursor.fetchall()
gradeDict = {}
count = {}
for did, si in gradeData:
    if did not in gradeDict.keys():
        gradeDict[did] = si
        count[did] = 1
    else:
        gradeDict[did] += si
        count[did] += 1

# calculate mean and convert to list
idList = []
scoreList = []
for i in gradeDict.keys():
    gradeDict[i] = gradeDict[i] / count[i]
    idList.append(i)
    scoreList.append(gradeDict[i])

# get top5
topScores = []
topScoresId = []
for n in range(5):
    maxScore = scoreList[0]
    maxScoreId = 0
    # find max
    for sid, sco in enumerate(scoreList):
        if (maxScore < sco) and (sco not in topScores):
            maxScore = sco
            maxScoreId = sid
    topScores.append(maxScore)
    topScoresId.append(maxScoreId)


# sales part
salesInfo = 'select dish_id, sales from SALES'
cursor.execute(salesInfo)
salesData = cursor.fetchall()
salesId = []
salesList = []
for dish_id, sales in salesData:
    salesId.append(dish_id)
    salesList.append(sales)

topSales = []
topSalesId = []
for n in range(5):
    maxSale = salesList[0]
    maxSaleId = 0
    # find max
    for saleid, sale in enumerate(salesList):
        if (maxSale < sale) and (sale not in topSales):
            maxSale = sale
            maxSaleId = saleid
    topSales.append(maxSale)
    topSalesId.append(maxSaleId)

# get dish name corresponding to dish id
dishInfo = 'select dish_id, dish_name from DISH'
cursor.execute(dishInfo)
dishData = cursor.fetchall()
dishNameDict = {}
for x, y in dishData:
    dishNameDict[x] = y
topScoresName = [dishNameDict[n] for n in topScoresId]
topSalesName = [dishNameDict[m] for m in topSalesId]


# show images
plt.rcParams['font.sans-serif'] = ['SimHei'] # to support Chinese Character
fig = plt.figure(figsize=(20, 20))
gs = fig.add_gridspec(2)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

ax1.bar(np.array(topScoresName), np.array(topScores), color='blue', width=0.5)
ax1.set_title('Top 5 food with highest scores', fontsize=30)
ax1.set_xlabel('Food Name', fontsize=20)
ax1.set_ylabel('Score', fontsize=20)
ax1.tick_params(labelsize=20)

ax2.bar(np.array(topSalesName), np.array(topSales), color='green', width=0.5)
ax2.set_title('Top 5 food with highest sales', fontsize=30)
ax2.set_xlabel('Food Name', fontsize=20)
ax2.set_ylabel('Sales', fontsize=20)
ax2.tick_params(labelsize=20)

st.pyplot(fig)

