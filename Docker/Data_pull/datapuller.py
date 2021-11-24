from unicodedata import name
from flask.json import dumps
from markupsafe import escape
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import tqdm
import requests
import json
import os
import pymongo
import urllib.parse
import logging
from datetime import date, datetime
from dateutil.relativedelta import relativedelta



elastic = Elasticsearch(host="t05-elasticsearch")

dataSearchdomain= os.getenv('DATASEARCH_DOMAIN', 't05-datasearch')

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
    for document in res:
        yield document

def pull_all_artists():
    res = requests.get(dataSearchdomain + "/artists")
    for document in res:
        yield document

users= pull_all_songs()
songs = pull_all_songs()
artists = pull_all_artists()

print("Indexing events...")
progress = tqdm.tqdm(unit="events", total=int(len(users)+len(songs)+len(artists))) 

    
for ok, action in streaming_bulk(
    client=elastic, index="users", chunk_size=2000, actions=users):
        progress.update(1)
        
for ok, action in streaming_bulk(
    client=elastic, index="songs", chunk_size=2000, actions=songs):
        progress.update(1)
for ok, action in streaming_bulk(
    client=elastic, index="artists", chunk_size=2000, actions=artists):
        progress.update(1)
    