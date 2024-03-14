from flask import Flask, request, jsonify
from db import database

app = Flask(__name__)


@app.route("/set_user", methods=['POST'])
def set_user():
    db = database()
    data = request.get_json()
    name_first = data.get('name_first')
    name_last = data.get('name_last')
    user_name = data.get('username')
    password = data.get('password')
    db.insert_user(user_name, password, name_first, name_last)
    db.close()


@app.route("/set_interests", methods=['POST'])
def set_interests():
    db = database()
    data = request.get_json()
    db.insert_interests(data)
    db.close()


@app.route("/set_friend", methods=['POST'])
def set_friend():
    db = database()
    data = request.get_json()
    user_name1 = data.get('user_name1')
    user_name2 = data.get('user_name2')
    db.insert_friendship_usernames(user_name1, user_name2)
    db.close()


@app.route("/get_recs", methods=['GET'])
def get_recs():
    db = database()
    data = request.get_json()
    username = data.get('username')
    return db.get_recomendations(username)


@app.route("/get_leaderboard", methods=['POST'])
def get_leaderboard():
    db = database()
    data = request.get_json()
    username = data.get('username')
    result = db.get_leaderboard(username)
    # print(result)
    return result


@app.route("/login", methods=['GET'])
def login():
    db = database()
    data = request.get_json()
    un = data.get('username')
    pw = data.get('password')
    result = db.check_login(un, pw)
    db.close()
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
