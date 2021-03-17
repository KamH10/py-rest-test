import os

from flask import Flask, jsonify                # **NOTE**
from flask_restful import Api                   # **NOTE**
from flask_jwt import JWT, JWTError             # **NOTE** s07e04-added

from security import authenticate, identity     # **NOTE** s07e04-added
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister         # **NOTE** s07e04-added

app = Flask(__name__)               # **NOTE**

app.config['DEBUG'] = True          # **NOTE**

# **NOTE** In case of no 'DATABASE_URL' environment variable, 'sqlite:///data.db'
# will be used as default.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # s07e10-added
app.config['PROPAGATE_EXCEPTIONS'] = True               # s07e10-added

# **NOTE** secret_key is used to encode cookies (we won't be using)
app.secret_key = 'jose'     # s07e04-added

api = Api(app)              # **NOTE**

# **NOTE** VIP - likes up app, authenticate, and identity to
# enable us to call the /auth endpoint.
jwt = JWT(app, authenticate, identity)      # s07e04-added

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
api.add_resource(Store, '/store/<string:name>')

# **NOTE** [GET] http://127.0.0.1:5000/item/piano
api.add_resource(Item, '/item/<string:name>')

api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')     # **NOTE** s07e04-added

# **NOTE** s07e04-added - whenever a JWTError is raised inside our
# application, the auth_error() handler will be called
@app.errorhandler(JWTError)
def auth_error(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization header?'}), 401


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
if __name__ == '__main__':
    from db import db

    db.init_app(app)                    # **NOTE**

    if app.config['DEBUG']:             # **NOTE** In debug mode
        @app.before_first_request       # **NOTE** after the first request, the method won't run
        def create_tables():
            db.create_all()             # **NOTE** Flask-SQLAlchemy will create all tables

    app.run(port=5000)
