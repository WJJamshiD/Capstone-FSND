from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import requires_auth, AuthError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    MOVIE_PER_PAGE = 10

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    def paginate_movies(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page-1)*MOVIE_PER_PAGE
        end = start+MOVIE_PER_PAGE

        items = [item.format() for item in selection]
        current_items = items[start:end]

        return current_items

    # Endpoints

    '''
    An endpoint to handle GET requests for listing movies,
    including pagination (every 10 movies).
    This endpoint returns a list of movies and
    number of total movies.
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def retrieve_movies(payload):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_movies(request, movies)
        except Exception:
            return abort(500)

        if len(current_movies) == 0:
            return abort(404)

        return jsonify({
                'success': True,
                'movies': current_movies,
                'total_movies': len(movies)
                })
    '''
    An endpoint to handle POST requests for creating a new movie
    which requieres movie title, release date and actors.This endpoint
    returns created movie's id, movie list and total movies number.
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movie')
    def create_movie(payload):
        body = request.get_json()
        movie_title = body.get('title', None)
        movie_release_date = body.get('release_date', None)
        movie_actors = body.get('actors', None)
        search = body.get('search', None)

        if search:
            movies = Movie.query.filter(Movie.title.ilike(f'%{search}%')).all()
            current_movies = paginate_movies(request, movies)

            return jsonify({
                'success': True,
                'movies': current_movies,
                'total_movies': len(movies)
                })
        else:
            if (movie_title is None) or (movie_release_date is None):
                abort(400)
        movie = Movie(release_date=movie_release_date,
                      title=movie_title)
        try:
            if movie_actors:
                for actor_id in movie_actors:
                    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
                    if not actor:
                        abort(400)
                    movie.actors.append(actor)
            movie.insert()

            movies = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_movies(request, movies)

            return jsonify({
                'success': True,
                'created': movie.id,
                'movies': current_movies,
                'total_movies': len(movies)
                })
        except Exception:
            abort(500)

    '''
    An endpoint to handle GET request for retrieving a
    movie which includes movie title, release date and its actors
    '''
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('view:movies')
    def retrieve_single_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format(),
            'total_movies': Movie.query.count()
        })

    '''
    An endpoint to handle PATCH request for updating an existing
    movie.
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('edit:movie')
    def update_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        body = request.get_json()
        movie_title = body.get('title', None)
        movie_release_date = body.get('release_date', None)
        movie_actors = body.get('actors', None)
        if not (movie_title or movie_release_date or movie_actors):
            abort(400)
        if movie_title:
            movie.title = movie_title
        if movie_release_date:
            movie.release_date = movie_release_date
        if movie_actors:
            actors = []
            for actor_id in movie_actors:
                actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
                if not actor:
                    abort(400)
                actors.append(actor)
            movie.actors = actors
        try:
            movie.update()
            movies = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_movies(request, movies)

            return jsonify({
                'success': True,
                'message': 'Updated succesfully',
                'updated': movie.id,
                'movies': current_movies,
                'total_movies': Movie.query.count()
            })
        except Exception:
            abort(422)

    '''
    An endpoint to handle DELETE request for updating an existing
    movie.
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        try:
            movie.delete()
            movies = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_movies(request, movies)

            return jsonify({
                'success': True,
                'message': 'Deleted succesfully',
                'deleted': movie_id,
                'movies': current_movies,
                'total_movies': len(movies)
            })
        except Exception:
            abort(422)

    '''
    An endpoint to handle GET requests for listing actors,
    including pagination (every 10 movies).
    This endpoint returns a list of actors and
    number of total actors.
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def retrieve_actors(payload):
        try:
            actors = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_movies(request, actors)
        except Exception:
            return abort(500)

        if len(current_actors) == 0:
            return abort(404)

        return jsonify({
                'success': True,
                'actors': current_actors,
                'total_actors': len(actors)
                })

    '''
    An endpoint to handle POST requests for creating a new actor
    which requieres actor name, age and gender.
    This endpoint returns created actor's id, actors list and total number.
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def create_actor(payload):

        body = request.get_json()

        actor_name = body.get('name', None)
        actor_age = body.get('age', None)
        actor_gender = body.get('gender', None)
        search = body.get('search', None)

        if search:
            actors = Actor.query.filter(Actor.name.ilike(f'%{search}%')).all()
            current_actors = paginate_movies(request, actors)

            return jsonify({
                'success': True,
                'actors': current_actors,
                'total_actors': len(actors)
                })
        else:
            if (actor_name is None) or (actor_age is None) \
                                or (actor_gender is None):
                abort(400)
        try:
            actor = Actor(name=actor_name,
                          age=actor_age,
                          gender=actor_gender)
            actor.insert()

            actors = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_movies(request, actors)

            return jsonify({
                'success': True,
                'created': actor.id,
                'actors': current_actors,
                'total_actors': len(actors)
                })
        except Exception:
            abort(500)

    '''
    An endpoint to handle GET request for retrieving an
    actor which includes actor name, age, gender and its movies
    '''
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('view:actors')
    def retrieve_single_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format(),
            'total_movies': Actor.query.count()
        })

    '''
    An endpoint to handle PATCH request for updating an existing
    actor.
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:actor')
    def update_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        body = request.get_json()
        actor_name = body.get('name', None)
        actor_age = body.get('age', None)
        actor_gender = body.get('gender', None)
        if (actor_age is None) and (actor_gender is None)\
           and (actor_name is None):
            abort(400)
        if actor_name:
            actor.name = actor_name
        if actor_gender:
            actor.gender = actor_gender
        if actor_age:
            actor.age = actor_age
        try:
            actor.update()
            actors = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_movies(request, actors)

            return jsonify({
                'success': True,
                'message': 'Updated succesfully',
                'updated': actor.id,
                'actors': current_actors,
                'total_actors': Actor.query.count()
            })
        except Exception:
            abort(422)

    '''
    An endpoint to handle DELETE request for deleting an existing
    actor.
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        try:
            actor.delete()
            actors = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_movies(request, actors)

            return jsonify({
                'success': True,
                'message': 'Deleted succesfully',
                'deleted': actor_id,
                'actors': current_actors,
                'total_actors': len(actors)
            })
        except Exception:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'page not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(405)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'forbidden'
        }), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(ex):
        res = jsonify(ex.error)
        res.status_code = ex.status_code
        return res

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
