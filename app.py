from flask import Flask, render_template
import mysql.connector
from flask import jsonify

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kaizo12334",
    database="anistock"
)

cursor = db.cursor(dictionary=True)

@app.route("/shop")
def shop():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template("shop.html", products=products)

@app.route("/api/products")
def get_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)