from flask import Flask, render_template, request, flash, jsonify, redirect
from markupsafe import escape
import requests
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from  smtplib import  SMTP


# CONSTANTS
# Email credentials:
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
API_KEY = os.environ.get("API_KEY") # API KEY
SECRET_KEY = os.urandom(12) # Flask secret key
year = datetime.now().year # current year

# Instantiating 'app' variable from class Flask
app = Flask(__name__)
app.secret_key = SECRET_KEY

# DB configuration
# DB location and name
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # Initialize the DB
ma = Marshmallow(app) # Init marshmallow

# Create model class
class Movies(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  title = db.Column(db.String(200), nullable=False, unique=True)
  poster = db.Column(db.String(200), nullable=True)
  
  def __init__(self, title, poster): # Constructor
    self.title = title
    self.poster = poster
      

class MovieSchema(ma.Schema): # Movie DB schema
  class Meta:
    fields = ("id", "title", "poster")


# Init Schema
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# API key response
response = f"http://www.omdbapi.com/?apikey={API_KEY}&s=star%20wars"
# Assigning API response to 'data' variable 
data = requests.get(url=response)

# ROUTES
@app.route("/", methods=["GET"]) # Main page
def homepage(): 
   
  # Check GET request response  and return json data
  movies = data.json()
  if movies["Response"] == "True":
    return render_template(
      escape("index.html"),
      movies=movies
    )
    
 
@app.route("/fav")  # Favorites
def fav_movies():
  # Query for all data in favorites DB and return it
  favorites = Movies.query.all()
  favorites_list = movies_schema.dump(favorites)
  
  if len(favorites_list) == 0: # Render empty message if Favorites is empty
    flash("you have no items yet in your Favorites list")
  
  return render_template(
    escape("favorites.html"),
    favorites_list=favorites_list
  )   
  
 
@app.route("/add_fav/<title>")  # Add to favorites - movie-info route
def add_title(title):
  # Instantiate a json object from the API response
  movie =  requests.get(
  url=f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
  ).json()
  
  # Declare title and poster(title image) 
  title_name = movie["Title"]
  poster = movie["Poster"]
  
  # Add title and poster to DB and save
  fav_item = Movies(title_name, poster)
  if Movies.query.filter_by(title=title_name).first():
    flash(f"{title_name} is already in your Favorites!")
  else:
    db.session.add(fav_item)
    db.session.commit()
    flash(f"{title_name} has been added to your Favorites!")
  
  return render_template(
  escape("movie-info.html"),
  movie=movie
  )
  

@app.route("/add_fav_search/<title>")  # Add to Favorites - search-form route
def add_title_search(title):
  # Instantiate a json object from the API response
  movie =  requests.get(
  url=f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
  ).json()
  
  # Declare title and poster(title image) 
  title_name = movie["Title"]
  poster = movie["Poster"]
  
  # Add title and poster to DB and save
  fav_item = Movies(title_name, poster)
  if Movies.query.filter_by(title=title_name).first():
    flash(f"{title_name} is already in your Favorites!")
  else:
    db.session.add(fav_item)
    db.session.commit()
    flash(f"{title_name} has been added to your Favorites!")
  
  return render_template(
  escape("search-form.html"),
  movie=movie
  )
  

@app.route("/remove_fav/<title_id>") # Remove title from Favorites
def remove_title(title_id):
  title = Movies.query.get(title_id)
  db.session.delete(title)
  db.session.commit() 
  flash(f"{title.title} has been removed from Favorites!")
  return redirect("/fav")


# Movie details route 
@app.route("/movie_info/<title_ID>")
def movie_info(title_ID):
  movie =  requests.get(
    url=f"http://www.omdbapi.com/?apikey={API_KEY}&t={title_ID}"
    ).json()
 
  if request.method == "GET":
    return render_template(
      escape("movie-info.html"),
      movie=movie
    )
  
# Advanced Search route
@app.route('/search-movies', methods=["GET", "POST"])
def search_movies():
  # method: POST - return requested data
  if request.method == "POST":
    # Declare inputs fields in variables with submitted form values
    title = request.form["title"]
    year = request.form["year"]
    type = request.form["type"]
        
    # Check if the user provided Year or Type data
    if year != "" or type != "":
        movie = requests.get(
          url=f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}&y={year}&type={type}"
          ).json()
    else:
      movie = requests.get(
        url=f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
      ).json()

    # Check if no data returned upon searching 
    if movie["Response"] == "False":
      flash("Title not found!")
      
      return render_template(
        escape("search-form.html")
      ) 
      
    # Render response payload
    return render_template(
        escape("search-form.html"),
        movie=movie
    )
    
  # method: GET - return Search Form
  else:
    return render_template(
          escape("search-form.html")
    )

# Navbar Search route
@app.route('/search-nav', methods=["POST"])
def search_nav():
    # Adding users search variable into the API json response
    search_mov = request.form["search_mov"] 
    movies = requests.get(url=f"http://www.omdbapi.com/?apikey={API_KEY}&s={search_mov}").json()

    # In case search returns no data
    if movies["Response"] == "False":
      flash("Your search did not return any result!")
      return render_template(
        escape("search-nav.html"),
        movies=movies
     )
    
    # Render search result   
    return render_template(
        escape("search-nav.html"),
        movies=movies
     )


# Contact me - route
@app.route("/contact_me", methods=["GET", "POST"])
def contact_me():
    # Post request - Receive an email from Contact Me form
  if request.method == "POST":
      name = request.form.get("name")
      email = request.form.get("email")
      subject = request.form.get("subject")
      message = request.form.get("message")
    
      server = SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(user=EMAIL_ADDRESS, password=EMAIL_PASS)
      server.sendmail(
          from_addr=email,  # email address from form input
          to_addrs=EMAIL_ADDRESS, # your email address - recipient
          msg=f"Subject: {subject}\n\n{message}"
              f"From: {name.title()}\n"
              f"Email: {email}\n"
              f"Subject: {subject.capitalize()}\n\n"
              f"{message.capitalize()}".encode("utf8")
      )
      flash(f"Thank you {name.title()} for your message!")
      print(name, email, subject, message)
      return render_template(
        "contact-me.html",
        name=name
      )
  if request.method == "GET":
     return render_template(
        "contact-me.html"
      )
     
# Page not found route:
@app.errorhandler(404)
def page_not_found(error):
  flash("Page not found error 404")
  return render_template(
    escape("error.html"),
    error=error,  
  ), 404


if __name__ == "__main__":
  app.run(debug=True)
  