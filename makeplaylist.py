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





#to do 
#make playlist collaborative
#add playlist description
#add "by"
#enclosed in [ ]
#maybe replace "the" with " " ----error with arctic monkeys
#when getting a - or by hit, continue with line until period,comma,puncuation -- search AFTER by/-

#duplicate songs




#test cases
#https://www.reddit.com/r/AskReddit/comments/8snzad/whats_a_1010_song_that_most_people_have_probably/
#https://www.reddit.com/r/AskReddit/comments/8kwx1u/whats_the_most_relaxing_song_you_know/
redlink = "https://www.reddit.com/r/AskReddit/comments/8kwx1u/whats_the_most_relaxing_song_you_know"




def add_track(line, id_list):

    searchresults = spotify.search(line,1,0,"track") #get top track from query
    if (searchresults['tracks']['total'] > 0):
        print("got one\n")
        id_list.append( searchresults['tracks']['items'][0]['id'] )
        return

    searchresults = spotify.search(line.replace("."," "),1,0,"track")
    if (searchresults['tracks']['total'] > 0):
        print("got one2\n")
        id_list.append( searchresults['tracks']['items'][0]['id'] )
        return


    line = refine_string(line,".")
    searchresults = spotify.search(line,1,0,"track")
    if (searchresults['tracks']['total'] > 0):
        print("got one2\n")
        id_list.append( searchresults['tracks']['items'][0]['id'] )
        return

    line = refine_string(line,",")
    searchresults = spotify.search(line,1,0,"track")
    if (searchresults['tracks']['total'] > 0):
        print("got one3\n")
        id_list.append( searchresults['tracks']['items'][0]['id'] )
        return

    print("search failed with query: " + line)
    return

#severs line at the first instance of seperator
def refine_string(line, seperator):
    head,sep,tail = line.partition(seperator)
    return head



#returns list of song ids to add
def extract_query(body):

    id_list = []

    lines = body.split('\n')
    for line in lines:
        if re.search("-", line, re.IGNORECASE):
            #search spotify
            print('found - in ::::' + line) #shows what its going to query in spotify
            line = line.replace("-", " ") #removes instances of "-" in song description
            add_track(line, id_list)
        elif re.search(" by ", line, re.IGNORECASE):
            ###need to remove

            print('found by in ::::' + line) #shows what its going to query in spotify
            line = line.replace(" by ", " ") #removes instances of "by" in song description
            print('querying ----- ' + line)
            add_track(line, id_list)



    return id_list;












token = util.prompt_for_user_token('fabioveracrespo','playlist-modify-public playlist-modify-private',client_id='5cb6ee8fca954ef9ba5dc019e3afb467',client_secret='c114b261ff854f3798d95e715a5c6201',redirect_uri='http://google.com/')
spotify = spotipy.Spotify(auth=token)



# Create the Reddit instance
reddit = praw.Reddit('bot1')

# and login....not necessary i think
#reddit.login(spotifyplaylistrobot, itsmethespotifyplaylistrobot)

score_threshold = 10;

song_id_list = [];


post = reddit.submission(url=redlink)  # if you have the URL
for comment in post.comments:
    try: 
            body = comment.body + " " #hacky way of ensuring a string before processing more
            print(str(comment.score) + "   ")

            if (comment.score > score_threshold):
                song_id_list.extend( extract_query(body) )



    except: 
        continue


newplaylist = spotify.user_playlist_create("fabioveracrespo",post.title,public = True)
playlistid = newplaylist['id']

#make collaborative
spotify.user_playlist_change_details("fabioveracrespo", playlistid, post.title, False, True)


#print(song_id_list,sep='\n')
spotify.user_playlist_add_tracks('fabioveracrespo', playlistid, song_id_list)
