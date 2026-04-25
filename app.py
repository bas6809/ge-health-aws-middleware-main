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

        cursor.execute("SELECT * FROM Equipment_Repairs")
        rows = cursor.fetchall()

        conn.close()

        return jsonify({
            "status": "success",
            "total_records": len(rows),
            "equipment": rows
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/api/equipment", methods=["POST"])
def add_equipment():
    conn = None

    try:
        data = request.get_json()

        equipment_name = data.get("equipment_name")
        equipment_type = data.get("equipment_type")
        location = data.get("location")
        status = data.get("status")

        if not equipment_name or not equipment_type or not location or not status:
            return jsonify({
                "status": "error",
                "message": "Missing required fields"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO equipment 
            (equipment_name, equipment_type, location, status)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            equipment_name,
            equipment_type,
            location,
            status
        )

        cursor.execute(sql, values)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": "Equipment record added successfully",
            "new_record_id": cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('/etc/ssl/geCA/cert.pem','/etc/ssl/geCA/key.pem') debug=True) #Make sure you refer to SSL Setup File before setting
