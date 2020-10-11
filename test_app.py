import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


def sample_movie(title='Hannibal', release_date='2020.08.09'):
    return Movie(title=title, release_date=release_date)


def sample_actor(name='Jane Kandy', age=32, gender='Male'):
    return Actor(name=name, age=age, gender=gender)


class MovieTestCase(unittest.TestCase):
    """This class represents the poject test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',
                                                         self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            "title": "King Kong",
            "release_date": "2020.02.01"
        }
        self.new_actor = {
            "name": "Shakhrukh Khan",
            "age": 59,
            "gender": "male"
        }
        self.token3 = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJfYWxzVlp3RlpURDF4Zmo3T2FoQiJ9.eyJpc3MiOiJodHRwczovL3dqai5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY4MTMzNDU5MmJjYTUwMDY5ZGIxNGU4IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MDIzNTE0NTMsImV4cCI6MTYwMjQyMzQ1MywiYXpwIjoiWGNjeTFSSEdwYWxNZGtlbUplWU92cUdmazRQNlBFNUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.abRdWs5lmhi7YfknI4JSPS-GUvAu1ZoYy_qJxkgOwacrwGDDR9ItGi6h70i6if8ENZOU28VIzTlymgwWpm3pHlIV9grh39KAQYsVXPpRSjdGj5LS6LZK89sFZgxKzmnWjmkd0gM2VScXjhsLE1LjRR5sN5C-63rUzmBx1ru_1KxxsQrd-CffIDzADevww45Sf6Yfg_CuIWlRlHd1KKsEUQz3h42Z-NzXFIPXrvvrJ8GuFTrl2NBwr7AT8ngFUEMMKrcQVvKVb7_ieJF-ulCIuNf24bl3aJHksaktYe3b4vm35ptrMmirLYUvVJmQpV3VF7zyvXG13jWZIVlwgq4ZGw'
        self.token1 = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJfYWxzVlp3RlpURDF4Zmo3T2FoQiJ9.eyJpc3MiOiJodHRwczovL3dqai5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZjM5M2MwZjcyYjQwMDY3YjQxYmY5IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MDIzNTE2NDcsImV4cCI6MTYwMjQyMzY0NywiYXpwIjoiWGNjeTFSSEdwYWxNZGtlbUplWU92cUdmazRQNlBFNUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.Ma5qgY503IQ6WNqQPjqKFAvoUPNw14hMfnwvtI-xpqtxCFHK-w5LsVS2HlLmk_GF37VRXGV0p_iX4VAeowJ4ciUBMBeEtZzkJYte6aKwFpL1TZmEMJDg5DvYqjj4M-wj71HMKssJt3kEx69OUbmu11Eqtn2tdsPYYs-Gxz8iuq_szVRdDZa_YR5zfA7U_3HEEJvKwLbGu8C73HxWeMom--wPpZOBfDC56SUTLs50tTSQIFVIrL0XFg_oUzfMN66qEu6rS7VHcIZhknmLM35t02u_L6hDxL3sE3v_emZpfHbcY2dyo2F9pzHIumCaNVqinaV3e6Uqv2fNSENiFzuCcA'
        self.token2 = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJfYWxzVlp3RlpURDF4Zmo3T2FoQiJ9.eyJpc3MiOiJodHRwczovL3dqai5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZjM5OWEwODc3ZmQwMDY3NzA1YmJmIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MDIzNTE3OTksImV4cCI6MTYwMjQyMzc5OSwiYXpwIjoiWGNjeTFSSEdwYWxNZGtlbUplWU92cUdmazRQNlBFNUciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImRlbGV0ZTphY3RvciIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.CNNLD1jyfbUG5KECDH3SlvOcIoqN16ulR2d2mqQz4nYHnwnL7c5bElDYThojPZ0oZA-AB4LjXqJcYSTnT9FSXFlBvbw83ZGGrEvGquKMigF3gAvkysPMLoCAlDCGb5srpP6na5nVjKjbZRVoefc2QCeuc7WCOBxPbRlm5GgK9r8G6c9BbBqXNOfV6YGBugihQFcE101z6XrRauL_JHC2PKGQz8SMZj4WxG8XAfkyejPjjj3NXP20GCDbTNIQ3QtFCKXUlLJrM97uDSbiqnLoyEUsUhGMiFkjC2AIujaC1MxCbJmuZjqy_ernafPAnJFVoKWammhSsFARbH17CgbqEg'
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.db.session.add(sample_actor())
            self.db.session.add(sample_movie(title='movie2'))
            self.db.session.add(sample_actor(name='actor2'))
            self.db.session.add(sample_movie())
            self.db.session.commit()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_movies(self):
        res = self.client().get('/movies',
                        headers=dict(Authorization='Bearer ' + self.token1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_failed_getting_paginated_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/movies?page=1000',
                headers=dict(Authorization='Bearer ' + self.token1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json={"title": "New Title"},
                       headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['title'], 'New Title')

    def test_400_for_failed_update(self):
        res = self.client().patch('/movies/1', json={},
                        headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_fails_update_whitout_permission(self):
        res = self.client().patch('/movies/1', json={'title': 'movie title'},
                        headers=dict(Authorization='Bearer ' + self.token1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_delete_movie(self):
        res = self.client().delete(('/movies/22'),
                headers=dict(Authorization='Bearer ' + self.token3))
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 22).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 22)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
        self.assertEqual(movie, None)

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000',
                        headers=dict(Authorization='Bearer ' + self.token3))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                        headers=dict(Authorization='Bearer ' + self.token3))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_fails_movie_creation_with_invalid_data(self):
        res = self.client().post('/movies', json={"title": ""},
                        headers=dict(Authorization='Bearer ' + self.token3))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_403_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies', json=self.new_movie,
                        headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_get_paginated_actors(self):
        res = self.client().get('/actors',
                    headers=dict(Authorization='Bearer ' + self.token1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_beyond_valid_page_for_actors(self):
        res = self.client().get('/actors?page=1000',
                    headers=dict(Authorization='Bearer ' + self.token1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_update_actor(self):
        res = self.client().patch('/actors/1', json={'name': 'NEWNAME'},
                        headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['name'], 'NEWNAME')

    def test_400_for_failed_update_actor(self):
        res = self.client().patch('/actors/1', json={},
                    headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_failed_update_actor_without_permission(self):
        res = self.client().patch('/actors/1', json={"name": "Mark"},
                    headers=dict(Authorization='Bearer ' + self.token1))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_delete_actor(self):
        res = self.client().delete('/actors/13',
                        headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 13).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 13)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
        self.assertEqual(actor, None)

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000',
                        headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'page not found')

    def test_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                        headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_fails_actor_creation_with_invalid_data(self):
        res = self.client().post('/actors', json={'name': ''},
                        headers=dict(Authorization='Bearer ' + self.token2))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors', json=self.new_actor,
                        headers=dict(Authorization='Bearer ' + self.token1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()

