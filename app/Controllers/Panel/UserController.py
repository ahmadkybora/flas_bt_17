import json
from flask import jsonify, render_template, redirect, url_for, request, abort
import requests
from app.Models.User import User

def index():
    users = User.query.all()
    users = json.dumps(users)
    return jsonify(users)

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