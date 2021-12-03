#https://github.com/ruanbekker/data-generation-scripts/blob/master/generate-random-data-into-elasticsearch.py
#https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
from faker import Factory
from faker import Faker
from faker_music import MusicProvider
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from dateutil.relativedelta import relativedelta
import uuid
import tqdm
import random
import json

esDomainEndpoint = "http://t05-elasticsearch:9200"
client = Elasticsearch(esDomainEndpoint)


def generate_users(fake, n):
    # https://www.w3schools.com/python/python_dictionaries.asp
    gender = ['male', 'female', 'other']
    users = []
    for _ in range(n):
        name = fake.name()
        dob = fake.date_between(start_date='-60y', end_date='-10y')
        users.append({
            "_id": uuid.uuid4(),
            "name": name,
            "email": fake.ascii_email(),
            "gender": random.choice(gender),
            "country": fake.country(),
            "dob": dob,
            "age": str(relativedelta(datetime.today(), dob).years)
        })

    return users

    

def generate_songs(n):
    fake = Faker()
    fake.add_provider(MusicProvider)
    songs = []
    for _ in range(n):
        genSong = fake.text(max_nb_chars=20)[:-1]
        songs.append({
            "_id": uuid.uuid4(),
            "title": genSong,
            "genre": fake.music_genre(),
            "artist": fake.name()
        })
    return songs

def generate_songStarted(fake,users,songs,days,n):
    for _ in range(n):
        genUname = fake.slug()
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now")
        doc ={
                "_id": genUname,
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp
            }

        yield doc

def generate_songSkipped(fake,users,songs,days,n):
    for _ in range(n):
        genUname = fake.slug()
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now")
        doc ={
                "_id": genUname,
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,20)
            }

        yield doc

def generate_songPausedAndUnpaused(fake,users,songs,days,n):
    for _ in range(n):
        genUname = fake.slug()
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now")
        doc ={
                "_id": genUname,
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,180)
            }

        yield doc

def generate_searchQueries(fake,users,days,n):
    for _ in range(n):
        genUname = fake.slug()
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now")
        doc ={
                "_id": genUname,
                "user": random.choice(users)["_id"],
                "searchterm": fake.text(max_nb_chars=20)[:-1],
                "timestamp": genTimestamp
            }

        yield doc


def generate_userIndex(fake,users,days):
   
   for user in users:
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now")
        doc ={
                "_id": user["_id"],
                "name": user["name"],
                "email": user["email"],
                "gender": user["gender"],
                "country": user["country"],
                "dob":user["dob"],
                "timestamp": genTimestamp
            }

        yield doc


if __name__ == '__main__':
    fake = Factory.create()
    songs = generate_songs(50)
    users = generate_users(fake,300)
    days = 14
    n = 300*10*14

    

    print("Indexing events...")
    progress = tqdm.tqdm(unit="events", total=int(n+n/100+n/5+n/5+len(users))) 
    
    for ok, action in streaming_bulk(
        client=client, index="users", chunk_size=2000, actions=generate_userIndex(fake,users,days)
    ):
        progress.update(1)
        
    for ok, action in streaming_bulk(
        client=client, index="songstarted", chunk_size=2000, actions=generate_songStarted(fake,users,songs,days,n)
    ):
        progress.update(1)
    for ok, action in streaming_bulk(
        client=client, index="songskipped", chunk_size=2000, actions=generate_songSkipped(fake,users,songs,days,int(n/100))
    ):
        progress.update(1)
    for ok, action in streaming_bulk(
        client=client, index="songpaused", chunk_size=2000, actions=generate_songPausedAndUnpaused(fake,users,songs,days,int(n/5))
    ):
        progress.update(1)

    for ok, action in streaming_bulk(
        client=client, index="songunpaused", chunk_size=2000, actions=generate_songPausedAndUnpaused(fake,users,songs,days,int(n/5))
    ):
        progress.update(1)
        
   