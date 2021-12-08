#https://github.com/ruanbekker/data-generation-scripts/blob/master/generate-random-data-into-elasticsearch.py
#https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
import uuid
import random
from faker import Faker
from faker_music import MusicProvider
from datetime import datetime
from dateutil.relativedelta import relativedelta


fake = Faker()

def generate_userCreated(days):
    #https://www.w3schools.com/python/python_dictionaries.asp
    gender = ['male', 'female', 'other']
    genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
    dob = fake.date_between(start_date='-60y', end_date='-10y').isoformat()
    name = fake.name()
    doc = {
            "event": "userCreated",
            "user_id": str(uuid.uuid4()),
            "name": name,
            "email": fake.ascii_email(),
            "gender": random.choice(gender),
            "country": fake.country(),
            "dob": dob,
            "age": str(relativedelta(datetime.today(), fake.date_between(start_date='-60y', end_date='-10y')).years),
            "timestamp": genTimestamp
        }
        
    return doc
    

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
                "event": "songStarted",
                "user": random.choice(users)["user_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp
            }

        return doc

def generate_songSkipped(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "songSkipped",
                "user": random.choice(users)["user_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,20)
            }

        return doc

def generate_songPausedAndUnpaused(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        events = ["songPaused", "songUnpaused"]
        doc ={
                "event": random.choice(events),
                "user": random.choice(users)["user_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,180)
            }

        return doc

def generate_searchQueries(users,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "search",
                "user": random.choice(users)["user_id"],
                "searchterm": fake.text(max_nb_chars=20)[:-1],
                "timestamp": genTimestamp
            }

        return doc

def generate_adClicks(users,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "adclicks",
                "user": random.choice(users)["user_id"],
                "ad": str(uuid.uuid4()),
                "timestamp": genTimestamp
            }

        return doc
