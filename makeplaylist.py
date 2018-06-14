#!/usr/bin/python
import praw
import pdb
import re
import os

#spotify dependencies
import json
import pprint
import spotipy
import spotipy.util as util






#returns list of song ids to add
def extract_query(body):

    id_list = []

    lines = body.split('\n')
    for line in lines:
        if re.search("-", line, re.IGNORECASE):
            #search spotify
            print('found - in ::::' + line + '\n') #shows what its going to query in spotify
            searchresults = spotify.search(line,1,0,"track")
            if (searchresults['tracks']['total'] > 0):
                id_list.append( searchresults['tracks']['items'][0]['id'] )
                





    return id_list;









token = util.prompt_for_user_token('fabioveracrespo','playlist-modify-public',client_id='5cb6ee8fca954ef9ba5dc019e3afb467',client_secret='c114b261ff854f3798d95e715a5c6201',redirect_uri='http://google.com/')
spotify = spotipy.Spotify(auth=token)



# Create the Reddit instance
reddit = praw.Reddit('bot1')

# and login....not necessary i think
#reddit.login(spotifyplaylistrobot, itsmethespotifyplaylistrobot)

score_threshold = 20;

song_id_list = [];


post = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/8kwx1u/whats_the_most_relaxing_song_you_know/')  # if you have the URL
for comment in post.comments:
    try: 
            body = comment.body + " " #hacky way of ensuring a string before processing more
            print(str(comment.score) + "   ")

            if (comment.score > score_threshold):
                song_id_list.extend( extract_query(body) )



    except: 
        print("exception raised bitch")


newplaylist = spotify.user_playlist_create("fabioveracrespo","newplaylistyall", public = True)
playlistid = newplaylist['id']

print(*song_id_list,sep='\n')
spotify.user_playlist_add_tracks('fabioveracrespo', playlistid, song_id_list)


