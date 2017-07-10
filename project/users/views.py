from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
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
from project.users.models import User
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError



users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder = 'templates'
)

@user_blueprints.route('/', methods=[ "GET"])
def search():
    return render_template("users/search.html")


@user_blueprints.route('/results', methods=["GET"])
def results():


    # searching for foods
    search_dict = {
        "q": request.args.get('search-food').lower(), 
        "sort":"n", 
        "max": "10",
        "api_key": usda_key,
        "format": "json",
    }

    try:
        search_response = requests.get("https://api.nal.usda.gov/ndb/search/", params=search_dict)
        search = search_response.json()
        product_list = search['list']['item']
    except (json.decoder.JSONDecodeError, KeyError) as e:
        no_results = request.args.get('search-food').lower()
        return render_template("400.html", no_results=no_results)


    # grabbing all product names


    products = []
    for i in product_list:
        products.append(i['name'])

    # counter for product_obj
    prodlength = len(products)

    ndbno_list = []
    for i in product_list:
        ndbno_list.append(i['ndbno'])

    ingredients = []
    for i in ndbno_list:
        try:
            ingredients.append(ingredient_lookup(i)['report']['food']['ing']['desc'])
        except (json.decoder.JSONDecodeError, KeyError) as e:
            ingredients.append("No ingredients found")

    # combined = list(zip(products, ingredients))

    
    counter = 0
    product_obj = {}
    while prodlength > counter:
        for i in products:
            product_obj[i] = ingredients[counter]  
            counter = counter+1

    # list of all additives in DB
    additive_list = {}
    for i in get_additives():
        additive_list[i['name']] = i['code']

    return render_template("users/results.html", search=search, product_obj=product_obj, additive_list=additive_list, ingredients=ingredients)

def ingredient_lookup(ndbno):
    search_ndbno_dict = {
        "ndbno": ndbno,
        "type": "f",
        "api_key": usda_key,
        "format": "json",
    }
    search_ndbno_response = requests.get("https://api.nal.usda.gov/ndb/reports", params=search_ndbno_dict)
    search_ndbno = search_ndbno_response.json()
    return search_ndbno

def get_additives():
    response = requests.get("https://vx-e-additives.p.mashape.com/additives?locale=en&order=asc&sort=last_update",
      headers={
        "X-Mashape-Key": "xSEQIb1gTTmshMeAu6VHKTQwea6cp1vQLqsjsnv1Bgx0gMeyl6",
        "Accept": "application/json"
      }
    )

    return response.json()

def additive_function(code):
    response = requests.get("https://vx-e-additives.p.mashape.com/additives/951?locale=en",
      headers={
        "X-Mashape-Key": "xSEQIb1gTTmshMeAu6VHKTQwea6cp1vQLqsjsnv1Bgx0gMeyl6",
        "Accept": "application/json"
      }
    )

    return response.json()

def upc_lookup(upcode):
    response = requests.get("http://api.walmartlabs.com/v1/items?",
        headers={
            "apiKey": "qkwugbctetqe4t6yweybcdx9",
            "format": "json",
            "upc": upcode
        }
    )

    return response.json()   