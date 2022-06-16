import json
from json import JSONEncoder
from flask import jsonify, render_template, redirect, url_for, request, abort
import requests
from app.Models.User import User, user_schema, users_schema

def index():
    # return 'a'
    # users = User.query.all()
    # return str(users)
    # users = JSONEncoder(users)
    # users = User()
    # users.first_name = 'a'
    # users.last_name = 'b'
    # users.username = 'c'
    # users.email = 'd'

    # users = User('aa', 'ba', 'ca', 'da')
    # users = json.dumps(users.__dict__)
    # return(users)
    # return jsonify(users)
    users = User.query.all()
    results = users_schema.dump(users)
    return jsonify(results)

def store():
    requests.form['username']
    request.form['pssword'];
    return 

def show(userId):
    return "ok"

def update(userId):
    return "ok"

def delete(userId):
    return "ok"