from typing import List
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import tqdm
import requests
import os
import pymongo
import urllib.parse
from flask import Flask, json

app = Flask(__name__)



elastic = Elasticsearch(host="t05-elasticsearch")

dataSearchdomain= os.getenv('DATASEARCH_DOMAIN', 'http://t05-datasearch')

username = urllib.parse.quote_plus('username123')
password = urllib.parse.quote_plus('password123')
myclient = pymongo.MongoClient('mongodb://%s:%s@t05-mongodb:27017' % (username, password))
mydb = myclient["t05"]
mycol = mydb["users"]

def pull_all_users():
    cursor = mycol.find({})
    for document in cursor:
        yield document

def pull_all_songs():
    res = requests.get(dataSearchdomain + "/songs")
    data = res.text
    data = json.loads(data)
    for document in data:
        yield document

def pull_all_artists():
    res = requests.get(dataSearchdomain + "/artists")
    data = res.text
    data = json.loads(data)
    for document in data:
        yield document


def sendToElastic(index_name,list):
    for ok, action in streaming_bulk(client=elastic, index=index_name, chunk_size=2000, actions=list):
        print("Printed User")

def changeIdFormatUser(users):
    changedFormatUsers= []
    for user in users.values():
        user['user_id'] = user['_id']
        changedFormatUsers.append(user) 
    return changedFormatUsers
    




#For caching so we can check if the pulled users already have been pulled 
cacheUsers={}
cacheSongs= {}
cacheArtists={}


#Same as below
@app.route('/pullUsers')
def get_users():
    allUsers = pull_all_users()    
    newUsers={}
    for user in allUsers:
        if(len(cacheUsers)!=0):
            try:
                cacheUsers[user["_id"]]
            except KeyError:
                newUsers[user["_id"]] = user
        else:
            newUsers[user["_id"]] = user

    cacheUsers.update(newUsers)

    if(len(newUsers)==0):
        return "Users is up to date" 
    else:
        newFormatUsers= changeIdFormatUser(newUsers)
        sendToElastic('users',newFormatUsers)

        return "Updated Users"           
        
    

@app.route('/pullSongs')
def get_songs():
    #Get all songs from datasearch
    allSongs = pull_all_songs()
    newSongs={}
    for song in allSongs:
        if(len(cacheSongs)!=0):
        # Check if a song exists in cache, if not, then a keyError is returned
            try:
                cacheSongs[song["song_id"]]
        #if a keyError is returned, then add to dict of new songs 
            except KeyError:
                newSongs[song["song_id"]] = song
        else:
            newSongs[song["song_id"]] = song


        #Cache the new songs
    cacheSongs.update(newSongs)

        #If list of new songs is empty, then up-to-date, if not then update elastic
    if(len(newSongs)==0):
        return "Songs is up to date" 
    else:
        sendToElastic('songs',newSongs.values())

        return "Updated songs"    

#Same as above
@app.route('/pullArtists')
def get_artists():
    allArtists = pull_all_artists()
    newArtists={}
    for artist in allArtists:
        if(len(cacheArtists)!=0):
            try:
                cacheArtists[artist["artist_id"]]
            except KeyError:
                newArtists[artist["artist_id"]] = artist
        else:
            newArtists[artist["artist_id"]] = artist

    cacheArtists.update(newArtists)

    if(len(newArtists)==0):
        return "Artists is up to date" 
    else:
        sendToElastic('artists',newArtists.values())
        return "Updated artists"   


if __name__ == '__main__':
    
    app.run(host='0.0.0.0', debug=True)