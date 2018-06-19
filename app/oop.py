import os
import sys
import flask
import json
from flask import request
from flask import jsonify
from flask import render_template
import pymongo
import configparser

from app.helpfunc import db_eng
from flask_cors import CORS


getdb='sanjay' #* sanjay kya hai?
connect_config = configparser.ConfigParser()
try:
    connect_config.sections()
    connect_config.read('config.ini')
    getdb = connect_config['MONGO_DB']['DB']

except Exception as e:
    print(e)

app = flask.Flask(__name__)
app.config.from_object(__name__)
CORS(app)


app.config['MONGODB_SETTINGS'] = {'DB': getdb}
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

pydb_conn=pymongo.MongoClient()
coll1=pydb_conn['sanjay'] #* coll1 kya hai be?!

db_eng.init_app(app)

from app.helpfunc import *

"""@app.route("/")
def index():
    return render_template("textbox.html")"""





if __name__ == "__main__":

    app.run(host="0.0.0.0", port=4000)


