import random
import time
import json
import requests
from datetime import datetime
from elasticsearch import Elasticsearch
from generator import *

es = Elasticsearch("http://t05-elasticsearch:9200")


days = 14
genres = generate_genres(5)

#10 artists generated and send to elastic

artists = []
for _ in range(10):
    artist = generate_artists(genres,days)
    artists.append(artist)
    es.index(index="artists", id=str(uuid.uuid4()),body=artist)

#10 songs generated and send to elastic

songs = []
for _ in range(20):
    song = generate_song(genres,artists, days)
    songs.append(song)
    es.index(index="songs", id=str(uuid.uuid4()),body=song)

#Creates some initial "user created" events first and logs them

users = []
countries = generate_countries(10)
for _ in range(5):

    user = generate_userCreated(days, countries)
    users.append(user) 
    user = json.dumps(user) 
    requests.post('http://service01:80/users', json=user)


count = 0

#Creates events in a loop
while True:
    count+=1
    rand = random.randint(1,6)
    time.sleep(rand)


    if(count%10 != 0):
    
    #The following code can probably be optimized. Feel free to do so!
    
        switch = rand
        
        if switch == 1:
            entry = generate_songStarted(users,songs,days)
        elif switch == 2:
            entry = generate_songSkipped(users,songs,days)
        elif switch == 3:
            entry = generate_songPausedAndUnpaused(users,songs,days)
        elif switch == 4:
            entry = generate_searchQueries(users,days)
        elif switch == 5:
            entry = generate_songPausedAndUnpaused(users,songs,days)
        elif switch == 6:
            entry = generate_adClicks(users,days)
            
        entry = json.dumps(entry)
        print(entry)

    
    
    else:
        doc = generate_userCreated(days, countries)
        doc_json = json.dumps(doc)
        users.append(doc)
        requests.post('http://service01:80/users', json=doc_json)

        doc = generate_adminCreated(days)
        doc_json = json.dumps(doc)
        requests.post('http://service01:80/admins', json=doc_json)

        artist = generate_artists(genres,days)
        artists.append(artist)
        es.index(index="artists", id=str(uuid.uuid4()),body=artist)

        song = generate_song(genres,artists, days)
        songs.append(song)
        es.index(index="songs", id=str(uuid.uuid4()),body=song)

    
