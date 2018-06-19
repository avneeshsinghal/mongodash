from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret-key'
DB_NAME = 'users'

DATABASE = MongoClient()[DB_NAME]
USERS_COLLECTION = DATABASE.admin


DEBUG = True

# rename this file to mongo_config.py
