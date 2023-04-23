import os
from dotenv import load_dotenv
import pymongo
import contractions
import re
import json

#Function to remove special characters
to_remove = ['(', ')', '"', '?', '!', '-', ',']
def remove_extra(word):
    for r in to_remove:
        word = word.replace(r, '')
    return word

#Create Connection to database
load_dotenv()
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client['test']
col = db['playlistitemsschemas']

#Go through each song and store each unique word
words = []  #List of all words
genres = []  #List of every year present
pairs = []  #Combination of lyrics and year, used later
rec = col.find({}, {})
for song in rec:
    track = song["genres"]
    for i in track:
        if i not in genres:
            genres.append(i)
    if 'Lyrics' in song['lyrics']:
        lyrics = contractions.fix(song['lyrics'].split('Lyrics')[1].lower()) #Remove contractions and get rid of header area with languages
        lyrics = re.sub('[.*?]', '', lyrics) #Remove text such as [Chorus] or [Verse 1]
        lyrics = remove_extra(lyrics) #Remove special characters
        lyrics_words = lyrics.split()
        for word in lyrics_words:
            if word not in words:
                words.append(word)
        pairs.append([lyrics, track])


#Fill map with keys of each year and each value of every present year and the count of the word to 0
data = {}
for word in words:
    genre_t = {}
    for genre in genres:
        genre_t[genre] = 0
    data[word] = genre_t

#Go through each song and count each occurence of every word, updates based on the corresponding year of the song
for song in pairs:
    for word in words:
        tmp = song[1]
        for i in tmp:
            data[word][i] += song[0].count(word)

#Save all data to json file
with open('LyricsVsGenre/words_genres.json', 'w') as f:
    json.dump(data, f)