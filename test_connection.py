import pymysql
import config

try:
    conn = pymysql.connect(
        host="server-3.c4qyicfkvft8.us-east-1.rds.amazonaws.com",
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
        port=3306
    )
    print("Connected successfully!")
    conn.close()

except Exception as e:
    print("Connection failed:", e)
