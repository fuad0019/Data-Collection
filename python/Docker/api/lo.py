from unicodedata import name
from flask import Flask, jsonify
from flask.json import dumps
from markupsafe import escape
from elasticsearch import Elasticsearch
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
  

users = []
for x in range(0,2):

    data = {
            "Name": "Fuad Hassan Farah",
            "E-mail": "fuad@gmail.com",
            "Gender": "Male",
            "Country": "Somalia",
            "Age": 23
        }
    users.append(data)
print(json.dumps(users))