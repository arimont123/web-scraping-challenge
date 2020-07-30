from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

#Use PyMongo to establish Mongo Connection
client = MongoClient("mongodb://localhost:27017")
mars_db = client["mars_db"]
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars_db = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", data=mars_db)

# Route that will trigger the scrape function
@app.route("/scrape")
def scraping():
    #Get into collection
    mars_col = mongo.db.collection
    # Run the scrape function
    data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_col.update({}, data, upsert=True)
    # Redirect back to home page
    return redirect("/",code = 302)


if __name__ == "__main__":
    app.run(debug=False)
