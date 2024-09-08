import pymysql

# 数据库连接配置，请替换为您的实际数据库信息
db_config = {
    'host': 'localhost',
    'user': 'root',  # 请替换为您的用户名
    'password': 'YWYASYKl1208',  # 请替换为您的密码
    'charset': 'utf8mb4'
}

# 建立数据库连接
connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS cuhk_sz;")
    connection.commit()

    with connection.cursor() as cursor:
        # 创建CANTEEN表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuhk_sz.CANTEEN (
                canteen_name VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                capacity INT NOT NULL,
                PRIMARY KEY (canteen_name)
            );
        """)
    connection.commit()

    with connection.cursor() as cursor:
        # 创建STAND表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuhk_sz.STAND (
                stand_id INT AUTO_INCREMENT,
                canteen_name VARCHAR(255) NOT NULL,
                stand_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (stand_id),
                FOREIGN KEY (canteen_name) REFERENCES cuhk_sz.CANTEEN(canteen_name)
            );
        """)
    connection.commit()

    with connection.cursor() as cursor:
        # 创建DISH表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuhk_sz.DISH (
                dish_id INT AUTO_INCREMENT,
                stand_id INT NOT NULL,
                dish_name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT,
                PRIMARY KEY (dish_id),
                FOREIGN KEY (stand_id) REFERENCES cuhk_sz.STAND(stand_id)
            );
        """)
    connection.commit()

    with connection.cursor() as cursor:
        # 创建USER表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuhk_sz.USER (
                user_id INT NOT NULL,
                user_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (user_id)
            );
        """)
    connection.commit()

    with connection.cursor() as cursor:
        # 创建SALES表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuhk_sz.SALES (
                dish_id INT NOT NULL,
                date DATE NOT NULL,
                sales INT NOT NULL,
                PRIMARY KEY (dish_id, date),
                FOREIGN KEY (dish_id) REFERENCES cuhk_sz.DISH(dish_id)
            );
        """)
    connection.commit()

    with connection.cursor() as cursor:
        # 创建grade表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuhk_sz.grade (
                user_id INT NOT NULL,
                dish_id INT NOT NULL,
                score INT NOT NULL,
                date DATE NOT NULL,
                PRIMARY KEY (user_id, dish_id, date),
                FOREIGN KEY (user_id) REFERENCES cuhk_sz.USER(user_id),
                FOREIGN KEY (dish_id) REFERENCES cuhk_sz.DISH(dish_id)
            );
        """)
    connection.commit()

    with connection.cursor() as cursor:
        # 创建set_menu表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cuhk_sz.set_menu (
                disha_id INT NOT NULL,
                dishb_id INT,
                set_price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (disha_id) REFERENCES cuhk_sz.DISH(dish_id),
                FOREIGN KEY (dishb_id) REFERENCES cuhk_sz.DISH(dish_id)
            );
        """)
    connection.commit()
    

except Exception as e:
    print(f"An error occurred: {e}")
    connection.rollback()


finally:
    connection.close()
