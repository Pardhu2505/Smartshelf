from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://vtu29179_db_user:<db_password>@cluster0.ji0t12u.mongodb.net/?appName=Cluster0")

# Database
db = client["smartshelf"]

# Collection
products = db["products"]

# Home Page
@app.route('/')
def home():

    data = list(products.find())

    for p in data:

        if p["stock"] <= p["threshold"]:
            p["alert"] = "⚠️ Low Stock"
        else:
            p["alert"] = "✅ Available"

    return render_template("index.html", data=data)

# Add Product
@app.route('/add', methods=['POST'])
def add():

    product = {
        "name": request.form['name'],
        "category": request.form['category'],
        "stock": int(request.form['stock']),
        "threshold": int(request.form['threshold']),
        "daily_usage": int(request.form['daily_usage'])
    }

    products.insert_one(product)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
