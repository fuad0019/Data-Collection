from unicodedata import name
from flask import Flask, jsonify, render_template, request
from flask.helpers import send_file, send_from_directory
from flask.json import dumps
from markupsafe import escape
from elasticsearch import Elasticsearch
import json
import pymongo
import urllib.parse
import logging
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


elastic = Elasticsearch(host="t05-elasticsearch")

username = urllib.parse.quote_plus('username123')
password = urllib.parse.quote_plus('password123')
myclient = pymongo.MongoClient(
    'mongodb://%s:%s@t05-mongodb:27017' % (username, password))
mydb = myclient["t05"]
mycol = mydb["users"]

# log search links saved as saved-objects using the share kibana feauture
logSavedObjects = {
    'team05': 'http://opensuse.stream.stud-srv.sdu.dk/app/discover#/view/c6697420-4a58-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'kube-system': 'http://opensuse.stream.stud-srv.sdu.dk/app/discover#/view/4a1ecf90-4a13-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'longhorn': 'http://opensuse.stream.stud-srv.sdu.dk/app/discover#/view/fb3f7f50-4aa3-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'fluent': 'http://opensuse.stream.stud-srv.sdu.dk/app/discover#/view/73e45ac0-4aa4-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!f%2Cvalue%3A10000)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'ingress-nginx': 'http://opensuse.stream.stud-srv.sdu.dk/app/discover#/view/5bb683f0-4aa5-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!f%2Cvalue%3A10000)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'team01': '',
    'team02': '',
    'team03': '',
    'team04': '',
    'team06': '',
    'team07': '',
    'team08': '',
    'team09': '',
    'team10': '',
    'team11': '',
    'team12': '',
    'team13': '',
    'team14': ''

}

# This sets up the application using the Flask object from the package flask.
app = Flask(__name__)


@app.route('/', methods=['GET'])  # Define http method
def home():
    return render_template("index.html")


@app.route('/users')
def getUsers():
    users = []
    for x in mycol.find({}, {"event": 0}):
        users.append(x)
    return jsonify(users)
    
@app.route('/users', methods=['POST'])
def save_user():
    if(request.is_json != True):
        return "This is not json"

    data = request.json
    mongodoc = json.loads(data)

    x = mycol.insert_one(mongodoc)
    return str(x.inserted_id)


@app.route('/users/<userid>')
def get_user_profile(userid):
    # Get a user profile
    users = []

    myquery = mycol.find_one({"_id": userid})

    for x in mycol.find(myquery, {"event": 0}):
        users.append(x)

    if(len(users) == 0):
        return jsonify(users)

    return jsonify(users[0])


# http://192.168.136.61:5000/history/41c6e6d7-b78c-413f-adb3-0567aa4996ef

@app.route('/users/<id>/songs')
def get_history(id):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={
                             "query": {"match": {"user": id}}})

    userHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "song": i['_source']["song"],
            "timestamp": i['_source']["timestamp"]
        }
        userHistory.append(data)
    return jsonify(userHistory)


@app.route('/users/<id>/searches')
def get_search_history(id):
    results = elastic.search(index="search.team05.t05-fakemicroservice", doc_type="_doc", body={
                             "query": {"match": {"user": id}}})

    userSearchHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "searchterm": i['_source']["searchterm"],
            "timestamp": i['_source']["timestamp"]
        }
        userSearchHistory.append(data)
    return jsonify(userSearchHistory)


@app.route('/users/<user>/songs/<song>/amount_played')
def amount_song_played_by_user(user, song):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
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

    return jsonify(plays)


@app.route('/users/<user>/artists/<artist>/amount_played')
def amount_artist_played_by_user(user, artist):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"user": user}},
                {"match": {"song.artist.keyword": artist}}]}}})
    x = results['hits'].get("total").get("value")
    plays = {
        "plays": x
    }

    return jsonify(plays)


@app.route('/songs/<id>/amount_played')
def amount_song_played(id):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"song._id.keyword": id}}]}}})
    x = results['hits'].get("total").get("value")
    plays = {
        "plays": x
    }

    return jsonify(plays)


@app.route('/artists/<id>/amount_played')
def artist_amount_played(id):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"song.artist.keyword": id}}]}}})
    x = results['hits'].get("total").get("value")
    plays = {
        "plays": x
    }

    return jsonify(plays)


@app.route('/ads/<id>/amount_clicked')
def ad_amount_clicked(id):
    results = elastic.search(index="adclicks.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"ad": id}}]}}})
    x = results['hits'].get("total").get("value")
    clicks = {
        "clicks": x
    }

    return jsonify(clicks)


@app.route('/ads')
def ad():
    results = elastic.search(index="adclicks.team05.t05-fakemicroservice", doc_type="_doc", body={  "query": {
    "match_all": {}
  }})
    x = results['hits']['hits']

    return jsonify(x)


@app.route('/songs/top')
def get_top_songs():
    # Get top 10 songs started the last week
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
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

    return jsonify(topsongs)


@app.route('/artists/top')
def get_top_artists():
    # Get top 10 artists the last week
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
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

    return jsonify(topartists)


@app.route('/users/<id>/artists/top')
def get_top_artist_for_user(id):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
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

    return jsonify(topartists)


@app.route('/users/<id>/songs/top')
def get_top_songs_for_user(id):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
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

    return jsonify(topartists)


@app.route('/users/<id>/genres/top')
def get_top_genres_for_user(id):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
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

    return jsonify(topartists)


'''
@app.route('/advertisements/<id>/amount_clicked')
def get_advertisements_amount_clicked(id):
    results = elastic.search(index="adclicks.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {"ad.keyword": id}}]}}})
    x = results['hits'].get("total").get("value")
    plays = {
        "clicks": x
    }

    return jsonify(plays)
'''


@app.route('/logs/<namespace>')
def get_namespace_log(namespace):
    link = logSavedObjects[namespace]

    return render_template('logs.html', namespacehtml=namespace, linkhtml=link)


@app.route('/logs/all')
def get_all_log(id):

    return ""


@app.route('/users/<id>/recommendation/songs')
def get_genres_recommendation_for_user(id):
    topGenreResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "filter":
                {"range": {"timestamp": {"gte": "now-7d/d", "lt": "now/d"}}},
            "must": [
                {"match": {
                    "user": id
                }}
                    ]
        }
    },
        "aggs": {"artists": {"terms": {"field": "song.genre.keyword"}}}})
    topgenres = []
    for i in topGenreResult['aggregations']['artists']['buckets']:
        data = {
            "genre": i["key"],
            "plays": i["doc_count"]
        }
        topgenres.append(data)

    topgenresForUser = [topgenres[0].get('genre')]

    topGenreResult = elastic.search(index="songs", doc_type="_doc", body={"query": {
        "more_like_this": {
            "fields": ["genre.keyword"],
            "like": [topgenresForUser[0]],
            "min_term_freq": 1,
            "max_query_terms": 2
        }
    }})
    songs = []
    for i in topGenreResult['hits'].get('hits'):
        data = {
            "title": i["_source"]["title"],
            "genre": i["_source"]["genre"],
            "artist": i["_source"]["artist"]
        }
        songs.append(data)
    return jsonify(songs)


@app.route('/users/<id>/recommendation/artists')
def get_artist_recommendation_for_user(id):
    topGenreResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "filter":
                {"range": {"timestamp": {"gte": "now-7d/d", "lt": "now/d"}}},
            "must": [
                {"match": {
                    "user": id
                }}
                    ]
        }
    },
        "aggs": {"artists": {"terms": {"field": "song.genre.keyword"}}}})
    topgenres = []
    for i in topGenreResult['aggregations']['artists']['buckets']:
        data = {
            "genre": i["key"],
            "plays": i["doc_count"]
        }
        topgenres.append(data)

    topgenresForUser = [topgenres[0].get('genre')]

    topGenreResult = elastic.search(index="artists", doc_type="_doc", body={"query": {
        "more_like_this": {
            "fields": ["genre.keyword"],
            "like": [topgenresForUser[0]],
            "min_term_freq": 1,
            "max_query_terms": 2
        }
    }})
    songs = []
    for i in topGenreResult['hits'].get('hits'):
        data = {
            "artist_name": i["_source"]["name"],
            "genre": i["_source"]["genre"],
        }
        songs.append(data)
    return jsonify(songs)


@app.route('/users/<id>/recommendations/genres')
def get_user_recommendations_genres(id):

    return ""



@app.route('/visuals')
def getvisualizations():
    return render_template("visualization.html")


# _______________________________________________________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________________________________________________
# COMPARATIVE RECOMMENDATION

# This method finds multiple users who also listens to the same song as you and returns them in a list
def find_favorite_song(user):
    topSongsQuery = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": user
                }}
            ]
        }
    },
        "aggs": {"songs": {"terms": {"field": "song.title.keyword"}}}})
    topSong = topSongsQuery['aggregations']['songs']['buckets'][0].get('key')
    return topSong

# This method finds the top matching user.
def find_matching_user(user):
    userQueryResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "song.title.keyword": find_favorite_song(user)
                }}
            ]
        }
    },
        "aggs": {"user": {"terms": {"field": "user.keyword", "exclude": user}}}})

    topUser = userQueryResult['aggregations']['user']['buckets'][0].get(
        'key')  # Use this for the top matching user

    return topUser

# This methods finds and returns the top matching users.
def find_matching_users(user):
    userQueryResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "song.title.keyword": find_favorite_song(user)
                }}
            ]
        }
    },
        "aggs": {"user": {"terms": {"field": "user.keyword", "exclude": user}}}})

    topUsers = []
    for i in userQueryResult['aggregations']['user']['buckets']:
        data = {
            "user": i["key"],
            "count": i["doc_count"]
        }
        topUsers.append(data)

    return topUsers


# This method searches in ES for a users top 10 songs. This method will be used in a loop to get all of top 10 matching users top 10 songs.
def get_song_test(id):
    songQueryResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": find_matching_user(id)}}]}},
        "aggs": {"songs": {"terms": {"field": "song.title.keyword", "exclude": find_favorite_song(id)}}}})

    topSongs = []
    for i in songQueryResult['aggregations']['songs']['buckets']:
        data = {
            "Title": i["key"]
        }
        topSongs.append(data)
    return topSongs


# This method appends the top 10 users favorite 10 songs into an array. The output will be an array filled with arrays.
def get_multiple_users_top_songs(user):
    songs = []

    for i in find_matching_users(user):
        songs.append(get_song_test(i['user']))
    return songs


# This method returns the top songs for each user without duplicates as json
@app.route('/users/<id>/comparativerec/songs')
def get_multiple_song_matches(id):
    usersSongList = []
    for i in get_multiple_users_top_songs(id):
        usersSongList.append(i)

    combinedSongList = []

    for i in usersSongList:
        for j in i:
            combinedSongList.append(j['Title'])

    checkDuplicate = set(combinedSongList)

    finalRecommendedSongList = []
    for i in checkDuplicate:
        data = {
            "Title": i
        }
        finalRecommendedSongList.append(data)

    return jsonify(finalRecommendedSongList)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
