from unicodedata import name
from flask import Flask, jsonify
from flask.json import dumps
from markupsafe import escape
from elasticsearch import Elasticsearch
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


elastic = Elasticsearch(host="t05-elasticsearch")

# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)


@app.route('/', methods=['GET'])  # Define http method
def home():
    return 'Data Collection API!'

@app.route('/users')
def getUsers():
    results = elastic.search(index="users", body={"query": {"match_all": {}}})

    data = results['hits'].get("hits")
       
    return json.dumps(data)


@app.route('/users/<userid>')
def get_user_profile(userid):
    # Get a user profile
    results = elastic.get(index="users",  id=userid)
    
    dateString = results['_source']["dob"]
    dob = datetime.strptime(dateString, '%Y-%m-%d')

    data = {
            "Name": results['_source']["name"],
            "E-mail": results['_source']["email"],
            "Gender": results['_source']["gender"],
            "Country": results['_source']["country"],
            "Age": str(relativedelta(datetime.today(), dob).years)
        }

    return json.dumps(data)


# http://192.168.136.61:5000/history/41c6e6d7-b78c-413f-adb3-0567aa4996ef

@app.route('/users/<id>/songs')
def get_history(id):
    results = elastic.search(index="songstarted", doc_type="_doc", body={
                             "query": {"match": {"user": id}}})

    userHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "song": i['_source']["song"],
            "timestamp": i['_source']["timestamp"]
        }
        userHistory.append(data)
    return json.dumps(userHistory)


@app.route('/users/<id>/searches')
def get_search_history(id):
    results = elastic.search(index="searchqueries", doc_type="_doc", body={
                             "query": {"match": {"user": id}}})

    userSearchHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "searchterm": i['_source']["searchterm"],
            "timestamp": i['_source']["timestamp"]
        }
        userSearchHistory.append(data)
    return json.dumps(userSearchHistory)


@app.route('/users/<user>/songs/<song>/amount_played')
def amount_song_played_by_user(user, song):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"user": user}},
                {"match": {"song._id.keyword": song}}    
                ]
        }
    }
    }
    )
    x = results['hits'].get("total").get("value")
    plays = {
        "plays": x
    }

    return json.dumps(plays)


@app.route('/users/<user>/artists/<artist>/amount_played')
def amount_artist_played_by_user(user, artist):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"user": user}},
                {"match": {"song.artist.keyword": artist}}]}}})
    x = results['hits'].get("total").get("value")
    plays = {
        "plays": x
    }

    return json.dumps(plays)


@app.route('/songs/<id>/amount_played')
def amount_song_played(id):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"song._id.keyword": id}}]}}})
    x = results['hits'].get("total").get("value")
    plays = {
        "plays": x
    }

    return json.dumps(plays)


@app.route('/artists/<id>/amount_played')
def artist_amount_played(id):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"song.artist.keyword": id}}]}}})
    x = results['hits'].get("total").get("value")
    plays = {
        "plays": x
    }

    return json.dumps(plays)


@app.route('/songs/top')
def get_top_songs():
    # Get top 10 songs started the last week
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "filter":
                {"range": {"timestamp": {"gte": "now-7d/d", "lt": "now/d"}}}}},
        "aggs": {"songs": {"terms": {"field": "song.title.keyword", "size": 10}}}})

    topsongs = []
    for i in results['aggregations']['songs']['buckets']:
        data = {
            "song": i["key"],
            "plays": i["doc_count"]
        }
        topsongs.append(data)

    return json.dumps(topsongs)


@app.route('/artists/top')
def get_top_artists():
    # Get top 10 artists the last week
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "filter":
                {"range": {"timestamp": {"gte": "now-7d/d", "lt": "now/d"}}}}},
        "aggs": {"artists": {"terms": {"field": "song.artist.keyword", "size": 10}}}})

    topartists = []
    for i in results['aggregations']['artists']['buckets']:
        data = {
            "artist": i["key"],
            "plays": i["doc_count"]
        }
        topartists.append(data)

    return json.dumps(topartists)


@app.route('/users/<id>/artists/top')
def get_top_artist_for_user(id):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": id
                }}
            ]
        }
    },
        "aggs": {"artists": {"terms": {"field": "song.artist.keyword"}}}})
    topartists = []
    for i in results['aggregations']['artists']['buckets']:
        data = {
            "artist": i["key"],
            "plays": i["doc_count"]
        }
        topartists.append(data)

    return json.dumps(topartists)


@app.route('/users/<id>/songs/top')
def get_top_songs_for_user(id):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": id
                }}
            ]
        }
    },
        "aggs": {"artists": {"terms": {"field": "song.title.keyword"}}}})
    topartists = []
    for i in results['aggregations']['artists']['buckets']:
        data = {
            "song": i["key"],
            "plays": i["doc_count"]
        }
        topartists.append(data)

    return json.dumps(topartists)


@app.route('/users/<id>/genres/top')
def get_top_genres_for_user(id):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": id
                }}
            ]
        }
    },
        "aggs": {"artists": {"terms": {"field": "song.genre.keyword"}}}})
    topartists = []
    for i in results['aggregations']['artists']['buckets']:
        data = {
            "genre": i["key"],
            "plays": i["doc_count"]
        }
        topartists.append(data)

    return json.dumps(topartists)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
