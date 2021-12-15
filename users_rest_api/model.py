from users_rest_api import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """
    A class to represent a user

    Attributes
    ----------
    id : int
        the primary key of the user (automatically created)
    username : str
        the username of the user
    email : str
        the email address of the user
    password_hash : str
        a hashed version of the password
    created_at : datetime
        the date and time that the user object is created, in greenwhich mean time
    is_active : boolean
        the state of the user (defualt is True)

    Methods
    -------
    check_password(self, password)
        Checks the given password agains the stored hashed pasword
        Returns a boolean value (True id password matches)

    json(self)
        Returns the username in a dictionary format (JSON friendly)
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    is_active = db.Column(db.Boolean(), default=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {'username':self.username}

db.create_all()
db.session.commit()
