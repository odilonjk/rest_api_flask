import sqlite3
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True,
        help='This field cannot be left blank.'
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'name': row[1], 'price': row[2]}
        return None

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (NULL, ?, ?)'
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return {'item': item}, 200 
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, name):
        user = current_identity
        print('{} is trying to create a new item called {}.'.format(user.username, name))
        if self.find_by_name(name) is not None:
            return {'message': 'An item called {} already exists.'.format(name)}, 400
        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        
        try:
            self.insert(new_item)      
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return new_item, 201

    @jwt_required()
    def delete(self, name):
        if self.find_by_name(name) is None:
            return {'message': 'There is no item called {}.'.format(name)}, 404
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': '{} deleted.'.format(name)}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        item = self.find_by_name(name)
        if item is None:
            try:
                self.insert(new_item)      
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                self.update(new_item)
            except:
                return {'message': 'An error occurred updating the item.'}, 500
        return new_item


class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[1], 'price': row[2]})
        connection.close()
        return {'items': items}