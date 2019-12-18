# Import Dependencies, including the Python file that did all of the work
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Scrape_Mars
import os

# Set up the FLASK Application
app = Flask(__name__)

mongo = PyMongo(app)

# Calls the HTML file
@app.route("/")
def index():
    marsDB = mongo.db.mars.find_one()
    return render_template("index.html", mars=marsDB)

# Calls the scrape() function to collect the Mars data
def scrape():
    marsDB = mongo.db.mars
    mars_info = Scrape_Mars.scrape()
    marsDB.update({}, mars_info, upsert=True)
    return redirect("http://localhost:5000/", code=302)

# Run the Application
if __name__ == "__main__":
    app.run(debug=True)
