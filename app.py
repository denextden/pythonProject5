# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii' : False, 'indent': 4}

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MoviesSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


# movie_schema = MovieSchema()
# movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if genre_id:
            movies = Movie.query.filter(Movie.director_id == director_id)
        elif director_id:
            movies = Movie.query.filter(Movie.genre_id == genre_id)
        else:
            movies = Movie.query.all()
        return MoviesSchema(many=True).dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        db.session.add(new_movie)
        db.session.commit()
        db.session.close()

        return '', 204


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get_one(self, mid):
        movie = Movie.query.get(mid)
        return MoviesSchema().dump(movie), 200

    def put(self, mid):
        req_json = request.json
        movie = Movie.query.get(mid)

        movie.id = req_json['id']
        movie.title = req_json['title']
        movie.description = req_json['description']
        movie.trailer = req_json['trailer']
        movie.year = req_json['year']
        movie.rating = req_json['rating']
        movie.genre_id = req_json['genre_id']
        movie.director_id = req_json['director_id']

    def delete(self, mid):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        db.session.close()


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return DirectorSchema(many=True).dump(directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        db.session.add(new_director)
        db.session.commit()
        db.session.close()

        return '', 204


@directors_ns.route('/<int:did>')
class DirectorsView(Resource):
    def get_one(self, did):
        director = Director.query.get(did)
        return DirectorSchema().dump(director), 200

    def put(self, did):
        req_json = request.json
        director = Director.query.get(did)

        director.id = req_json['id']
        director.name = req_json['name']

    def delete(self, did):
        director = Director.query.get(did)
        db.session.delete(director)
        db.session.commit()
        db.session.close()


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return GenreSchema(many=True).dump(genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        db.session.add(new_genre)
        db.session.commit()
        db.session.close()

        return '', 204


@genres_ns.route('/<int:gid>')
class GenresView(Resource):
    def get_one(self, gid):
        genre = Genre.query.get(gid)
        return GenreSchema().dump(genre), 200

    def put(self, gid):
        req_json = request.json
        genre = Genre.query.get(gid)

        genre.id = req_json['id']
        genre.name = req_json['name']

    def delete(self, gid):
        genre = Genre.query.get(gid)
        db.session.delete(genre)
        db.session.commit()
        db.session.close()


if __name__ == '__main__':
    app.run(debug=True)
