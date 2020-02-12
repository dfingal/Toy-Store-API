from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Pet(Resource):
    TABLE_NAME ='pets'

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="You know what to do!")

    @jwt_required()
    def get(self, name):
        pet = self.find_by_name(name)
        if pet:
            return pet
        return {'message': 'Pet not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'pet': {'pet': row[0], 'price': row[1]}}

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An pet with name '{}' already exisits.".format(name)}

        data = Pet.parser.parse_args()

        pet = {'name': name, 'price': data['price']}

        try:
            Pet.insert(pet)
        except:
            return {"message": "An error occured inserting the pet."}

        return pet

    @classmethod
    def insert(cls, pet):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?,?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (pet['name'], pet['price']))

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

        return {'message': 'Pet deleted.'}

    @jwt_required()
    def put(self, name):
        data = Pet.parser.parse_args()
        pet = self.find_by_name(name)
        updated_pet = {'name': name, 'price': data['price']}
        if pet is None:
            try:
                Pet.insert(updated_pet)
            except:
                return {"message": "An error occured inserting the pet."}
        else:
            try:
                Pet.update(updated_pet)
            except:
                return {"message": "An error occured updating the pet."}
        return updated_pet

        @classmethod
        def update(cls, name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
            cursor.execute(query, (pet['price'], pet['name']))

            connection.commit()
            connection.close()


class PetList(Resource):
    TABLE_NAME = 'pets'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        pets = []
        for row in result:
            pets.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'pets': pets}