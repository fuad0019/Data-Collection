import logging
import random
import time
import ast
import os
import json
from datetime import datetime
from generator import *
from faker import Factory
from elasticsearch import Elasticsearch
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


fake = Factory.create()
users = generate_users(fake,5)
songs = generate_songs(10)
days = 14
n = 10*10*14


while True:

    rand = random.randint(1,6)
    time.sleep(rand)

    
    #The following code can probably be optimized. Feel free to do so!
    
    switch = rand
    fake = Factory.create()
    
    if switch == 1:
        entry = generate_songStarted(fake,users,songs,days,n)
        res = es.index(index="songstarted", id=str(uuid.uuid4()),body=entry)
        print(res)
    elif switch == 2:
        entry = generate_songSkipped(fake,users,songs,days,n)
        res = es.index(index="songskipped", id=str(uuid.uuid4()),body=entry)
        print(res)
    elif switch == 3:
        entry = generate_songPausedAndUnpaused(fake,users,songs,days,n)
        res = es.index(index="songpaused", id=str(uuid.uuid4()),body=entry)
        print(res)

    elif switch == 4:
        entry = generate_userIndex(fake,users,days)
        res = es.index(index="users", id=str(uuid.uuid4()),body=entry)
        print(res)

    elif switch == 5:
        entry = generate_searchQueries(fake,users,days,n)
        res = es.index(index="searchqueries",id=str(uuid.uuid4()), body=entry)
        print(res)
 
    elif switch == 6:
        entry = generate_songPausedAndUnpaused(fake,users,songs,days,n)
        res = es.index(index="songunpaused",id=str(uuid.uuid4()), body=entry)
        print(res)

    
  
    id += 1
