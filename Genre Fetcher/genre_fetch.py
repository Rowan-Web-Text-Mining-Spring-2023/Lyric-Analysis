import os
from dotenv import load_dotenv
import pymongo
import lyricsgenius as lg
from bs4 import BeautifulSoup
import requests
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
    if j > -1: #Restart number if timeout occurred
        artist = i['track']['artists'][0]['name']
        song = i['track']['name'].split(' (')[0]
        id = i['_id']
        s = genius.search_song(song, artist)
        if s is not None: #Go to webpage of song and parse html to find tags AKA genres
            url = s.url 
            request = requests.get(url)
            soup = BeautifulSoup(request.content, 'html.parser')
            genres = []
            res = soup.find('div', {'class':'SongTags__Container-xixwg3-1 bZsZHM'})
            genres_uncleaned = res.find_all('a')
            for g in genres_uncleaned:
                genre = re.search('>.*<', str(g)).group(0)
                genre = genre.replace('>', '').replace('<', '')
                genres.append(genre)
        col.update_one({'_id': id}, {'$set': {'genres': genres}})
        print(j)
    j+=1