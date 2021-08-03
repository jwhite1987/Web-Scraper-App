from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb+srv://jimmywhite87:Ruger2012@cluster0.caep8.mongodb.net/missionstomars?retryWrites=true&w=majority")

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", vacation=mars_data)



@app.route("/images")
def images():
    mars_data = mongo.db.collection.find_one()
    return render_template("images.html", vacation=mars_data)


if __name__ == "__main__":
    app.run(debug=True)
