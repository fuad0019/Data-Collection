#https://github.com/ruanbekker/data-generation-scripts/blob/master/generate-random-data-into-elasticsearch.py
#https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
import uuid
import random




def generate_users(fake, n):
    #https://www.w3schools.com/python/python_dictionaries.asp
    gender = ['male', 'female', 'other']
    users = []
    for _ in range(n):
        name = fake.name()
        users.append({
            "_id": str(uuid.uuid4()),
            "name": name,
            "email": fake.ascii_email(),
            "gender": random.choice(gender),
            "country": fake.country(),
            "dob": fake.date_between(start_date='-60y', end_date='-10y').isoformat()
        })
        
    return users
    

def generate_songs(fake, n):
    songs = []
    for _ in range(n):
        genSong = fake.text(max_nb_chars=20)[:-1]
        songs.append(genSong)
    return songs

def generate_songStarted(fake,users,songs,days,n):
    for _ in range(n):
        genUname = fake.slug()
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "_id": genUname,
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp
            }

        return doc

def generate_songSkipped(fake,users,songs,days,n):
    for _ in range(n):
        genUname = fake.slug()
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "_id": genUname,
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,20)
            }

        return doc

def generate_songPausedAndUnpaused(fake,users,songs,days,n):
    for _ in range(n):
        genUname = fake.slug()
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "_id": genUname,
                "user": random.choice(users)["_id"],
                "song": random.choice(songs),
                "timestamp": genTimestamp,
                "duration": random.randint(0,180)
            }

        return doc

def generate_searchQueries(fake,users,days,n):
    for _ in range(n):
        genUname = fake.slug()
        genTimestamp = fake.date_time_between(start_date="-"+str(days)+"d", end_date="now").isoformat()
        doc ={
                "_id": genUname,
                "user": random.choice(users)["_id"],
                "searchterm": fake.text(max_nb_chars=20)[:-1],
                "timestamp": genTimestamp
            }

        return doc


def generate_userIndex(fake,users,days):
   
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

        return doc
