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
                genre_percent[genre] = genre_percent[genre] * (count/total) * 100

    high1 = 0
    high2 = 0
    high3 = 0
    highest = []
    total = 0

    for genre in genre_percent:
        total += genre_percent[genre]
        if float(genre_percent[genre]) > high1:
            high1 = genre_percent[genre]

    for genre in genre_percent:
        if high2 < float(genre_percent[genre]) < high1:
            high2 = genre_percent[genre]

    for genre in genre_percent:
        if high3 < float(genre_percent[genre]) < high2 < float(genre_percent[genre]) < high1:
            high3 = genre_percent[genre]

    for genre in genre_percent:
        if genre_percent[genre] == high1 or genre_percent[genre] == high2 or genre_percent[genre] == high3:
            highest.append([genre, genre_percent[genre]])

    tmp = []
    tmp.append([highest[0][0], str(highest[0][1]/total*100)+'%'])
    tmp.append([highest[1][0], str(highest[1][1] / total*100)+'%'])
    tmp.append([highest[2][0], str(highest[2][1] / total*100)+'%'])

    return tmp

print(predict('on a dark desert highway cool wind though my hair'))
