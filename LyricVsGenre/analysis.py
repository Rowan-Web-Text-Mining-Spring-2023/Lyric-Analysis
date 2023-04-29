import os
from dotenv import load_dotenv
import pymongo
import contractions
import re
import json
import nltk
import demoji
from unicodedata import normalize


nltk.download('stopwords')
stops_en = nltk.corpus.stopwords.words('english')

with open('new_stops.txt') as file:
    new_stops = []
    for line in file:
        new_stops.append(line.strip())
    stops_en.extend(new_stops)

#Function to remove special characters
to_remove = ['(', ')', '"', '?', '!', '-', ',']
def remove_extra(word):
    for r in to_remove:
        word = word.replace(r, '').replace('\n', ' ').replace('\t', ' ')
    return word

def remove_stopwords(value):
    remove_stops = ''
    words = value.split(' ')
    for word in words:
        if word not in stops_en: 
            remove_stops = remove_stops + word + ' '
    return remove_stops

#Create Connection to database
load_dotenv()
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client['test']
col = db['playlistitemsschemas']

#Load valid genres
with open('LyricVsGenre/genres.json', encoding='utf-8') as file:
    genres = json.load(file)

genre_count = {}
for g in genres:
    genre_count[g] = 0

#Go through each song and store each unique word
words = []  #List of all words
pairs = []  #Combination of lyrics and year, used later
rec = col.find({}, {})
for song in rec:
    track = song["genres"]
    track_valid = []
    for t in track:
        if t in genres:
            track_valid.append(t)
    if 'Lyrics' in song['lyrics']:
        lyrics = contractions.fix(song['lyrics'].split('Lyrics')[1].lower()) #Remove contractions and get rid of header area with languages
        lyrics = re.sub('[.*?]', '', lyrics) #Remove text such as [Chorus] or [Verse 1]
        lyrics = remove_extra(lyrics) #Remove special characters
        lyrics = demoji.replace(lyrics, "")
        t = normalize('NFKD', lyrics).encode('ascii', 'ignore')
        lyrics = t.decode()
        lyrics = remove_stopwords(lyrics)
        lyrics_words = lyrics.split()
        for word in lyrics_words:
            if word not in words:
                words.append(word)
        pairs.append([lyrics, track_valid])
        for t in track_valid:
            genre_count[t] += len(lyrics_words)

with open('test.json', 'w') as file:
    json.dump(genres, file)

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
with open('LyricVsGenre/words_genres.json', 'w') as f:
    json.dump(data, f)
with open('LyricVsGenre/genres_count.json', 'w') as f:
    json.dump(genre_count, f)