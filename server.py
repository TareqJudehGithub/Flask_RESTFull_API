from flask import Flask, render_template, request, flash
from markupsafe import escape
import requests
import os
from datetime import datetime


# Flask secret key
secret_key = os.urandom(12)
# Instantiating 'app' variable from class Flask
app = Flask(__name__)
app.secret_key = secret_key
# current year
year = datetime.now().year

# API response
response = "http://www.omdbapi.com/?apikey=deec4c57&s=star%20wars&type=movie"
# Assigning API response to 'data' variable 
data = requests.get(url=response)


# TODO TASK 1. GET: 
# Main page route - movies route
@app.route("/")
def homepage():  
  # Check GET response for returned data
  movies = data.json()
  if movies["Response"] == "True":
    return render_template(
      escape("index.html"),
      movies=movies
    )
  else:
    flash("Requested data not found")
    return render_template(
      escape("error.html")
    )

# Movie details route 
@app.route("/move_info/<title_ID>")
def movie_info(title_ID):
  movie =  requests.get(
    url=f"http://www.omdbapi.com/?apikey=deec4c57&t={title_ID}"
    ).json()
  return render_template(
    escape("movie-info.html"),
    movie=movie
  )

# TODO TASK 2. POST: 
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
          url=f"http://www.omdbapi.com/?apikey=deec4c57&t={title}&y={year}&type={type}"
          ).json()
    else:
      movie = requests.get(
        url=f"http://www.omdbapi.com/?apikey=deec4c57&t={title}"
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
    movies = requests.get(url=f"http://www.omdbapi.com/?apikey=deec4c57&s={search_mov}").json()

    
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
  