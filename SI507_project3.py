from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import setup
from setup import *

# Routes
@app.route('/')
def index():
    movies = Movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', movies=movies, num_movies=num_movies)

@app.route('/movie/new/<title>/<rating>/<directorfname>/<directorlname>/<distributor>/')
def new_movie(title,rating,directorfname,directorlname,distributor):
    if Movie.query.filter_by(title=title).first():
        return "There is already a movie with this title"
    else:
        rating = get_rating(rating)
        if type(rating) == str:
            return rating
        else:
            director = get_or_create_director(directorfname,directorlname)
            distributor = get_or_create_distributor(distributor)
            movie = Movie(title=title, rating=rating.id,director=director.id,distributor=distributor.id)
            session.add(movie)
            session.commit()
            return render_template('new_movie.html',mov=movie)

@app.route('/all_movies')
def see_all():
    movies = Movie.query.all()
    return render_template('all_movies.html',movies=movies)

@app.route('/all_directors')
def see_all_directors():
    directors = Director.query.all()
    return render_template('all_directors.html',directors=directors)

@app.route('/movies_by_rating')
def see_movies_by_rating():
    rating_from_user = input('Enter a rating (text value) to show all movies with that rating. Valid ratings: G, PG, PG-13, R, or NC-17')
    ratings = Rating.query.all()
    rating_is_valid = False
    for rating in ratings:
        if rating.text == rating_from_user:
            movies = rating.movies
            rating_is_valid = True
            break
    if rating_is_valid == False:
        movies = None
    return render_template('ratings.html',rating_is_valid=rating_is_valid,movies=movies)


if __name__ == '__main__':
    db.create_all()
    for rating in [(1,'G'),(2,'PG'),(3,'PG-13'),(4,'R'),(5,'NC-17'),(None,'Not Rated')]:
        rating_exists = Rating.query.filter_by(text=rating[1]).first()
        if rating_exists:
            continue
        else:
            new_rating = Rating(text=rating[1],num=rating[0])
            session.add(new_rating)
    session.commit()
    app.run()
