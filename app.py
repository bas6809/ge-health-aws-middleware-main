from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
import config

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return pymysql.connect(
        host=config.root_host,
        user=config.root_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM equipment")  # change to your table
        rows = cursor.fetchall()

        conn.close()

        return jsonify({
            "status": "success",
            "total_records": len(rows),
            "equipment": rows
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)