import os
from dotenv import load_dotenv
import pymongo
import lyricsgenius as lg
import re

#Genius api for lyrics
api_key= '_MHF5MqhYdAj3Tk3JLx9atl02VFY1tsAaoLPBju4cPEJh0CUw8H3mVbUaD_G9W5tWGPUhO31oqd9n9NLBZsMqQ'
genius = lg.Genius(api_key)
genius.timeout = 15

#Create Connection to database
load_dotenv()
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client['test']
col = db['playlistitemsschemas']

#Go through each song and get lyrics to store in database\
j = 0
rec = col.find({}, {})
for i in rec:
    if j > 698: #Restart number if timeout occurred
        artist = i['track']['artists'][0]['name']
        song = i['track']['name'].split(' (')[0]
        id = i['_id']
        s = genius.search_song(song, artist)
        if s is None:
            lyr = "Not found or contains no lyrics(instrumental)"
        else:
            lyr = s.lyrics
        col.update_one({'_id': id}, {'$set': {'lyrics': lyr}})
        print(j)
    j+=1