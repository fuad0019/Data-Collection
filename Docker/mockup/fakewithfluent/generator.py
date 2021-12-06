#https://github.com/ruanbekker/data-generation-scripts/blob/master/generate-random-data-into-elasticsearch.py
#https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
import uuid
import random
from faker import Faker
from faker_music import MusicProvider
from datetime import datetime
from dateutil.relativedelta import relativedelta


fake = Faker()
fake.add_provider(MusicProvider)



def generate_countries(n):
    countries = []
    for _ in range(n):
        countries.append(fake.country())
    return countries

def generate_userCreated(days, countries):
    #https://www.w3schools.com/python/python_dictionaries.asp
    gender = ['male', 'female', 'other']
    genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
    dob = fake.date_between(start_date='-60y', end_date='-10y')
    name = fake.name()
    doc = {
            "event": "userCreated",
            "_id": str(uuid.uuid4()),
            "name": name,
            "email": fake.ascii_email(),
            "gender": random.choice(gender),
            "country": random.choice(countries),
            "country_code": fake.country_code(),
            "dob": dob.isoformat(),
            "age": str(relativedelta(datetime.today(), dob).years),
            "timestamp": genTimestamp
        }
        
    return doc

def generate_adminCreated(days):
    #https://www.w3schools.com/python/python_dictionaries.asp

    genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
    
    doc = {
            "event": "adminCreated",
            "_id": str(uuid.uuid4()),
            "timestamp": genTimestamp
        }
        
    return doc
    

def generate_songStarted(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "songStarted",
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp
            }

        return doc

def generate_songSkipped(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "songSkipped",
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,20)
            }

        return doc

def generate_songPausedAndUnpaused(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        events = ["songPaused", "songUnpaused"]
        user= random.choice(users)
        doc ={
                "event": random.choice(events),
                "user": user["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,180)
            }

        return doc

def generate_searchQueries(users,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "search",
                "user": random.choice(users)["_id"],
                "searchterm": fake.text(max_nb_chars=20)[:-1],
                "timestamp": genTimestamp
            }

        return doc

def generate_adClicks(users,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "adclicks",
                "user": random.choice(users)["_id"],
                "ad": str(uuid.uuid4()),
                "timestamp": genTimestamp
            }

        return doc

def generate_song(genres,artists, days):
    genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()

    genSong = fake.text(max_nb_chars=20)[:-1]
    song = {
            "song_id": str(uuid.uuid4()),
            "title": genSong,
            "genre": random.choice(genres),
            "artist": random.choice(artists)["name"],
            "timestamp": genTimestamp
        }
    return song


def generate_artists(genres,days):
    genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
    artist = {
            "artist_id": str(uuid.uuid4()),
            "name": fake.name(),
            "genre": random.choice(genres),
            "timestamp": genTimestamp
        }
    return artist

def generate_genres(n):
    genres = []
    for _ in range(n):
        genres.append(fake.music_genre())
    return genres