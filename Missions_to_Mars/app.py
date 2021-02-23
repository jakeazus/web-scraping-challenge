from flask import Flask, render_template, redirect 
import pymongo
import scrape_mars



# Use PyMongo to establish Mongo connection
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

#Create an instance of Flask
app = Flask(__name__)

# Route to render index.html template using data from Mongo
@app.route('/')
def home():

    # Find one record of data from the mongo database
    mars = collection.find_one()

    # Return template and data
    return render_template('index.html', mars=mars)

# Route that will trigger the scrape function
@app.route('/scrape')
def scrape():
    scrape_mars.mars_scrape()
    return redirect("/", code=302)
    



if __name__ == "__main__":
    app.run(debug=True)


