from flask import Flask, jsonify, render_template, request
import uuid
import random
from faker import Faker
from faker_music import MusicProvider
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

count = 0
fake = Faker()
fake.add_provider(MusicProvider)



def generate_song(n,days, artists):

    songs_temp = []

    for _ in range(n):

    
        genSong = fake.text(max_nb_chars=20)[:-1]
        genTimestamp = fake.date_time_between(start_date="-" + str(days) + "d", end_date="now").isoformat()

        song = {
            "title": genSong,
            "song_id": str(uuid.uuid4()),
            "genre": fake.music_genre(),
            "artist": random.choice(artists)["name"],
            "timestamp": genTimestamp
            }
        songs_temp.append(song)

    return songs_temp


def generate_artist(n,days):

    artists_temp = []

    for _ in range(n):

        genTimestamp = fake.date_time_between(start_date="-" + str(days) + "d", end_date="now").isoformat()
        artist = {
            "artist_id": str(uuid.uuid4()),
            "name": fake.name(),
            "genre": fake.music_genre(),
            "timestamp": genTimestamp
        }
        artists_temp.append(artist)

    return artists_temp
        

artists = generate_artist(10,10)
songs = generate_song(40,10,artists)

@app.route('/get/artist/all')
def get_users():

    return jsonify(artists)

@app.route('/get/song/all')
def get_songs():

    return jsonify(songs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
