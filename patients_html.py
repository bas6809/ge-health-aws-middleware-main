from flask import Flask, Response
import pymysql
import config
from html import escape

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/patients")
def patients_html():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, condition_desc FROM patients")
        rows = cursor.fetchall()

        html = """
        <html>
        <head><title>GE Health Patients</title></head>
        <body>
        <h1>Patients List</h1>
        <table border="1" cellpadding="5">
            <tr><th>ID</th><th>Name</th><th>Condition</th></tr>
        """

        for row in rows:
            html += f"<tr><td>{escape(str(row['id']))}</td><td>{escape(row['name'])}</td><td>{escape(row['condition_desc'])}</td></tr>"

        html += "</table></body></html>"
        return Response(html, mimetype="text/html")

    except Exception as e:
        return Response(f"<html><body><h1>Error</h1><p>Database error: {escape(str(e))}</p></body></html>", mimetype="text/html", status=500)

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('/etc/ssl/geCA/cert.pem','/etc/ssl/geCA/key.pem') debug=True)
