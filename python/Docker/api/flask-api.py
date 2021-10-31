from unicodedata import name
from flask import Flask, jsonify
from markupsafe import escape
from elasticsearch import Elasticsearch
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta



elastic = Elasticsearch(host = "t05-elasticsearch")

# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)


@app.route('/', methods=['GET'])  # Define http method
def home():
    return 'Data Collection API!'


@app.route('/users/<id>')
def get_user_profile(id):
    # Get a user profile
    results = elastic.search(index="users", doc_type="_doc", body={"query": {"match": {"_id": id}}}, size=1)
    userData = []
    for i in results['hits'].get("hits"):
        dateString = i['_source']["dob"]
        dob = datetime.strptime(dateString, '%Y-%m-%d')

        data = {
            "Name": i['_source']["name"],
            "E-mail": i['_source']["email"],
            "Gender": i['_source']["gender"],
            "Country": i['_source']["country"],
            "Age": str(relativedelta(datetime.today(), dob).years)
        }
        userData.append(json.dumps(data))

    return str(userData)


# http://192.168.136.61:5000/history/41c6e6d7-b78c-413f-adb3-0567aa4996ef

@app.route('/history/<userid>')
def get_history(userid):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {"match": {"user": userid}}})

    userHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "song": i['_source']["song"],
            "timestamp": i['_source']["timestamp"]
        }
        userHistory.append(json.dumps(data))
    return str(userHistory)


@app.route('/searchhistory/<userid>')
def get_search_history(userid):
    results = elastic.search(index="search", doc_type="_doc", body={"query": {"match": {"user": userid}}})

    userSearchHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "searchterm": i['_source']["searchterm"],
            "timestamp": i['_source']["timestamp"]
        }
        userSearchHistory.append(json.dumps(data))
    return str(userSearchHistory)


@app.route('/amountSongPlayedBy/<user>/<song>')
def amount_song_played_by_user(user, song):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"user": user}},
                {"match": {"song.title.keyword": song}}]}}})
    x = results['hits'].get("total").get("value")
    amountPlays = []
    plays = {
        "plays": x
    }
    amountPlays.append(json.dumps(plays))

    return str(amountPlays)


@app.route('/amountArtistPlayedBy/<user>/<artist>')
def amount_artist_played_by_user(user, artist):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"user": user}},
                {"match": {"song.artist.keyword": artist}}]}}})
    x = results['hits'].get("total").get("value")
    amountPlays = []
    plays = {
        "plays": x
    }
    amountPlays.append(json.dumps(plays))

    return str(amountPlays)


@app.route('/amountSongPlayed/<song>')
def amount_song_played(song):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"song.title.keyword": song}}]}}})
    x = results['hits'].get("total").get("value")
    amountPlays = []
    plays = {
        "plays": x
    }
    amountPlays.append(json.dumps(plays))

    return str(amountPlays)


@app.route('/amountArtistPlayed/<artist>')
def artist_amount_played(artist):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"song.artist.keyword": artist}}]}}})
    x = results['hits'].get("total").get("value")
    amountPlays = []
    plays = {
        "plays": x
    }
    amountPlays.append(json.dumps(plays))

    return str(amountPlays)


@app.route('/topsongs')
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
        topsongs.append(json.dumps(data))

    return str(topsongs)


@app.route('/topartists')
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
        topartists.append(json.dumps(data))

    return str(topartists)


@app.route('/topArtistsForUser/<user>')
def get_top_artist_for_user(user):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": user
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
        topartists.append(json.dumps(data))

    return str(topartists)

@app.route('/topSongsForUser/<user>')
def get_top_songs_for_user(user):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": user
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
        topartists.append(json.dumps(data))

    return str(topartists)

@app.route('/topGenresForUser/<user>')
def get_top_genres_for_user(user):
    results = elastic.search(index="songstarted", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": user
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
        topartists.append(json.dumps(data))

    return str(topartists)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)