from os import read
import pytest
import json
import urllib.request

#problem: the test do run in parallel
#globaluserid = "0b192a8d-ada6-4b8f-9bb2-44a82e01e52d"
#globaluserid = ""
#songid = ""

def test_home():
    #check if return code? html?
    print("to do: home line 27")


def test_getUsers():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users')
    output = testing.read().decode('utf-8')
    assert "_id" in output
    assert "age" in output
    assert "country" in output
    assert "dob" in output
    assert "email" in output
    assert "gender" in output
    assert "name" in output

def test_get_user_profile():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users')
    output = testing.read().decode('utf-8')
    
    idstart = output.find("_id")+7
    idend = output.find("age")-9
    userid = output[idstart:idend]

    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/'+userid)
    output = testing.read().decode('utf-8')

    assert "_id" in output
    assert "age" in output
    assert "country" in output
    assert "dob" in output
    assert "email" in output
    assert "gender" in output
    assert "name" in output

def test_get_history():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users')
    users = testing.read().decode('utf-8')

    found = False
    while(not found):
        idstart = users.find("_id")+7
        idend = users.find("age")-9
        userid = users[idstart:idend]

        print(userid)

        testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/'+userid+'/songs')
        output = testing.read().decode('utf-8')
        if(len(output) > 8):
            found=True
        else:
            users = users[idend+20:len(users)]
    global globaluserid
    globaluserid = userid

    assert "song" in output
    assert "artist" in output
    assert "genre" in output
    assert "title" in output
    assert "timestamp" in output


''' index not found
def test_get_search_history():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/'+globaluserid+'/searches')
    songs = testing.read().decode('utf-8')

    assert "searchterm" in output
    assert "timestamp" in output
'''

def test_amount_song_played_by_user():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/'+globaluserid+'/songs')
    songs = testing.read().decode('utf-8')
    
    idstart = songs.find("title")+9
    idend = songs.find("timestamp")-15
    songname = songs[idstart:idend]

    songname = songname.replace(" ", "%20")
    global globalsong
    globalsong = songname
    
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/'+globaluserid+'/songs/'+songname+'/amount_played')
    output = testing.read().decode('utf-8')
    assert "plays" in output

def test_amount_artist_played_by_user():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/'+globaluserid+'/songs')
    songs = testing.read().decode('utf-8')
    
    idstart = songs.find("artist")+10
    idend = songs.find("genre")-11
    artistname = songs[idstart:idend]

    artistname = artistname.replace(" ", "%20")
    global globalartist
    globalartist = artistname
    
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01//users/'+globaluserid+'/artists/'+artistname+'/amount_played')
    output = testing.read().decode('utf-8')
    
    assert "plays" in output

def test_amount_song_played():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/songs/'+globalsong+'/amount_played')
    output = testing.read().decode('utf-8')
    assert "plays" in output

def test_artist_amount_played():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/artists/'+globalartist+'/amount_played')
    output = testing.read().decode('utf-8')
    assert "plays" in output
'''
def test_ad_amount_clicked():
    delete?
'''
def test_get_top_songs():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/songs/top')
    output = testing.read().decode('utf-8')
    assert "plays" in output
    assert "song" in output

def test_get_top_artists():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/artists/top')
    output = testing.read().decode('utf-8')
    assert "artist" in output
    assert "plays" in output

def test_get_top_artist_for_user():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/' +globaluserid+ '/artists/top')
    output = testing.read().decode('utf-8')
    assert "artist" in output
    assert "plays" in output

''' KeyError: 'artists'
def test_get_top_songs_for_user():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/' +globaluserid+ '/songs/top')
    output = testing.read().decode('utf-8')
    assert "song" in output
    assert "plays" in output
'''
def test_get_top_genres_for_user():
    testing = urllib.request.urlopen('http://opensuse.stream.stud-srv.sdu.dk/service01/users/' +globaluserid+ '/genres/top')
    output = testing.read().decode('utf-8')
    assert "genre" in output
    assert "plays" in output

def test_get_advertisements_amount_clicked():
    print('help: how to get ad ids')

def test_get_namespace_log():
    print('help: HELP')
'''
def test_get_genres_recommendation_for_user():
    id = 1
    #output = json.dumps(Docker.api.flaskapi.get_genres_recommendation_for_user(id))
    test = "{\"title\": \"temp\", \"genre\": \"temp\", \"artist\": \"temp\"\"}"
    output = json.dumps(test)
    assert "title" in output
    assert "genre" in output
    assert "artist" in output

def test_get_artist_recommendation_for_user():
    id = 1
    #output = json.dumps(Docker.api.flaskapi.get_artist_recommendation_for_user(id))
    test = "{\"artist_name\": \"temp\", \"genre\": \"temp\"\"}"
    output = json.dumps(test)
    assert "artist_name" in output
    assert "genre" in output
'''
def test_get_user_recommendations_genres():
    print('no output?')

print("1")
test_home()
test_getUsers()
test_get_user_profile()
test_get_history()
#test_get_search_history()
test_amount_song_played_by_user()
test_amount_artist_played_by_user()
test_amount_song_played()
test_artist_amount_played()
#test_ad_amount_clicked()
test_get_top_songs()
test_get_top_artists()
test_get_top_artist_for_user()
#test_get_top_songs_for_user()
test_get_top_genres_for_user()
#test_get_genres_recommendation_for_user()
#test_get_artist_recommendation_for_user()
test_get_advertisements_amount_clicked()
test_get_namespace_log()
test_get_user_recommendations_genres()
print("2")
