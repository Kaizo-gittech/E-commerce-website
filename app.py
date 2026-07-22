from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kaizo12334",
        database="anistock"
    )

def get_categories():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM categories")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

@app.route('/')
def home():
    categories = get_categories()
    return render_template("pages/demo.html", categories=categories)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4646, debug=True)