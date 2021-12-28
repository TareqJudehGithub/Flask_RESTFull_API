# Title: Movies Query 

#### Video Demo: https://youtu.be/Q1cqGoEr24U
#### Description:
Movies Query 
  Movies Query is a RESTful API web app,  where users can browse and search for movies/series using Python 
  and a web service API called OMBD, build their own collection of their movies/series on a favorite list 
  with the help of Python and SQL Alchemy, and contact the page admin sending a message to his/her email or social media addresses.

Building the app
  Movies Query was developed and designed using Python/Flask/SQL Alchemy/API/JS/Bootstrap/HTML/CSS/Font Awesome.
  The app include features like API HTTP GET/POST requests, RESTful operations GET/POST/ and DELETE requests using Python and SQL Alchemy Database, and posting form data.

Below is a list of dependencies and libraries used:
Libraries/dependencies	Description	Installation
Python v3.9.7 virtual environment (venv)	
  A virtual environment containing all libraries and dependencies used in building up the web app	
  $ python -m venv venv

Python Flask v2/Jinja2	Backend framework.
  Jinja2 a templating engine that allows writing Python code in HTML files.	
  $ python -m pip install flask

requests	Handles HTTP/API requests	
  $ python -m pip install requests

OMBD API Key
  OMDB is a RESTful web service to obtain movie information.
  http://www.omdbapi.com/	where you can easily register and obtain your free API OMDB key.
  
Flask-SQLAlchemy	DB ORM for Storing Json data and to perform CRUD operations.	
$ python -m pip install flask-sqlalchemy

Flask-marshmallow,
  Marshmallow- SQLAlchemy	An object serialization for Python and SQL ALchemy	
  $ python -m pip install

Bootstrap v5, Google Fonts, and Font Awesome. 
  These tools were used to help build the frontend of the web app.	

Note: All dependencies and libraries used in the project are included in requirements.txt

Project files:
server.py
  server.py is the app main file, where all the logic an functionality of the web app take place.
  
/templates/*.html 
  The wep app view files and render files. 
  
/static/styles.css and Bootstrap v5
  Both styles.css and Bootstrap v5 are responsible for app design and responsivness.
 
 db.sqlite
  SQL Alchemy database file, where all data is kept and stored at.
 

After activating venv, kindly include these three variables below in your venv:
  
  $ export EMAIL_ADDRESS=your_email_address
  $ export EMAIL_PASS=your_email_password
  $ export API_KEY=your_OMDB_API_key obtained from http://www.omdbapi.com/


For further information and inquires please contact me.
  
Best regards,
Tareq Judeh
