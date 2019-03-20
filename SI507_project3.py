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
    all_movies = []
    movies = Movie.query.all()
    for mov in movies:
        director = Director.query.filter_by(id=mov.director).first()
        rating = Rating.query.filter_by(id=mov.rating).first()
        all_movies.append((mov.title,' '.join([str(Director.fname),str(Director.lname)]),Rating.text))
    return render_template('all_movies.html',all_movies=all_movies)
#
# @app.route('/all_artists')
# def see_all_artists():
#     artists = Artist.query.all()
#     names = []
#     for a in artists:
#         num_songs = len(Song.query.filter_by(artist_id=a.id).all())
#         newtup = (a.name,num_songs)
#         names.append(newtup) # names will be a list of tuples
#     return render_template('all_artists.html',artist_names=names)


if __name__ == '__main__':
    db.create_all()
    for rating in [(1,'G'),(2,'PG'),(3,'PG-13'),(4,'R'),(5,'NC-17'),(None,'Not Rated')]:
        rating_exists = Rating.query.filter_by(text=rating[1]).first()
        if rating_exists:
            continue
        else:
            new_rating = get_or_create_rating(rating_text=rating[1],rating_num=rating[0])
            session.add(new_rating)
    session.commit()
    app.run() # run with this: python main_app.py runserver
