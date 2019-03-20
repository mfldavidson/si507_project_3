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
            return "New movie: {}".format(movie)

@app.route('/all_movies')
def see_all():
    movies = Movie.query.all()
    return render_template('all_movies.html',movies=movies)

@app.route('/all_directors')
def see_all_directors():
    directors = Director.query.all()
    return render_template('all_directors.html',directors=directors)


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
