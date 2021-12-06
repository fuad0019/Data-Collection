import random
import time
import json
from datetime import datetime
from generator import *
from elasticsearch import Elasticsearch
import requests


es = Elasticsearch("http://t05-elasticsearch:9200")

days = 14
n = 10*10*14
genres = generate_genres(5)

artists = []
for _ in range(10):
    artist = generate_artist(genres,days)
    artists.append(artist)
    res = es.index(index="artists", id=str(uuid.uuid4()),body=artist)

songs = []
for _ in range(20):
    song = generate_song(genres,artists, days)
    songs.append(song)
    res = es.index(index="songs", id=str(uuid.uuid4()),body=song)


#Creates some initial "user created" events first and logs them
users = []
countries = generate_countries(10)
for _ in range(5):
    user = generate_userCreated(days)
    users.append(user) 
    user = json.dumps(user) 
    res = requests.post('http://service01:80/users', json=user)


    while True:
        
        rand = random.randint(1,8)
        time.sleep(rand)

        
        #The following code can probably be optimized. Feel free to do so!
        
        switch = rand
    

        if switch == 1:
            entry = generate_songStarted(users,songs,days)
            res = es.index(index="songstarted.team05.t05-fakemicroservice", id=str(uuid.uuid4()),body=entry)
        elif switch == 2:
            entry = generate_songSkipped(users,songs,days)
            res = es.index(index="songskipped.team05.t05-fakemicroservice", id=str(uuid.uuid4()),body=entry)
        elif switch == 3:
            entry = generate_songPausedAndUnpaused(users,songs,days)
            res = es.index(index="songpaused.team05.t05-fakemicroservice", id=str(uuid.uuid4()),body=entry)
        elif switch == 4:
            entry = generate_searchQueries(users,days)
            res = es.index(index="search.team05.t05-fakemicroservice",id=str(uuid.uuid4()), body=entry)
        elif switch == 5:
            entry = generate_songPausedAndUnpaused(users,songs,days)
            res = es.index(index="songunpaused.team05.t05-fakemicroservice",id=str(uuid.uuid4()), body=entry)
        elif switch == 6:
            entry = generate_userCreated(days)
            users.append(entry)
            doc_json = json.dumps(entry)
            requests.post('http://service01:80/users', json=doc_json)
        elif switch == 7:
            entry = generate_adminCreated(days)
            doc_json = json.dumps(entry)
            requests.post('http://service01:80/admins', json=doc_json)
        elif switch == 8:
            entry = generate_adClicks(users,days)
            res = es.index(index="adclicks.team05.t05-fakemicroservice",id=str(uuid.uuid4()), body=entry)


        
        
  
