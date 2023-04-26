import json


data = {}
with open('LyricsVsYear/words_years.json', encoding='utf-8') as file:
    data = json.load(file)

counts = {}
with open('LyricsVsYear/year_counts.json', encoding='utf-8') as file:
    counts = json.load(file)

years = []
with open('LyricsVsYear/years.json', encoding='utf-8') as file:
    years = json.load(file)

def predict(lyrics):
    lyrics_list = lyrics.split(' ')

    years_percent = {}
    for year in years:
        years_percent[year] = 1999999
    
    for word in lyrics_list:
        if word in data:
            result = data[word]
            #print(result)
            for year in result:
                total = counts[year]
                count = data[word][year]
                years_percent[year] = years_percent[year] * (count/total) * 100
                

    high1 = 0
    high2 = 0
    high3 = 0
    highest = []
    total = 0

    for year in years_percent:
        total += years_percent[year]
        if years_percent[year] > high1:
            high1 = years_percent[year]
    
    for year in years_percent:
        if years_percent[year] > high2 and years_percent[year] < high1:
            high2 = years_percent[year]
    
    for year in years_percent:
        if years_percent[year] > high3 and years_percent[year] < high1 and years_percent[year] < high2:
            high3 = years_percent[year]

    for year in years_percent:
        if years_percent[year] == high1 or years_percent[year] == high2 or years_percent[year] == high3:
            highest.append([year, years_percent[year]])

    tmp = []
    tmp.append([highest[0][0], str(highest[0][1]/total*100)+'%'])
    tmp.append([highest[1][0], str(highest[1][1]/total*100)+'%'])
    tmp.append([highest[2][0], str(highest[2][1]/total*100)+'%'])

    return(tmp)

print(predict('you know, young rich niggas you know so we ain\'t really had no old money'))