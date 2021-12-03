import logging
import random
import time
import os
import json
import requests
from datetime import datetime
from generator import *


days = 14
n = 10*10*14
artists = generate_artists(n, days)
songs = generate_songs(n,artists, days)


#Creates some initial "user created" events first and logs them
users = []
countries = generate_countries(10)
for _ in range(5):

    user = generate_userCreated(days, countries)
    users.append(user) 
    user = json.dumps(user) 
    requests.post('http://service01:80/users', json=user)



#Creates events in a loop
while True:
    rand = random.randint(1,8)

    
    #The following code can probably be optimized. Feel free to do so!
    
    switch = rand
    
    if switch == 1:
          entry = generate_songStarted(users,songs,days)
    elif switch == 2:
        entry = generate_songSkipped(users,songs,days)
    elif switch == 3:
        entry = generate_songPausedAndUnpaused(users,songs,days)
    elif switch == 4:
        doc = generate_userCreated(days, countries)
        doc_json = json.dumps(doc)
        users.append(doc)
        requests.post('http://service01:80/users', json=doc_json)

    elif switch == 5:
        doc = generate_adminCreated(days)
        doc_json = json.dumps(doc)
        requests.post('http://service01:80/admins', json=doc_json)

    elif switch == 6:
        entry = generate_searchQueries(users,days)
    elif switch == 7:
        entry = generate_songPausedAndUnpaused(users,songs,days)
    elif switch == 8:
        entry = generate_adClicks(users,days)
        

    
    if switch != 4 or switch != 5:
        entry = json.dumps(entry)
        print(entry)

        
    
