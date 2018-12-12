from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'my_secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = [
    {
        'name': 'Pen',
        'price': 1.99
    },
    {
        'name': 'Chair',
        'price': 65.00
    }
]


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True,
        help='This field cannot be left blank.'
    )

    def get_item(self, name):
        return next(filter(lambda i: i['name'] == name, items), None)

    @jwt_required()
    def get(self, name):
        item = Item.get_item(self, name)
        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if Item.get_item(self, name) is not None:
            return {'message': 'An item called {} already exists.'.format(name)}, 400
        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201

    @jwt_required()
    def delete(self, name):
        global items
        if Item.get_item(self, name) is None:
            return {'message': 'There is no item called {}.'.format(name)}, 404
        items = [i for i in items if i['name'] != name]
        return {'message': '{} deleted.'.format(name)}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.get_item(self, name)
        if item is None:
            new_item = {'name': name, 'price': data['price']}
            items.append(new_item)
            return new_item, 201
        item.update(data)
        return item


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)