from config import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

SECRET_KEY = os.urandom(22)
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

app.config['SECRET_KEY'] = SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://andreakybora:09392141724abc@localhost/flask'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ahmadkybora:09392141724abc@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)