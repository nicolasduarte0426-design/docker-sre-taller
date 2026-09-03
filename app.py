from flask import Flask, jsonify
import os
import time
import pymysql

app = Flask(__name__)


def get_db_connection():
    for _ in range(30):
        try:
            return pymysql.connect(
                host=os.getenv("DB_HOST", "servidor-bd"),
                user=os.getenv("DB_USER", "adso_user"),
                password="adso_password",
                database=os.getenv("DB_NAME", "adso_db"),
                connect_timeout=5
            )
        except pymysql.MySQLError:
            time.sleep(2)

    raise Exception("No se pudo conectar a MySQL")


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "Flask API"
    })


@app.route("/health")
def health():
    connection = get_db_connection()
    connection.close()

    return jsonify({
        "status": "ok",
        "database": "connected"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)  # nosec B104
