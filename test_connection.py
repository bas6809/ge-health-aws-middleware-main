import pymysql
import config

try:
    conn = pymysql.connect(
        host="server-3.c4qyicfkvft8.us-east-1.rds.amazonaws.com",
        user=config.root_USER,
        password=config.root_PASS,
        database=config.root_NAME,
        port=3306
    )
    print("Connected successfully!")
    conn.close()

except Exception as e:
    print("Connection failed:", e)