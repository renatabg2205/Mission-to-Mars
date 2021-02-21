#Import tools
from flask import Flask, render_template, redirect #we'll use Flask to render a template
from flask_pymongo import PyMongo #we'll use PyMongo to interact with our Mongo database
import scraping #to use the scraping code, we will convert from Jupyter notebook to Python

#Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" 
#The line above tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
#This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
mongo = PyMongo(app)

#Define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
#The line above uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. 
# We will also assign that path to themars variable for use later.
   return render_template("index.html", mars=mars)
# The line above tells Flask to return an HTML template using an index.html file. 
# We'll create this file after we build the Flask routes.
# , mars=mars) tells Python to use the "mars" collection in MongoDB.

#Set up the scraping route
@app.route("/scrape") #Defines the route that Flask will be using. This route, “/scrape”, will run the function that we create just beneath it.
def scrape():
   mars = mongo.db.mars #assign a new variable that points to our Mongo database
   mars_data = scraping.scrape_all() #Create a new variable to hold the newly scraped data. In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.
   mars.update({}, mars_data, upsert=True) #Now that we've gathered new data, we need to update the database. We're inserting data, so first we'll need to add an empty JSON object with {}
   #upsert=True indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).
   return redirect('/', code=302) #This will navigate our page back to / where we can see the updated content.

if __name__ == "__main__":
   app.run(debug=True)