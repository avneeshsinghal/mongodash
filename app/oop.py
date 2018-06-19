import os
import sys
import flask
import json
from flask import request
from flask import jsonify
from flask import render_template
import pymongo
import configparser
from helpfunc import db
from flask_cors import CORS


sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

connect_config = configparser.ConfigParser()
try:
    connect_config.sections()
    connect_config.read('config.ini')
    getdb = connect_config['MONGO_DB']['DB']
except:
    print("check config file and db name")

app = flask.Flask(__name__)
app.config.from_object(__name__)
CORS(app)


app.config['MONGODB_SETTINGS'] = {'DB': 'sanjay'}
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

pydb_conn=pymongo.MongoClient()
coll1=pydb_conn['sanjay']

db.init_app(app)

from helpfunc import *

"""@app.route("/")
def index():
    return render_template("textbox.html")"""

@app.route("/get_all_tables", methods=['GET'])

def get_collections():
    """

    :return: list of collections in current db
    """
    collection = coll1.collection_names(include_system_collections=False)
    return jsonify(collection)


@app.route("/get_tbl1_keys", methods=['GET'])

def get_tbl1_keys():
    """

    :return: list of keys in tbl1
    """
    table1 = request.args.get("tbl1")

    keyList = get_table_keys(table1)

    return jsonify(keyList)


@app.route("/get_tbl2_keys", methods=['GET'])
def get_tbl2_keys():
    """

    :return: list of keys tbl2
    """

    table2 = request.args.get("tbl2")

    keyList = get_table_keys(table2)

    return jsonify(keyList)

@app.route("/common_keys", methods=['GET'])
def json_common_keys():
    """

    :return: list of keys common in tbl1 & 2
    """
    table1 = request.args.get("tbl1")
    table2 = request.args.get("tbl2")
    keyList=common_keys(table1,table2)


    return jsonify(keyList)




@app.route("/table", methods=['GET'])

def table_call():
    """

    :return: JSON string with optimal answers to query, and relation if exists
    """

    tbname = request.args
    key1 = request.args.get("key1")
    key2 = request.args.get("key2")
    action1=request.args.get("action1")
    action2=request.args.get("action2")
    value1=request.args.get("value1")
    value2=request.args.get("value2")
    final1=""

    list1 = list(tbname.keys())
    param = {}

    final = {}

    for itr in range(len(list1)):
        param[list1[itr]] = ifInt(tbname[list1[itr]])
    print(param)





    if key1 == "":
        key1 = key2
    if key2 == "":
        key2 = key1

    table1 = request.args.get("tbl1")
    table2 = request.args.get("tbl2")

    if key1 == None and value1 == None and action1 == None and key2 == None and value2 == None and action2 == None and table1 == None and table2 == None:

        final = []
        final1 = jsonify(final)

#if table2 is stated
    if table1==None and table2!=None:
        commonlist=get_table_keys(table2)

        class Table2(db.DynamicDocument):
            meta = {
                'collection': table2
            }

        cursor = Table2.objects.aggregate(*[
            {
                '$lookup': {
                    'from': Table2._get_collection_name(),
                    'localField': commonlist[0],
                    'foreignField': commonlist[0],
                    'as': 'relation'
                }
            },
            {'$unwind': '$relation'}
        ])

        final = JSONEncoder().encode([c for c in cursor])
        final1=final
        if (key2 != None and value2 != None and action2==None):
            kwargs={
                key2 : ifInt(value2)
            }

            temp = Table2.objects(**kwargs)
            final1= jsonify(temp)

        if (key2 != None and value2 != None and action2!=None):
            keyAction=key2+"__"+action2
            kwargs = {
                keyAction : ifInt(value2)
            }
            temp=Table2.objects(**kwargs)
            final1=jsonify(temp)
#if table1 is stated
    if table1!=None and table2==None:
        commonlist=get_table_keys(table1)

        class Table1(db.DynamicDocument):
            meta = {
                'collection': table1
            }

        cursor = Table1.objects.aggregate(*[
            {
                '$lookup': {
                    'from': Table1._get_collection_name(),
                    'localField': commonlist[0],
                    'foreignField': commonlist[0],
                    'as': 'relation'
                }
            },
            {'$unwind': '$relation'}
        ])
        final = JSONEncoder().encode([c for c in cursor])
        final1=final

        if (key1 != None and value1 != None and action1==None):
            kwargs={
                key1 : ifInt(value1)
            }

            temp = Table1.objects(**kwargs)
            final1 = jsonify(temp)

        if (key1 != None and value1 != None and action1!=None):
            keyAction=key1+"__"+action1
            kwargs = {
                keyAction : ifInt(value1)
            }
            temp=Table1.objects(**kwargs)
            final1=jsonify(temp)




#if both tables are stated
    if table1!=None and table2!=None:
        commonlist=common_keys(table1,table2)

        class Table1(db.DynamicDocument):
            meta = {
                'collection': table1     }

        class Table2(db.DynamicDocument):
            meta = {
                'collection': table2
            }

        class temp(db.DynamicDocument):
            meta = {
                'collection': 'temp'
            }

        cursor = Table1.objects.aggregate(*[
            {
                '$lookup': {
                    'from': Table2._get_collection_name(),
                    'localField': commonlist[0],
                    'foreignField': commonlist[0],
                    'as': 'relation'
                }
            },
            {'$unwind': '$relation'}
        ])

        final = JSONEncoder().encode([c for c in cursor])

        if (key1 == None and value1 == None and action1 == None and key2 == None and value2 == None and action2 == None):
            final1=final

        if (key1 != None and value1 != None and action1 == None and key2 == None and value2 == None and action2 == None):
            kwargs={
                key1 : ifInt(value1)
            }

            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            final1 = jsonify(temp.objects(**kwargs))

        if (key1 != None and value1 != None and action1!=None and key2 == None and value2 == None and action2==None):
            keyAction=key1+"__"+action1
            kwargs = {
                keyAction : ifInt(value1)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            final1 = jsonify(temp.objects(**kwargs))

        if (key2 != None and value2 != None and action2==None and key1 == None and value1 == None and action1==None):
            key2="relation__"+key2
            kwargs={
                key2 : ifInt(value2)
            }

            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            final1 = jsonify(temp.objects(**kwargs))

        if (key2 != None and value2 != None and action2 != None and key1 == None and value1 == None and action1==None):
            key2 = "relation__" + key2
            keyAction=key2+"__"+action2
            kwargs = {
                keyAction : ifInt(value2)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            final1 = jsonify(temp.objects(**kwargs))

        if (key2 != None and value2 != None and action2==None and key1 != None and value1 != None and action1==None):
            key2="relation__"+key2
            kwargs={
                key1 : ifInt(value1),
                key2 : ifInt(value2)
            }

            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            final1 = jsonify(temp.objects(**kwargs))

        if (key2 != None and value2 != None and action2 != None and key1 != None and value1 != None and action1 == None):

            key2 = "relation__" + key2
            keyAction2=key2+"__"+action2
            kwargs = {
                key1 : ifInt(value1),
                keyAction2 : ifInt(value2)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            final1 = jsonify(temp.objects(**kwargs))

        if ( key2 != None and value2 != None and action2 == None and key1 != None and value1 != None and action1 != None):
            keyAction = key1 + "__" + action1
            key2 = "relation__" + key2
            kwargs = {
                keyAction: ifInt(value1),
                key2: ifInt(value2)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            final1 = jsonify(temp.objects(**kwargs))


        if (key2 != None and value2 != None and action2 != None and key1 != None and value1 != None and action1 != None):
            keyAction = key1 + "__" + action1
            key2 = "relation__" + key2
            keyAction2=key2+"__"+action2
            kwargs = {
                keyAction : ifInt(value1),
                keyAction2 : ifInt(value2)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            final1 = jsonify(temp.objects(**kwargs))




        temp.objects().delete()

        """item= json.loads(final)[0]
        tem = temp(**item)
        final=jsonify(tem)"""

        """tem.save(force_insert=True)
        final1=tem.objects()
        print (final1)
        #final=jsonify(final1)"""


    return final1


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=4000)

