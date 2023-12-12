from flask import Flask
from flask_pymongo import PyMongo
from injector import inject

from data.model.user import User
from data.repository.user_repository import UserRepository

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/StiluqDB'
mongo = PyMongo(app)


class UserRepositoryImpl(UserRepository):

    @inject
    def __init__(self):
        self.mongo = mongo

    def find_user(self, user_id):
        return self.mongo.db.users.find_one({'_id': user_id})

    def save(self, user):

        if isinstance(user, dict):
            user_id = user.get('_id')
            update_data = {'$set': {'is_logged_in': user.get('is_logged_in')}}
            self.mongo.db.users.update_one({'_id': user_id}, update_data)
        elif isinstance(user, User):
            user_data = {
                'email': user.email,
                'password': user.password,
                'is_logged_in': user.is_logged_in,
            }
            return self.mongo.db.users.insert_one(user_data)

        else:
            raise ValueError("Unsupported user type")

    def find_by_email(self, email):
        return self.mongo.db.users.find_one({'email': email})

    def delete_all(self):
        self.mongo.db.users.delete_many({})
