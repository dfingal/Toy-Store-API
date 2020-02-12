from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Toy(Resource):
    TABLE_NAME ='toys'

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="You know what to do!")

    @jwt_required()
    def get(self, name):
        toy = self.find_by_name(name)
        if toy:
            return toy
        return {'message': 'Toy not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'toy': {'name': row[0], 'price': row[1]}}

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An toy with name '{}' already exisits.".format(name)}

        data = Toy.parser.parse_args()

        toy = {'name': name, 'price': data['price']}

        try:
            Toy.insert(toy)
        except:
            return {"message": "An error occured inserting the toy."}

        return toy

    @classmethod
    def insert(cls, toy):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?,?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (toy['name'], toy['price']))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Toy deleted.'}

    @jwt_required()
    def put(self, name):
        data = Toy.parser.parse_args()
        toy = self.find_by_name(name)
        updated_toy = {'name': name, 'price': data['price']}
        if toy is None:
            try:
                Toy.insert(updated_toy)
            except:
                return {"message": "An error occured inserting the toy."}
        else:
            try:
                Toy.update(updated_toy)
            except:
                return {"message": "An error occured updating the toy."}
        return updated_toy

        @classmethod
        def update(cls, name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
            cursor.execute(query, (toy['price'], toy['name']))

            connection.commit()
            connection.close()


class ToyList(Resource):
    TABLE_NAME = 'toys'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        toys = []
        for row in result:
            toys.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'toys': toys}