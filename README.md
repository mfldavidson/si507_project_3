# SI 507 Project 3: Movies App and ER Diagram with SQLite Database
## About the Movies App
This program in SI507_project_3.py is a Flask app that uses a SQLite database defined in setup.py (by importing setup.py into SI507_project_3.py) to create routes that use movie data in the database or add new movies to the database. Before running the app, the program creates the database and adds values for the standard MPAA movie ratings (G, PG, etc) to the ratings table.

### About setup.py
setup.py creates and configures the Flask app ('app') and defines models/tables for Movie, Rating, Director, and Distributor. It also defines functions to use to get the ID for a rating given the text, to get the ID for a director given the first and last name if it exists or else create a new director, and to get the ID for a distributor given the name if it exists or else create a new distributor. Refer to the entity-relationship diagram below for the database structure and available attributes of each table.

![ER Diagram of the movies database](https://github.com/mfldavidson/si507_project_3/blob/master/SI507%20Project%202%20Movies%20ERD.png?raw=true)

### The routes available in the app include:
- The home/index route (/) displays the number of movies recorded in the app by querying the movies table and counting the number of instances of Movie. If there are no movies, it displays text saying that there are no movies. It displays links to each of the other routes except for the route to create a new movie, for which it displays instructions.
- The route `/movie/new/<title>/<rating>/<directorfname>/<directorlname>/<distributor>/` creates a new instance of Movie in the movies table of the database using values the user inputs in each of the items in the `<>`. For example, if the user navigates to the route `/movie/new/Top Gun/PG/Tony/Scott/Paramount/`, a new instance of Movie will be created in the movies table with the title Top Gun, rating PG, director Tony Scott, and distributor Paramount. This route also creates new values for director and distributor if the director or distributor does not already exist in the appropriate tables. If an invalid rating is entered (i.e. text that does not map to the text value of an existing MPAA rating), the user is told to select a valid rating and the movie is not created.
- The route `/all_movies` lists all movies currently in the database by title and rating, or, if there are none, returns a message informing the user that there are no movies in the database.
- The route `/all_directors` lists all directors currently in the database by full name and the number of movies associated with them in the database, or, if there are none, returns a message informing the user that there are no directors in the database.
- The route `/movies_by_rating` asks the user for input (in the Terminal, not in the browser) of what MPAA rating they want to see movies for, and returns all movies in the databse that have that rating. The requested input is the text value of the MPAA rating (i.e. G, PG, PG-13, R, NC-17, Not Rated). If an invalid value is entered, the user sees a message that the input was invalid and to reload the page and try again. If no movies exist with this rating, the user sees a message that no movies have that rating.

# How to Run the Program
This program was written with Python Anaconda, Flask module, and SQLAlchemy using a virtual environment. Requirements to run the program can be found in requirements.txt. To install everything from requirements.txt, download the requirements.txt file, activate your virtual environment, and then enter the following in your shell: `pip install -r requirements.txt`.

In order to run the program, make sure you are in the same directory as all the files, and then enter the following in your shell: `python SI507_project_3.py runserver`. The program can then be found running at `localhost:5000` plus the correct route in your browser.
