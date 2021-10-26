from unicodedata import name
from flask import Flask, jsonify
from markupsafe import escape
from elasticsearch import Elasticsearch
import json


elastic = Elasticsearch(hosts=["192.168.136.34"])


# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)



@app.route('/', methods=['GET']) # Define http method
def home():
    return 'It still lives!'

@app.route('/users/<username>')
def get_user_profile(username):
    # Get a user profile
    results = elastic.search(index="users", doc_type="_doc", body={"query": {"match":{"name": username}}})
    return results['hits']

    
    
@app.route('/history/<username>')
def get_history(username):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {"match":{"user": username}}})
    '''
    res = ""
    x = 0
    for i in results['hits'].get("hits"):
        res = res + "{ \"song\" : " + i['_source']["song"] + ",\n \"plays\" :"  + i['_source']["timestamp"]] + "\n}\n"
        x = x+1
    '''
    userHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "song": i['_source']["song"],
            "timestamp": i['_source']["timestamp"]
        }
        userHistory.append(json.dumps(data))
    return str(userHistory)
    


'''

'''
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


    #name = ""
    
    #for i in results['aggregations']['songs']['buckets']:
        #name = name + "{ \"song\" : " + i["key"] + ",\n \"plays\" :" + str(i["doc_count"]) + "\n}\n"
    


    #return results['aggregations']['songs']['buckets'][0]['key']
    #return "{ \"song\" : " + str(results['aggregations']['songs']['buckets'][0]["doc_count"]) + ",\n \"plays\" :" + "\n}"
    return str(topsongs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

