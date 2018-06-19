from app import app, lm
from flask import request, redirect, render_template, url_for

from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm
from .forms import RegisterForm
from .user import User
import datetime
from app import sock
from app.helpfunc import *
from app.oop import pydb_conn, coll1, connect_config,jsonify

from datetime import timedelta
from flask import session

import json


@app.before_request
def make_session_permanent():
    """
    make session for 24 Hr
    :return:
    """
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1440)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('write'))

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])  # * only POST
def login():
    if current_user.is_authenticated:  # if user already logged then --> /write
        return redirect(url_for('write'))

    form = LoginForm()  # user LoginForm

    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one(
            {
                "user_name": form.username.data
            }
        )

        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['user_name'])
            login_user(user_obj)
            return redirect(url_for("write"))

        else:
            error = connect_config['STRINGS']['password_error']
            print(error)
            return render_template("login.html", form=form, title="login", error=error)

    return render_template('login.html', title='login', form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    ip = sock.get_ip_address()
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"user_name": form.username.data})

        if user is None:
            register_username = form.username.data
            register_password = form.password.data
            current_date_time = datetime.datetime.now().isoformat()  # read date-time in iso format
            app.config['USERS_COLLECTION'].insert(
                {
                    "user_name": register_username,
                    "password": register_password,
                    "added_by": current_user.username,
                    "added_time": current_date_time
                }
            )  # * read hashing for passwords
            return redirect(url_for("write"))

        else:
            error = connect_config['STRINGS']['user_already_exist']
            return render_template("register.html", form=form, title="login", error=error)

    return render_template('register.html', title='login', form=form)


@app.route('/logout')  # if logout then --> login.html
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"user_name": username})
    if not u:
        return None
    return User(u['user_name'])


@app.route('/write')
@login_required
def write():
    ip = sock.get_ip_address()
    return render_template('textbox.html', ip=ip)  # send host to textbox.html


@app.route("/get_all_tables", methods=['GET'])
@login_required
def get_collections():
    """
    :return: list of collections in current db
    """
    collection = coll1.collection_names(include_system_collections=False)
    return jsonify(collection)


@app.route("/get_tbl1_keys", methods=['GET'])
@login_required
def get_tbl1_keys():
    """
    :return: list of keys in tbl1
    """
    keyList = []
    table1 = request.args.get("tbl1")
    try:
        keyList = get_table_keys(table1)
    except:
        print(Exception)

    return jsonify(keyList)


@app.route("/get_tbl2_keys", methods=['GET'])
@login_required
def get_tbl2_keys():
    """
    :return: list of keys tbl2
    """
    keyList = []
    table2 = request.args.get("tbl2")
    try:
        keyList = get_table_keys(table2)
    except:
        print(Exception)

    return jsonify(keyList)


@app.route("/common_keys", methods=['GET'])
@login_required
def json_common_keys():
    """
    :return: list of keys common in tbl1 & 2
    """
    table1 = request.args.get("tbl1")
    table2 = request.args.get("tbl2")
    keyList = common_keys(table1, table2)

    return jsonify(keyList)


@app.route("/table", methods=['GET'])
def table_call():
    """

    :return: JSON string with optimal answers to query, and relation if exists
    """

    tbname = request.args
    key1 = request.args.get("key1")
    key2 = request.args.get("key2")
    action1 = request.args.get("action1")
    action2 = request.args.get("action2")
    value1 = request.args.get("value1")
    value2 = request.args.get("value2")
    final1 = ""

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

    # if table2 is stated
    if table1 == None and table2 != None:
        commonlist = get_table_keys(table2)

        class Table2(db_eng.DynamicDocument):
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
        final1 = final
        if (key2 != None and value2 != None and action2 == None):
            kwargs = {
                key2: ifInt(value2)
            }

            temp = Table2.objects(**kwargs)
            final1 = jsonify(json.loads(temp.to_json()))

        if (key2 != None and value2 != None and action2 != None):
            keyAction = key2 + "__" + action2
            kwargs = {
                keyAction: ifInt(value2)
            }
            temp = Table2.objects(**kwargs)
            final1 = jsonify(json.loads(temp.to_json()))

    # if table1 is stated
    if table1 != None and table2 == None:
        commonlist = get_table_keys(table1)

        class Table1(db_eng.DynamicDocument):
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
        final1 = final

        if (key1 != None and value1 != None and action1 == None):
            kwargs = {
                key1: ifInt(value1)
            }
            temp = Table1.objects(**kwargs)
            final1 = jsonify(json.loads(temp.to_json()))

        if (key1 != None and value1 != None and action1 != None):
            keyAction = key1 + "__" + action1

            kwargs = {
                keyAction: ifInt(value1)
            }
            #temp = Table1.objects(shuttl_credit__gte=234)
            temp = Table1.objects(**kwargs)
            final1 = jsonify(json.loads(temp.to_json()))
            print(final1)

    # if both tables are stated
    if table1 != None and table2 != None:
        commonlist = common_keys(table1, table2)

        class Table1(db_eng.DynamicDocument):
            meta = {
                'collection': table1}

        class Table2(db_eng.DynamicDocument):
            meta = {
                'collection': table2
            }

        class temp(db_eng.DynamicDocument):
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

        if (
                key1 == None and value1 == None and action1 == None and key2 == None and value2 == None and action2 == None):
            final1 = final

        if (
                key1 != None and value1 != None and action1 == None and key2 == None and value2 == None and action2 == None):
            kwargs = {
                key1: ifInt(value1)
            }

            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            to_json_str = temp.objects(**kwargs).to_json()
            final1 = jsonify(json.loads(to_json_str))

        if (
                key1 != None and value1 != None and action1 != None and key2 == None and value2 == None and action2 == None):
            keyAction = key1 + "__" + action1
            kwargs = {
                keyAction: ifInt(value1)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)
            to_json_str=temp.objects(**kwargs).to_json()
            final1 =jsonify(json.loads(to_json_str))

        if (
                key2 != None and value2 != None and action2 == None and key1 == None and value1 == None and action1 == None):
            key2 = "relation__" + key2
            kwargs = {
                key2: ifInt(value2)
            }

            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            to_json_str = temp.objects(**kwargs).to_json()
            final1 = jsonify(json.loads(to_json_str))

        if (
                key2 != None and value2 != None and action2 != None and key1 == None and value1 == None and action1 == None):
            key2 = "relation__" + key2
            keyAction = key2 + "__" + action2
            kwargs = {
                keyAction: ifInt(value2)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            to_json_str = temp.objects(**kwargs).to_json()
            final1 = jsonify(json.loads(to_json_str))

        if (
                key2 != None and value2 != None and action2 == None and key1 != None and value1 != None and action1 == None):
            key2 = "relation__" + key2
            kwargs = {
                key1: ifInt(value1),
                key2: ifInt(value2)
            }

            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            to_json_str = temp.objects(**kwargs).to_json()
            final1 = jsonify(json.loads(to_json_str))

        if (
                key2 != None and value2 != None and action2 != None and key1 != None and value1 != None and action1 == None):

            key2 = "relation__" + key2
            keyAction2 = key2 + "__" + action2
            kwargs = {
                key1: ifInt(value1),
                keyAction2: ifInt(value2)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            to_json_str = temp.objects(**kwargs).to_json()
            final1 = jsonify(json.loads(to_json_str))

        if (
                key2 != None and value2 != None and action2 == None and key1 != None and value1 != None and action1 != None):
            keyAction = key1 + "__" + action1
            key2 = "relation__" + key2
            kwargs = {
                keyAction: ifInt(value1),
                key2: ifInt(value2)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            to_json_str = temp.objects(**kwargs).to_json()
            final1 = jsonify(json.loads(to_json_str))

        if (
                key2 != None and value2 != None and action2 != None and key1 != None and value1 != None and action1 != None):
            keyAction = key1 + "__" + action1
            key2 = "relation__" + key2
            keyAction2 = key2 + "__" + action2
            kwargs = {
                keyAction: ifInt(value1),
                keyAction2: ifInt(value2)
            }
            for item in json.loads(final):
                tem = temp(**item)
                tem.save(force_insert=True)

            to_json_str = temp.objects(**kwargs).to_json()
            final1 = jsonify(json.loads(to_json_str))

        temp.objects().delete()

        """item= json.loads(final)[0]
        tem = temp(**item)
        final=jsonify(tem)"""

        """tem.save(force_insert=True)
        final1=tem.objects()
        print (final1)
        #final=jsonify(final1)"""

    return final1
