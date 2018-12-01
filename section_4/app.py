from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

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
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda i: i['name'] == name, items), None) is not None:
            return {'message': 'An item called {} already exists.'.format(name)}, 400
        data = request.get_json()
        new_item = {'name': name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)