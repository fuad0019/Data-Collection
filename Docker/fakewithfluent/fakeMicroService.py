import logging
import random
import time
import os
import json
from datetime import datetime
from generator import *



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

# filemode w for overwriting whole file, filemode a for appending
#logging.basicConfig(filename=log, filemode="w", level=logging.DEBUG) 

#The logger module called "logging" logs everything even the imported modules like faker, basically a global logger.
# So in order to get a logger that only logs this module and ignores the imported modules, a custom logger is created like under:
logger = logging.getLogger("event_logger")
handler = logging.FileHandler(log)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

days = 14
n = 10*10*14
songs = generate_songs(10)

#Creates some initial "user created" events first and logs them
users = []
for _ in range(5):
    user = generate_userCreated(days)
    users.append(user) 
    user = json.dumps(user)
    print(user)
    logger.info(user)

    

#Creates events in a loop
while True:
    rand = random.randint(1,6)
    time.sleep(rand)

    
    #The following code can probably be optimized. Feel free to do so!
    
    switch = rand
    
    if switch == 1:
          entry = generate_songStarted(users,songs,days)
    elif switch == 2:
        entry = generate_songSkipped(users,songs,days)
    elif switch == 3:
        entry = generate_songPausedAndUnpaused(users,songs,days)
    elif switch == 4:
        entry = generate_userCreated(days)
        users.append(entry)
    elif switch == 5:
        entry = generate_searchQueries(users,days)
    elif switch == 6:
        entry = generate_songPausedAndUnpaused(users,songs,days)

    entry = json.dumps(entry)
    print(entry)
    #logging.info(entry)
    logger.info(entry)
    id += 1
