import os
from flask_sqlalchemy import SQLAlchemy


DATABASE_URL = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
  binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=DATABASE_URL):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


actors = db.Table(
    'actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True)
)


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))

    def __repr__(self):
        return self.name
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'movies': [movie.short_format() for movie in self.movies]
        }
    
    def short_format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
        }


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    release_date = db.Column(db.String(120))
    actors = db.relationship('Actor', secondary=actors, lazy='subquery',
                             backref=db.backref('movies', lazy=True))           

    def __repr__(self):
        return self.title

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.short_format() for actor in self.actors]
        }
    
    def short_format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }



