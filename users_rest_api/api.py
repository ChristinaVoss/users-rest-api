from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from datetime import datetime
from json import dumps

from users_rest_api import app, db
from users_rest_api.secure_check import authenticate, identity
from users_rest_api.model import User

users_api = Blueprint('users_api', __name__)

api = Api(app)
# API AUTHENTICATION - to authenticate deletion requests
jwt = JWT(app, authenticate, identity)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class NewUser(Resource):
    """
    A class to represent a new user

    Methods
    -------
    post(self, username, email, password)
        Creates a new user object and stores it in the database.
        Returns a dictionary (JSON format) with the new user's username
    """

    def post(self, username, email, password):
        user = User(username, email, password)

        db.session.add(user)
        db.session.commit()

        return user.json()

class ExistingUser(Resource):
    """
    A class to represent an existing user

    Methods
    -------
    get(self, email)
        Reads/retrieves an existing user object from the database.

        Returns a dictionary (JSON format) with the user's username,
        email, date and time created and state (active/inactive).
        If user does not exist, returns {'name': None} and status code 404.

    delete(self, email)
        Deletes a user object if it exists in the database (Requires authentication)

        Returns a dictionary (JSON format) note stating 'delete success'.
    """

    def get(self, email):
        user = User.query.filter_by(email=email).first()
        date = dumps(user.created_at, default=json_serial)
        if user:
            return {'id':user.id,
                    'username':user.username,
                    'email':user.email,
                    'created_at':date,
                    'is_active':user.is_active}
        else:
            return {'name': None}, 404

    @jwt_required()# this request now reqires authentication
    def delete(self, email):
        user = User.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()
        return {'note':'delete success'}

class AllUsers(Resource):
    """
    A class to represent all users

    Methods
    -------
    get(self)
        Reads/retrieves all user objects from the database.

        Returns a list of dictionary objects (JSON format) with all usernames.
        If there are no users in the database, it returns {'users': None}
        and status code 404.
    """

    def get(self):
        users = User.query.all()
        if users:
            return [user.json() for user in users]
        else:
            return {'users': None}, 404

# CREATE ROUTES
api.add_resource(NewUser, '/user/<string:username>/<string:email>/<string:password>')
api.add_resource(ExistingUser, '/user/<string:email>')
api.add_resource(AllUsers, '/users')



# SET UP DB in terminal
# MAC & UNIX:
# export FLASK_APP=app.py
# WINDOWS:
# set FLASK_APP=app.py

# flask db init
# flask db migrate -m "first migration"
# flask db upgrade
# python app.py

# TESTING
# GET ALL
# curl http://127.0.0.1:5000/users

# GET 1
# curl http://127.0.0.1:5000/user/Chris

# POST
# curl -X POST http://127.0.0.1:5000/user/Sam/sam@email.com/sam123

# AUTHENTICATE user to get access token:
# curl -H "Content-Type: application/json" -X POST   -d '{"username":"Chris","password":"chris123"}' http://127.0.0.1:5000/auth
# -- this returns a token - copy including quotation marks

# then export the provided token (obviously use given token, not this example token)
# export ACCESS="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzkwNTU0NjIsImlhdCI6MTYzOTA1NTE2MiwibmJmIjoxNjM5MDU1MTYyLCJpZGVudGl0eSI6MX0.qOWnu5WUmXrbAv86AWDvCXebPbydEnNxWPuoWxP8AZI"

# then finally use this exported token in the delete request
# chris$ curl -H "Authorization: JWT $ACCESS" -X DELETE http://127.0.0.1:5000/user/sam@email.com
