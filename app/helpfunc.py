from flask_mongoengine import MongoEngine
from bson.json_util import ObjectId
import json

db=MongoEngine()


def ifInt(parobj):
    """
    :param parobj: This is the parameter object.
    :return: Returns the same object if string, else integer.
    """
    try:
        parsed=int(parobj)
        return parsed
    except:
        return parobj


def get_table_keys(table_name):


    """

    :param table_name(string):
    :return: returns list of tables
    """

    class Table1(db.DynamicDocument):
        meta = {
            'collection': table_name
        }

    data=Table1.objects.all()[0]
    listKeys=list()
    for key in data:
        listKeys.append(key)

    listKeys.remove("id")

    return listKeys



def common_keys(table1,table2):
    list1=set(get_table_keys(table1))
    list2=set(get_table_keys(table2))
    keyList=list(list2.intersection(list1))
    keyList.append("id")

    return keyList

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        """
        :param o: CommandCursor from mongoDB
        :return: JSON encoded string
        """
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)