from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Skylord@1123",
    database="blood_donor_db"
)

cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print("Received data:", data)   # DEBUG LINE

    if not data:
        return jsonify({"message": "No data received"}), 400

    query = """
    INSERT INTO donor (name, blood_group, age, phone, city)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data.get("name"),
        data.get("blood_group"),
        data.get("age"),
        data.get("phone"),
        data.get("city")
    )

    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Donor Registered Successfully"})


@app.route("/search", methods=["POST"])
def search():
    data = request.json
    cursor.execute(
        "SELECT name, blood_group, age, phone, city FROM donor WHERE blood_group=%s AND city=%s",
        (data["blood_group"], data["city"])
    )
    return jsonify(cursor.fetchall())

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


