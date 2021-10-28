import logging
import random
import time
import ast
import os
from datetime import datetime
log = "fake.log"

id = 0 
# Read id from the log
if os.path.exists(log):
    with open(log, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            last_line = lines[len(lines)-1]
            stripped_line = last_line[last_line.find('{'):]
            entry = ast.literal_eval(stripped_line) # Convert line to dictionary
            if entry['id']:
                id = entry['id']+1

logging.basicConfig(filename=log, filemode="w", level=logging.DEBUG) # filemode w for overwriting whole file, filemode a for appending

while True:
    time.sleep(random.randint(1,6))

    entry = {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "id": id,
        "random": random.randint(1,1000)
    }
    print(entry)
    logging.info(entry)
    id += 1
