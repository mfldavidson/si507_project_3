# association tables
movie-rating = db.Table('movie-rating',db.Column('movie_id',db.Integer, db.ForeignKey('movies.id')),db.Column('rating_id',db.Integer, db.ForeignKey('ratings.id')))

movie-distributor = db.Table('movie-distributor',db.Column('movie_id',db.Integer, db.ForeignKey('movies.id')),db.Column('distributor_id',db.Integer, db.ForeignKey('distributors.id')))

movie-director = db.Table('movie-director',db.Column('movie_id',db.Integer, db.ForeignKey('movies.id')),db.Column('director_id',db.Integer, db.ForeignKey('directors.id')))

# models
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    rating = db.relationship('Rating',secondary=movie-rating,backref=db.backref('ratings',lazy='dynamic'),lazy='dynamic')
    run_time = db.Column(db.Integer)
    distributor = db.relationship('Distributor',db.backref('distributors',lazy='dynamic'),lazy='dynamic')
    genre = db.Column(db.String(24))
    director = db.relationship('Director',secondary=movie-director,backref=db.backref('Director',lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
        return '{} by director {}'.format(self.title,self.director)

class Rating(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    text = db.Column(db.String(64))

    def __repr__(self):
        return "{} rating with number value {}".format(self.text,self.num)

class Distributor(db.Model):
    __tablename__ = "distributors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(24))
    lname = db.Column(db.String(24))

    def __repr__(self):
        return "{} {}".format(self.fname,self.lname)

# functions to get or create new values
def get_or_create_rating(rating_text):
    rating = Rating.query.filter_by(text=rating_text).first()
    if rating:
        return rating
    else:
        rating = Rating(text=rating_text)
        session.add(rating)
        session.commit()
        return rating

def get_or_create_distributor(distributor_name):
    distributor = Distributor.query.filter_by(name=distrdistributor_name).first()
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
