from typing import Dict
from unicodedata import name
from flask import Flask, jsonify, render_template, request
from flask.helpers import send_file, send_from_directory
from flask.json import dumps
from markupsafe import escape
from elasticsearch import Elasticsearch
import json
import pymongo
import urllib.parse
import os


serviceUrl = os.getenv("serviceurl", "http://opensuse.stream.stud-srv.sdu.dk")
elastic = Elasticsearch(host="t05-elasticsearch")

username = urllib.parse.quote_plus('username123')
password = urllib.parse.quote_plus('password123')
myclient = pymongo.MongoClient(
    'mongodb://%s:%s@t05-mongodb:27017' % (username, password))
mydb = myclient["t05"]


# log search links saved as saved-objects using the share kibana feauture
logSavedObjects = {
    'team05': serviceUrl + '/app/discover#/view/c6697420-4a58-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'kube-system': serviceUrl + '/app/discover#/view/4a1ecf90-4a13-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'longhorn': serviceUrl + '/app/discover#/view/fb3f7f50-4aa3-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'fluent': serviceUrl + '/app/discover#/view/73e45ac0-4aa4-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!f%2Cvalue%3A10000)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
    'ingress-nginx': serviceUrl + '/app/discover#/view/5bb683f0-4aa5-11ec-a57c-8577c0017101?_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!f%2Cvalue%3A10000)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))',
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
    mycol = mydb["users"]
    users = []
    for x in mycol.find({}, {"event": 0}):
        users.append(x["_id"])
    return jsonify(users)


@app.route('/users', methods=['POST'])
def save_user():
    mycol = mydb["users"]

    if(request.is_json != True):
        return "This is not json"

    data = request.json
    mongodoc = json.loads(data)

    x = mycol.insert_one(mongodoc)
    return str(x.inserted_id)


@app.route('/users/<userid>')
def get_user_profile(userid):
    # Get a user profile
    mycol = mydb["users"]

    myquery = mycol.find_one({"_id": userid}, {"event": 0})

    return jsonify(myquery)


@app.route('/admins')
def get_Admins():
    mycol = mydb["admins"]
    admins = []
    for x in mycol.find({}, {"event": 0}):
        admins.append(x["_id"])
    return jsonify(admins)


@app.route('/admins', methods=['POST'])
def save_Admin():
    mycol = mydb["admins"]
    if(request.is_json != True):
        return "This is not json at all"

    data = request.json
    mongodoc = json.loads(data)

    x = mycol.insert_one(mongodoc)
    return str(x.inserted_id)


@app.route('/admins/<adminid>')
def get_admin_profile(adminid):
    # Get a user profile
    mycol = mydb["admins"]

    myquery = mycol.find_one({"_id": adminid}, {"event": 0})

    return str(isinstance(myquery, dict))



@app.route('/users/<id>/songs')
def get_song_history(id):
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

@app.route('/users/<id>/artists')
def get_artist_history(id):
    results = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={
                             "query": {"match": {"user": id}}})

    userHistory = []
    for i in results['hits'].get("hits"):
        data = {
            "artist": i['_source']["song"]["artist"],
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
    results = elastic.search(index="adclicks.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
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


@app.route('/logs/<namespace>')
def get_namespace_log(namespace):
    link = logSavedObjects[namespace]

    return render_template('logs.html', namespacehtml=namespace, linkhtml=link)


@app.route('/users/<id>/recommendation/artists')
def get_user_recommendations_artists(id):
    timeintervarl = "30"
    topGenreResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "filter":
                {"range": {"timestamp": {"gte": "now-" +
                                         timeintervarl + "d/d", "lt": "now/d"}}},
            "must": [
                {"match": {
                    "user": id
                }}
                ]
        }
    },
        "aggs": {
        "genres": {
            "terms": {
                "field": "song.genre.keyword"
            }
        },
        "artists": {
            "terms": {
                "field": "song.artist.keyword"
            }
        }
    }})

    topArtists = []
    for i in topGenreResult['aggregations']['artists']['buckets']:
        topArtists.append({"match": {"artist.keyword": i["key"]}})

    topgenres = []
    for i in topGenreResult['aggregations']['genres']['buckets']:
        topgenres.append({"match": {"genre.keyword": i["key"]}})

    if(len(topgenres) == 0):
        return 'This user has not listened to anything the last ' + timeintervarl + ' days'

    topGenreResult = elastic.search(index="songs", doc_type="_doc", body={
        "query": {
            "bool": {
                "should": topgenres,
                "must_not": topArtists
            }
        }
    })

    artists = set()

    for i in topGenreResult['hits'].get('hits'):
        artists.add(i["_source"]["artist"])

    #Turning set into list, because set is not json serializable    
    artistslist = list(artists)

    return jsonify(artistslist)



# This method returns the top songs for each user without duplicates as json
@app.route('/users/<id>/recommendation/songs')
def get_multiple_song_matches(id):

    multiple_users_top_songs = get_multiple_users_top_songs(id)
    if(multiple_users_top_songs == None):
        return "The user has not listened to songs"
    elif(len(multiple_users_top_songs)== 0):
        return get_user_recommendations_songs(id)

    sortedList = sorted(multiple_users_top_songs, key=lambda x: x['freq'], reverse=True)

    return jsonify({"collaborative" : sortedList})




def get_user_recommendations_songs(id): 
    timeintervarl = "30"
    topGenreResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "filter":
                {"range": {"timestamp": {"gte": "now-" +
                                         timeintervarl + "d/d", "lt": "now/d"}}},
            "must": [
                {"match": {
                    "user": id
                }}
                ]
        }
    },
        "aggs": {
        "genres": {
            "terms": {
                "field": "song.genre.keyword"
            }
        },
        "songs": {
            "terms": {
                "field": "song.title.keyword"
            }
        }
    }})

    topSongs = []
    for i in topGenreResult['aggregations']['songs']['buckets']:
        topSongs.append({"match": {"title.keyword": i["key"]}})

    topgenres = []
    for i in topGenreResult['aggregations']['genres']['buckets']:
        topgenres.append({"match": {"genre.keyword": i["key"]}})

    if(len(topgenres) == 0):
        return 'This user has not listened to anything the last ' + timeintervarl + ' days'

    topGenreResult = elastic.search(index="songs", doc_type="_doc", body={
        "query": {
            "bool": {
                "should": topgenres,
                "must_not": topSongs
            }
        }
    })
    songs = set()
    for i in topGenreResult['hits'].get('hits'):
        songs.add(i["_source"]["title"])
    songslist = list(songs)
    return jsonify({"content_based" : songslist})


# This method appends the top 10 users favorite 10 songs into an array. The output will be an array filled with arrays.
def get_multiple_users_top_songs(user):
    matching_users = find_matching_users(user)
    songs = []

    if(matching_users == None):
        return None
    elif(len(matching_users)==0):
        return []

    for i in matching_users:
        songs.extend(get_top_songs(i))

    #changing a lists size while iterating might cause problems
    unique_songs = set(songs)
    songsWithfreq = []
    for i in unique_songs:
        count = songs.count(i)
        freq = count/len(songs)

        
        songsWithfreq.append({
            "song": i,
            "freq": freq}) 
    
    
    return songsWithfreq



# This method searches in ES for a users top 10 songs. This method will be used in a loop to get all of top 10 matching users top 10 songs.
def get_top_songs(id):
  

    songQueryResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "user": id}}]}},
        "aggs": {"songs": {"terms": {"field": "song.title.keyword", "exclude": find_favorite_song(id)}}}})

    topSongs = []
    
    for i in songQueryResult['aggregations']['songs']['buckets']:
        topSongs.append(i["key"])
    return topSongs



# This methods finds and returns the top matching users.


def find_matching_users(user):

    favourite_song = find_favorite_song(user)
    if(favourite_song == None):
        return None

    userQueryResult = elastic.search(index="songstarted.team05.t05-fakemicroservice", doc_type="_doc", body={"query": {
        "bool": {
            "must": [
                {"match": {
                    "song.title.keyword": favourite_song
                }}
            ]
        }
    },
        "aggs": {"user": {"terms": {"field": "user.keyword", "exclude": user}}}})

    topUsers = []
    
    for i in userQueryResult['aggregations']['user']['buckets']:
        topUsers.append(i["key"])

    return topUsers

# This method finds a users favourite song
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
    topsongs = topSongsQuery['aggregations']['songs']['buckets']
    if(len(topsongs) == 0):
        return None
    topSong = topSongsQuery['aggregations']['songs']['buckets'][0].get('key')
    return topSong


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
