import pymysql
from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

start_date = datetime(2024, 4, 1)
end_date = datetime(2024, 4, 13)

# 生成一个在范围内的随机日期
#random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]


# 初始化 Faker 生成假数据
fake = Faker('zh_CN')

# 假设的数据库连接信息
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YWYASYKl1208',#替换为你自己设定的密码
    'db': 'cuhk_sz',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

alpha = 2  # 举例
beta = 5   # 举例
multiplier = 100

# 指定的菜品名称列表
dish_names = [
    "脆皮锅烧粉", "牛肉拉面", "酸汤肥牛", "清汤抄手", "奥尔良香辣鸡扒饭",
    "干拌抄手", "五香牛腩粉", "逸夫炸酱面", "金汤无骨鱼", "虾仁鲜虾小馄饨",
    "玉米猪肉水饺", "黄焖排骨", "红油鸡丝凉面", "麻辣烫", "猪脚饭",
    "红油抄手", "姜蓉白切鸡饭", "蜜汁鸡腿饭", "麻辣香锅", "番茄无骨鱼",
    "潮汕牛筋丸汤粉", "肉多多汤粉", "宜宾燃面", "牛肉炒拉面", "大盘鸡盖浇饭",
    "新疆抓饭羊肉", "黄焖鸡", "豌豆杂酱面", "白菜猪肉水饺", "鲜肉小馄饨",
    "白切鸡烧鸭饭", "滑蛋牛肉", "南昌拌粉", "牛肉炒刀削面", "担担面",
    "烧鸭饭", "烧鸭叉烧饭", "牛肉水饺", "香辣无骨鱼", "三两粉",
    "烤盘饭", "黄焖茄子", "荠菜鲜肉小馄饨", "烧鸭手撕鸡饭", "叉烧饭",
    "芹菜猪肉水饺", "重庆小面", "手撕鸡饭", "重庆酸辣粉", "土耳其烤肉拌饭"
]

# 预设的食堂信息
canteens_info = [
    ("快乐食间", "学生活动中心一楼", 200,15),
    ("海月廷", "思廷B栋一楼", 190,10),
    ("逸夫食堂", "逸夫B栋1楼", 100,5),
    ("学生活动中心二楼食堂", "学生活动中心二楼", 170,8),
    ("赛百味餐厅", "下沉广场", 160,5)
]


canteens_and_stands = {
    "快乐食间":['重庆小面', '粤式烧腊', '手工早点铺','香锅麻辣烫', '烤盘饭' , '黄焖水煮', '三两粉', '小小花果山', '兰州拉面', '精品餐',],
    "海月廷" :['宵夜淄博烧烤', '东北水饺', '粤式烧腊', '铁板炒饭', '汤粉面', '拌饭', '自选中晚餐'],
    "逸夫食堂" : ['馄饨-饺子', '小碗菜', '包点', '面条', '逸帆茶饮'],
    "学生活动中心二楼食堂" : ['南昌拌粉', '盖码饭', '土耳其烤肉', '酸汤肥牛', 'E时麦檬'],
    "赛百味餐厅" :['金枪鱼三明治', '照烧鸡三明治', '厚切牛排三明治'],

}
    


df_grades = pd.read_excel(r'C:\Users\97575\Desktop\打分数据.xlsx', engine='openpyxl')#替换为你的excel文件路径

# 连接到数据库
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("TRUNCATE TABLE cuhk_sz.grade;")
        cursor.execute("TRUNCATE TABLE cuhk_sz.DISH;")
        cursor.execute("TRUNCATE TABLE cuhk_sz.STAND;")
        cursor.execute("TRUNCATE TABLE cuhk_sz.CANTEEN;")
        cursor.execute("TRUNCATE TABLE cuhk_sz.USER;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        connection.commit()
        # 插入 CANTEEN 数据
        for canteen_name, location, capacity,stands_count in canteens_info:  
            cursor.execute("""
                INSERT INTO canteen (canteen_name, location, capacity) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE location = VALUES(location), capacity = VALUES(capacity);
            """, (canteen_name, location, capacity))
        connection.commit()
        
        # 插入 STAND 数据
        stand_ids = []

        for canteen_name, stands in canteens_and_stands.items():
            for stand_name in stands:
                cursor.execute("""
                    INSERT INTO STAND (canteen_name, stand_name)
                    VALUES (%s, %s);
                """, (canteen_name, stand_name))
        
            # 立即获取刚刚插入的STAND记录的自动生成的stand_id
                cursor.execute("SELECT LAST_INSERT_ID();")
                result = cursor.fetchone()
                if result is not None:
            # 这里确保使用字典访问方式，因为您设置了cursorclass为DictCursor
                    stand_id = result['LAST_INSERT_ID()']
                    stand_ids.append(stand_id)
                else:
                    print("stand_id not found.")

        connection.commit()
        
        # 插入 USER 数据
        user_ids = df_grades['User ID'].unique()
        
        # 插入USER数据（假设user_name暂时为空或者和user_id相同）
        for user_id in user_ids:
            try:
                cursor.execute("INSERT INTO USER (user_id, user_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE user_id = user_id;", (user_id, str(user_id)))
            except pymysql.err.IntegrityError:
                print(f"User ID {user_id} already exists.")
        
        # 提交用户数据事务
        connection.commit()

        # 插入 DISH 数据
        for i, dish_name in enumerate(dish_names, start=1):
            #dish_id = f'{i:02d}'  # 生成格式化的ID，如'01', '02', ...
            price = round(random.uniform(10, 30), 2)  # 价格设置为 10 到 30 之间
            description = f"{dish_name}"  # 菜品描述
            stand_id = random.choice(stand_ids) 
            cursor.execute(
                "INSERT INTO DISH (stand_id, dish_name, price, description) VALUES (%s, %s, %s, %s);",
                (stand_id, dish_name, price, description)
            )
        connection.commit()
        #插入grade表数据
        for index, row in df_grades.iterrows():
            random_date = random.choice(date_list)
            # 查询dish_id
            cursor.execute("SELECT dish_id FROM DISH WHERE dish_name = %s", (row['Food ID'],))
            result = cursor.fetchone()
            if result:
                dish_id = result['dish_id']
                try:
                    cursor.execute("INSERT INTO grade (user_id, dish_id, score,date) VALUES (%s, %s, %s,%s);", (row['User ID'], dish_id, row['Rating'], random_date.strftime('%Y-%m-%d')))
                    connection.commit()
                except pymysql.err.IntegrityError:
                    print(f"Could not insert grade for User ID {row['User ID']} and Dish ID {dish_id}.")
            else:
                print(f"Dish named {row['Food ID']} not found.")
        
        cursor.execute("SELECT dish_id FROM DISH")
        dish_ids = [row['dish_id'] for row in cursor.fetchall()]

        #插入sales
        for dish_id in dish_ids:
            # 生成随机日期
            random_date = random.choice(date_list)
            # 生成 beta 分布的销售数
            sales = int(random.betavariate(alpha, beta) * multiplier)
            # 插入数据
            cursor.execute("""
                INSERT INTO cuhk_sz.SALES (dish_id, date, sales)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE sales = VALUES(sales);
            """, (dish_id, random_date, sales))
            connection.commit()

    connection.commit()


    #打印不同表的内容，检查数据的准确性
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cuhk_sz.SALES;")#可替换为别的表
        rows = cursor.fetchall()
        for row in rows:
            print(row)



except Exception as e:
    print("An unexpected error occurred:")
    print(e)
    print(type(e))
    print(e.args)
    connection.rollback()

finally:
    connection.close()
