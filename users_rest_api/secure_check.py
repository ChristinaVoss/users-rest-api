from users_rest_api.model import User

def authenticate(username, password):
    """
    Function used by jwt to authenticate users.
    Checks if user exists and password matches
    """
    user = User.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        return user

def identity(payload):
    """ Function used by jwt to generate token (secret key). """
    user_id = payload['identity']
    return user_id
