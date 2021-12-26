from flask import Flask, render_template, request, flash, jsonify, redirect
from markupsafe import escape
import requests
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Flask secret key
secret_key = os.urandom(12)
# Instantiating 'app' variable from class Flask
app = Flask(__name__)
app.secret_key = secret_key

# current year
year = datetime.now().year


# DB configuration
# DB location and name
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize the DB
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Create model class
class Movies(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  title = db.Column(db.String(200), nullable=False, unique=True)
  poster = db.Column(db.String(200), nullable=True)
  
 
  # Constructor
  def __init__(self, title, poster):
    self.title = title
    self.poster = poster
      

# Movie schema
class MovieSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "poster")


# Init Schema
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# API key and response
API_KEY = os.environ.get("API_KEY")
response = f"http://www.omdbapi.com/?apikey={API_KEY}&s=harry%20potter&type=movie"
# Assigning API response to 'data' variable 
data = requests.get(url=response)


# Main page route - movies route
@app.route("/", methods=["GET"])
def homepage(): 
   
  # Check GET response for returned data
  movies = data.json()
  
  if movies["Response"] == "True":
    return render_template(
      escape("index.html"),
      movies=movies
    )
    
  
# Return favorites titles  
@app.route("/fav")
def fav_movies():
  favorites = Movies.query.all()
  favorites_list = movies_schema.dump(favorites)
  
  if len(favorites_list) == 0:
    flash("you have no items yet in Favorites.")

  # Show favorites  
  return render_template(
    escape("favorites.html"),
    favorites_list=favorites_list
  )   
  
 
# Add to favorites
@app.route("/add_fav/<title>")
def add_title(title):

  # Instantiate a json object from the API response
  movie =  requests.get(
  url=f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
  ).json()
  
  # Declare title and poster(title image) from 
  title_name = movie["Title"]
  poster = movie["Poster"]
    
  fav_item = Movies(title_name, poster)
  if Movies.query.filter_by(title=title_name).first():
    flash(f"{title_name} is already in your favorites!")
  else:
    db.session.add(fav_item)
    db.session.commit()
  
    flash(f"{title_name} has been added to your favorites!")
    # return redirect("/")
  
  return render_template(
  escape("movie-info.html"),
  movie=movie
  )
  
  
# Remove title from Favorites
@app.route("/remove_fav/<title_id>")
def remove_title(title_id):
  title = Movies.query.get(title_id)
  db.session.delete(title)
  db.session.commit()
  
  flash(f"{title.title} has been removed from Favorites.")
  return redirect("/fav")


# Movie details route 
@app.route("/movie_info/<title_ID>", methods=["GET", "POST"])
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
  # method: POST - return response payload
  if request.method == "POST":
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
      # Display message for not finding any data and redirect to Adv Search
      flash("Requested data not found")
      return render_template(
        escape("search-form.html")
      ) 
      
    # Successful POST
    # Display message confirming data found
    flash("Insert done successfully")
    # Display response payload
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
    #
    search_mov = request.form["search_mov"] 
    movies = requests.get(url=f"http://www.omdbapi.com/?apikey={API_KEY}&s={search_mov}").json()

    
    # Display message for not finding any data and redirect to Adv Search
    if movies["Response"] == "False":
      flash("Requested data not found")
      return render_template(
        escape("search-form.html")
      )
      
    # Successful POST - # Display message confirming data found
    flash("Insert done successfully")
    return render_template(
        escape("search-nav.html"),
        movies=movies
     )

# Other routes:
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
  