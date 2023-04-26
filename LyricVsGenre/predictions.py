import json
import re
import math

counts = {}
data = {}
genres = []

with open('genres_count.json', encoding='utf-8') as file:
    counts = json.load(file)

with open('words_genres.json', encoding='utf-8') as file:
    data = json.load(file)

with open('genres.json', encoding='utf-8') as file:
    genres = json.load(file)


def predict(lyrics):
    lyrics_list = lyrics.split(' ')
    genre_percent = {}
    for genre in genres:
        genre_percent[genre] = 1

    for word in lyrics_list:
        if word in data:
            result = data[word]
            for genre in result:
                total = counts[genre]
                count = data[word][genre]
                genre_percent[genre] = genre_percent[genre] * (count / total) * 100

    total = 0

    for genre in genre_percent:
        total += genre_percent[genre]

    genre_lists = []
    for genre in genre_percent:
        genre_lists.append([genre, genre_percent[genre]/total * 100])

    genre_lists.sort(key=lambda x: x[1], reverse=True)

    return genre_lists[:3]


print(predict('on a dark desert highway cool wind though my hair'))
