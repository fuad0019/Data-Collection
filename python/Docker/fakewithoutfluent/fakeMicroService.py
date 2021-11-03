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


log = "fake.log"

id = 0 
# Read id from the log
if os.path.exists(log):
    with open(log, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            last_line = lines[len(lines)-1]
            stripped_line = last_line[last_line.find('{'):]
            entry = json.loads(stripped_line) # Convert line to dictionary
            if entry['id']:
                id = entry['id']+1


print("generating users...")
users = generate_users(5)
print("generating songs...")
songs = generate_songs(10)
days = 14
n = 10*10*14


print("inserting users in index...")
progress = tqdm.tqdm(unit="events", total=int(len(users))) 
for ok, action in streaming_bulk(
    client=es, index="users", chunk_size=2000, actions=generate_userIndex(users,days)
):
    progress.update(1)

print("inserting events in index...")
while True:
    
    rand = random.randint(1,5)
    time.sleep(rand)

    
    #The following code can probably be optimized. Feel free to do so!
    
    switch = rand
 

    if switch == 1:
        entry = generate_songStarted(users,songs,days)
        res = es.index(index="songstarted", id=str(uuid.uuid4()),body=entry)
        print(res)
    elif switch == 2:
        entry = generate_songSkipped(users,songs,days)
        res = es.index(index="songskipped", id=str(uuid.uuid4()),body=entry)
        print(res)
    elif switch == 3:
        entry = generate_songPausedAndUnpaused(users,songs,days)
        res = es.index(index="songpaused", id=str(uuid.uuid4()),body=entry)
        print(res)

    elif switch == 4:
        entry = generate_searchQueries(users,days)
        res = es.index(index="searchqueries",id=str(uuid.uuid4()), body=entry)
        print(res)
 
    elif switch == 5:
        entry = generate_songPausedAndUnpaused(users,songs,days)
        res = es.index(index="songunpaused",id=str(uuid.uuid4()), body=entry)
        print(res)

    
  
    id += 1
