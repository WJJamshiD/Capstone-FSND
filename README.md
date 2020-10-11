# Intro
This is the capstone project of `Udacity Full Stack Nanodegree` Course.
The Casting Agency API supports a basic castic agency by allowing users to query the database for movies and actors. There are three different user roles (and related permissions), which are:
- Casting agent: Can view actors and movies.
- Casting director: Can view, add, modify, or delete actors; can view and modify movies.
- Executive producer: Can view, add, modify, or delete actors and movies. 

# Running the API

API endpoints can be accessed via https://my-last-project-capstone-fsnd.herokuapp.com/

Auth0 information for endpoints that require authentication can be found in `setup.sh`.
And there is given three access tokens to use endpoinds with different roles.

# Running tests

To run the unittests, first CD into the Capstone folder and run the following command:
```
python test_app.py
```

# API Documentation

Errors
`400`
`401`
`403`
`404`
`405`
`422`
`500`

Note: all error handlers return a JSON object with the request status and error message.

400
- 400 error handler is returned when invalid data submitted. 
```
{
	"error": 400,
    	"success": false,
	"message": "bad request"
}
```
401
- 401 error handler is returned when there is an issue with the authentication necessary for the action being requested. 
```
{
	"error": 401,
	"code": "authorization_header_missing"
}
```
403
- 403 error handler occurs when the requested action is not allowed, i.e. incorrect permissions.
```
{
	"error": 403,
    	"code": "unauthorized"
	"description": "Permission not found."
}
```
404
- 404 error handler occurs when a request resource cannot be found in the database, i.e. an actor with a nonexistent ID is requested.
```
{
	"error": 404,
	"message": "page not found",
	"success": false
}
```
422
- 422 error handler is returned when the request contains invalid arguments, i.e. a difficulty level that does not exist.
```
{
	"error": 422,
	"message": "Request could not be processed.",
	"success": false
}
```
422
- 422 error handler is returned when the request contains invalid arguments, i.e. a difficulty level that does not exist.
```
{
	"error": 422,
	"message": "Request could not be processed.",
	"success": false
}
```
500
- 500 error handler is returned when any unexpected issues or database related errors occured.
```
{
	"error": 500,
	"message": "internal server error",
	"success": false
}
```

## Endpoints
`GET '/actors'`
`GET '/movies'`
`POST '/actors'`
`POST '/movies'`
`PATCH '/actors/<int:actor_id>'`
`PATCH '/movies/<int:movie_id>'`
`DELETE '/actors/<int:actor_id>'`
`DELETE '/movies/<int:movie_id>'`

### GET '/actors'
- Fetches a JSON object with a list of actors in the database.
- Request Arguments: None
- Returns: Multiple objects, such as actors, that contains multiple objects with a series of string key pairs, total_actors, which is shows total number of actors and response status.
```
{
    "actors": [
        {
            "age": "45",
            "gender": "male",
            "id": 1,
            "name": "Leonardo DiCaprio"
        },
        {
            "age": "42",
            "gender": "male",
            "id": 2,
            "name": "Jensen Ackles"
        },
    ],
    "total_actors": 2,
    "success": true
}
```
### GET '/movies'
- Fetches a JSON object with a list of movies in the database.
- Request Arguments: None
- Returns: Multiple objects, such as movies, that contains multiple objects with a series of string key pairs, total_moviess, which shows total number of movies and response status.
```
{
    "movies": [
        {
            "id": 1,
            "release": "December 19, 1997",
            "title": "Titatic"
        },
        {
            "id": 3,
            "release": "January 16, 2009",
            "title": "My Bloody Valentine"
        }
    ],
    "total_movies": 2,
    "success": true
}
```
### POST '/actors'
- Posts a new actor to the database, including the name, age, gender, and actor ID, which is automatically assigned upon insertion.
- Request Arguments: Requires three string arguments: name, age, gender.
- Returns: JSON object with the new inserted actor id, as created, total actors nubmer, as total_actors, a list of actors, as actors, and response status.

```
{
    "actors": [
        {
            "age": 35,
            "gender": "male",
            "id": 1,
            "movies": [],
            "name": "ALi"
        },
        {
            "age": 35,
            "gender": "male",
            "id": 2,
            "movies": [
                {
                    "id": 2,
                    "release_date": "2020",
                    "title": "King kong"
                }
            ],
            "name": "ALi"
        },
        {
            "age": 35,
            "gender": "male",
            "id": 3,
            "movies": [],
            "name": "ALi"
        },
        {
            "age": 35,
            "gender": "male",
            "id": 4,
            "movies": [
                {
                    "id": 4,
                    "release_date": "2000",
                    "title": "sidney"
                }
            ],
            "name": "ALi"
        },
        {
            "age": 22,
            "gender": "male",
            "id": 5,
            "movies": [
                {
                    "id": 4,
                    "release_date": "2000",
                    "title": "sidney"
                }
            ],
            "name": "Baxri"
        },
        {
            "age": 32,
            "gender": "male",
            "id": 6,
            "movies": [],
            "name": "King kong"
        },
        {
            "age": 35,
            "gender": "Male",
            "id": 7,
            "movies": [],
            "name": " Jamshi Y"
        }
    ],
    "created": 7,
    "success": true,
    "total_actors": 7
}
```
### POST '/movies'
- Posts a new movie to the database, including the title, release, and movie ID, which is automatically assigned upon insertion.
- Request Arguments: Requires two string arguments: title, release_date.
- Returns: JSON object with the new inserted movie id, as created, total movies nubmer, as total_movies, a list of movies, as movies, and response status.

```
{
    "movies": [
        {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
        {
        "id": 6,
        "release": "December 8, 2021",
        "title": "Thor: The final battle"
        }],
    "created": 6,
    "total_movies": 2,
    "success": true
}
```
### PATCH '/actors/<int:actor_id>'
- Patches an existing actor in the database.
- Request arguments: Actor ID, included as a parameter following a forward slash (/), and the key to be updated passed into the body as a JSON object. For example, to update the age for '/actors/6'
```
{
	"age": "36"
}
```
- Returns: JSON object with the updated actor id, as updated, total actors nubmer, as total_actors, a list of actors, as actors, an info message, as message and response status
```
{
    "actors": [{
        "age": "36",
        "gender": "male",
        "id": 6,
        "name": "Henry Cavill"
    }],
    "message": "Updated succesfully",
    "updated": 6,
    "total_actors": 1,
    "success": true
}
```
### PATCH '/movies/<int:movie_id>'
- Patches an existing movie in the database.
- Request arguments: Movie ID, included as a parameter following a forward slash (/), and the key to be updated, passed into the body as a JSON object. For example, to update the age for '/movies/5'
```
{
	"release": "November 3, 2017"
}
```
- Returns:  JSON object with the updated movie id, as updated, total movies nubmer, as total_movies, a list of movies, as movies, an info message, as message and response status.
```
{
    "movies": [{
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    }],
    "message": "Updated succesfully",
    "updated": 5,
    "total_movies": 1,
    "success": true
}
```
### DELETE '/actors/<int:actor_id>'
- Deletes an actor in the database via the DELETE method and using the actor id.
- Request argument: Actor id
- Returns: JSON object with the deleted actor id, as deleted, total actors nubmer, as total_actors, a list of actors, as actors, an info message, as message and response status
```
{
    "actors": [
        {
        "id": 2,
        "age": 22,
        "gender": "Male",
        "name": "Jamshid Y",
        "movies" : []
    }],
    "deleted": 1,
    "message": "Deleted succesfully",
    "total_actors": 1,
    "success": true
}
```
### DELETE '/movies/<int:movie_id>'
- Deletes a movie in the database via the DELETE method and using the movie id.
- Request argument: Movie id
- Returns: JSON object with the delete movie id, as deleted, total movies nubmer, as total_movies, a list of movies, as movies, an info message, as message and response status..
```
{
    "movies": [
        {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
        {
        "id": 6,
        "release": "December 8, 2021",
        "title": "Thor: The final battle"
        }],
    "deleted": 4,
    "message": "Deleted succesfully",
    "total_movies": 2,
    "success": true
}
```
