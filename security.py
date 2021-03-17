
# s07e04-created

from werkzeug.security import safe_str_cmp
from models.user import UserModel

# **NOTE** gets called when a user enters /auth end-point.
def authenticate(username, password):
    print("==> authenticate()")     # fDBG

    # **NOTE** if authentication successful, return the user, otherwise return None
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# **NOTE** VIP - gets called when we get a JWT token, saying that the
# user is already authenticated/logged in, and Flask-JWT verified
# their authorization header is correct.
# 'payload' is a dictionary with 'identity' key which is the user id.
def identity(payload):
    print("==> identity()")     # fDBG

    user_id = payload['identity']
    return UserModel.find_by_id(user_id)    # return a user object
