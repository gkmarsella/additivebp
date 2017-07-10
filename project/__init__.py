from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_modus import Modus
from flask_login import LoginManager
import sys
import os
import requests
import urllib.request
import json
# for logging in
from flask_login import LoginManager
# from project import db, bcrypt
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
api = Modus(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


usda_key = app.config['USDA_KEY'] = os.environ.get('USDA_KEY')