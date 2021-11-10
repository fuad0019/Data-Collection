#https://github.com/ruanbekker/data-generation-scripts/blob/master/generate-random-data-into-elasticsearch.py
#https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
import uuid
import random
from faker import Faker
from faker_music import MusicProvider
from datetime import datetime
from dateutil.relativedelta import relativedelta


fake = Faker()


def generate_users(n,days):
    #https://www.w3schools.com/python/python_dictionaries.asp
    gender = ['male', 'female', 'other']
    users = []
    genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
    dob = fake.date_between(start_date='-60y', end_date='-10y').isoformat()
    name = fake.name()
    
    for _ in range(n):
        name = fake.name()
        users.append({
            "event": "userCreated",
            "_id": str(uuid.uuid4()),
            "name": name,
            "email": fake.ascii_email(),
            "gender": random.choice(gender),
            "country": fake.country(),
            "dob": dob,
            "age": str(relativedelta(datetime.today(), fake.date_between(start_date='-60y', end_date='-10y')).years),
            "timestamp": genTimestamp
        })
        
    return users


def generate_songs(n):
    
    fake.add_provider(MusicProvider)
    songs = []
    for _ in range(n):
        genSong = fake.text(max_nb_chars=20)[:-1]
        songs.append({
            "_id": str(uuid.uuid4()),
            "title": genSong,
            "genre": fake.music_genre(),
            "artist": fake.name()
        })
    return songs

def generate_songStarted(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp
            }

        return doc

def generate_songSkipped(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,20)
            }

        return doc

def generate_songPausedAndUnpaused(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,180)
            }

        return doc

def generate_searchQueries(users,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "user": random.choice(users)["_id"],
                "searchterm": fake.text(max_nb_chars=20)[:-1],
                "timestamp": genTimestamp
            }

        return doc


def generate_userIndex(users,days):


    for user in users:

        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
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
