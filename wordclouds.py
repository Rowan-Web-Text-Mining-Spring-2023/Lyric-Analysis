import json
import circlify

data = {}
with open('LyricsVsYear/words_years.json', encoding='utf-8') as file:
    data = json.load(file)

def choose_year(year):
    output = {}
    for word in data:
        output[word] = data[word][year]
        #print(output[word])
    
    numbers = []
    for word in output:
        #print(output[word])
        numbers.append(int(output[word]))
    
    numbers.sort()
    numbers.reverse()
    top = []
    for i in range(200):
        top.append(numbers[i])
    
    top_words = []
    for word in output:
        if output[word] in top:
            top_words.append([word, output[word]])
    
    print(top_words)



choose_year("2021")