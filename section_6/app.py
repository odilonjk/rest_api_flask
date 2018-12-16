from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)

# JWT
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'my_secret'

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(port=5000, debug=True)
