from unicodedata import name
from flask import Flask, jsonify
from markupsafe import escape
from elasticsearch import Elasticsearch
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta



elastic = Elasticsearch(hosts=["192.168.136.34"])


# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)



@app.route('/', methods=['GET']) # Define http method
def home():
    return 'It still lives!'

@app.route('/users/<id>')
def get_user_profile(id):
    # Get a user profile
    results = elastic.search(index="users", doc_type="_doc", body={"query": {"match":{"_id": id}}}, size=1)
    userData = []
    for i in results['hits'].get("hits"):
        dateString = i['_source']["dob"]
        dob = datetime.strptime(dateString,'%Y-%m-%d')

        data = {
            "Name": i['_source']["name"],
            "E-mail": i['_source']["email"],
            "Gender": i['_source']["gender"],
            "Country": i['_source']["country"],
            "Age": str(relativedelta(datetime.today(),dob).years)
        }
        userData.append(json.dumps(data))

    return str(userData)

# http://192.168.136.61:5000/history/41c6e6d7-b78c-413f-adb3-0567aa4996ef
    
@app.route('/history/<userid>')
def get_history(userid):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {"match":{"user": userid}}})

    userHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "song": i['_source']["song"],
            "timestamp": i['_source']["timestamp"]
        }
        userHistory.append(json.dumps(data))
    return str(userHistory)
    



@app.route('/topsongs')
def get_topsongs():
    # Get top 10 songs started the last week
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
    "bool": {
      "filter":
        { "range": { "timestamp": { "gte": "now-7d/d", "lt": "now/d" }}}}}, "aggs": {"songs": {"terms": {"field": "song", "size": 10}}}})
    
    topsongs = []
    for i in results['aggregations']['songs']['buckets']:
        data = {
            "song": i["key"],
            "plays": i["doc_count"]
        }
        topsongs.append(json.dumps(data))


    return str(topsongs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

