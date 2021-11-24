import logging
import random
import time
import ast
import os
import json
import tqdm
from datetime import datetime
from generator import *
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

es = Elasticsearch("http://t05-elasticsearch:9200")

days = 14
n = 10*10*14
songs = generate_songs(10)

#Creates some initial "user created" events first and logs them
users = []
for _ in range(5):
    user = generate_userCreated(days)
    users.append(user) 
    res = es.index(index="users", id=user["user_id"],body=user)
    print(res)




print("inserting events in index...")
while True:
    
    rand = random.randint(1,7)
    time.sleep(rand)

    
    #The following code can probably be optimized. Feel free to do so!
    
    switch = rand
 

    if switch == 1:
        entry = generate_songStarted(users,songs,days)
        res = es.index(index="songstarted", id=str(uuid.uuid4()),body=entry)
    elif switch == 2:
        entry = generate_songSkipped(users,songs,days)
        res = es.index(index="songskipped", id=str(uuid.uuid4()),body=entry)
    elif switch == 3:
        entry = generate_songPausedAndUnpaused(users,songs,days)
        res = es.index(index="songpaused", id=str(uuid.uuid4()),body=entry)
    elif switch == 4:
        entry = generate_searchQueries(users,days)
        res = es.index(index="searchqueries",id=str(uuid.uuid4()), body=entry)
    elif switch == 5:
        entry = generate_songPausedAndUnpaused(users,songs,days)
        res = es.index(index="songunpaused",id=str(uuid.uuid4()), body=entry)
    elif switch == 6:
        entry = generate_userCreated(days)
        users.append(entry)
        res = es.index(index="users",id=str(uuid.uuid4()), body=entry)
    elif switch == 7:
        entry = generate_adClicks(users,days)
        res = es.index(index="adclicks",id=str(uuid.uuid4()), body=entry)

    
    
    print(res)
    
  
