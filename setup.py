from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'gordonbdnumber1cat'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movies.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session

# models
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    rating = db.Column(db.Integer, db.ForeignKey('ratings.id'))
    run_time = db.Column(db.Integer)
    distributor = db.Column(db.Integer, db.ForeignKey('distributors.id'))
    genre = db.Column(db.String(24))
    director = db.Column(db.Integer, db.ForeignKey('directors.id'))

    def __repr__(self):
        return '{} which is rated {}'.format(self.title,Rating.query.filter_by(id=self.rating).first().text)

class Rating(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    text = db.Column(db.String(64))
    movies = db.relationship('Movie',backref='Rating')

    def __repr__(self):
        return "{} rating with number value {}".format(self.text,self.num)

class Distributor(db.Model):
    __tablename__ = "distributors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    movies = db.relationship('Movie',backref='Distributor')

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(24))
    lname = db.Column(db.String(24))
    movies = db.relationship('Movie',backref='Director')

    def __repr__(self):
        return "Director {} {} with {} movies".format(self.fname,self.lname,len(self.movies))

# functions to get or create new values
def get_rating(rating_text,rating_num=None):
    rating = Rating.query.filter_by(text=rating_text).first()
    if rating:
        return rating
    else:
        return 'This is not a valid MPAA rating. Please use one of the following: G, PG, PG-13, R, or NC-17'

def get_or_create_distributor(distributor_name):
    distributor = Distributor.query.filter_by(name=distributor_name).first()
    if distributor:
        return distributor
    else:
        distributor = Distributor(name=distributor_name)
        session.add(distributor)
        session.commit()
        return distributor

def get_or_create_director(first,last):
    director = Director.query.filter_by(fname=first,lname=last).first()
    if director:
        return director
    else:
        director = Director(fname=first,lname=last)
        session.add(director)
        session.commit()
        return director
