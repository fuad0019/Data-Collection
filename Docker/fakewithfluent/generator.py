#https://github.com/ruanbekker/data-generation-scripts/blob/master/generate-random-data-into-elasticsearch.py
#https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
import uuid
import random
from faker import Faker
from faker_music import MusicProvider
from datetime import datetime
from dateutil.relativedelta import relativedelta


fake = Faker()


def generate_countries(n):
    countries = []
    for _ in range(n):
        countries.append(fake.country())
    return countries

def generate_userCreated(days, countries):
    #https://www.w3schools.com/python/python_dictionaries.asp
    gender = ['male', 'female', 'other']

    genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
    dob = fake.date_between(start_date='-60y', end_date='-10y').isoformat()
    name = fake.name()
    doc = {
            "event": "userCreated",
            "userid": str(uuid.uuid4()),
            "name": name,
            "email": fake.ascii_email(),
            "gender": random.choice(gender),
            "country": random.choice(countries),
            "dob": dob,
            "age": str(relativedelta(datetime.today(), fake.date_between(start_date='-60y', end_date='-10y')).years),
            "timestamp": genTimestamp
        }
        
    return doc
    

def generate_songs(n, artists):
    
    fake.add_provider(MusicProvider)
    songs = []
    for _ in range(n):
        genSong = fake.text(max_nb_chars=20)[:-1]
        songs.append({
            "title": genSong,
            "genre": fake.music_genre(),
            "artist": random.choice(artists)
        })
    return songs

def generate_artists(n):
    artists = []
    for _ in range(n):
        artists.append(fake.name())
    return artists


def gen_artist(days):
    genTimestamp = fake.date_time_between(start_date="-" + str(days) + "d", end_date="now").isoformat()
    doc = {
        "event": "artistCreated",
        "artist_id": str(uuid.uuid4()),
        "name": fake.name(),
        "genre": fake.music_genre(),
        "timestamp": genTimestamp
    }
    return doc

def gen_song(days, artists):
    fake.add_provider(MusicProvider)
    genTimestamp = fake.date_time_between(start_date="-" + str(days) + "d", end_date="now").isoformat()
    genSong = fake.text(max_nb_chars=20)[:-1]
    doc = {
        "event": "songCreated",
        "song_id": str(uuid.uuid4()),
        "title": genSong,
        "genre": fake.music_genre(),
        "artist": random.choice(artists),
        "timestamp": genTimestamp
    }
    return doc

def generate_songStarted(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "songStarted",
                "user": random.choice(users)["userid"],
                "song": random.choice(songs),
                "timestamp": genTimestamp
            }

        return doc

def generate_songSkipped(users,songs,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "songSkipped",
                "user": random.choice(users)["userid"],
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
                "user": random.choice(users)["userid"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,180)
            }

        return doc

def generate_searchQueries(users,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "search",
                "user": random.choice(users)["userid"],
                "searchterm": fake.text(max_nb_chars=20)[:-1],
                "timestamp": genTimestamp
            }

        return doc

def generate_adClicks(users,days):
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "event": "adclicks",
                "user": random.choice(users)["userid"],
                "ad": str(uuid.uuid4()),
                "timestamp": genTimestamp
            }

        return doc
