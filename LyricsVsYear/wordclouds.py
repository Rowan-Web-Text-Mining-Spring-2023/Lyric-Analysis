import json
import circlify
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = {}
with open('LyricsVsYear/words_years.json', encoding='utf-8') as file:
    data = json.load(file)

def get_colordict(palette,number,start):
    pal = list(sns.color_palette(palette=palette, n_colors=number).as_hex())
    color_d = dict(enumerate(pal, start=start))
    return color_d


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
    for i in range(100):
        top.append(numbers[i])
    
    top_words = []
    for word in output:
        if output[word] in top:
            top_words.append([word, output[word]])
    
    fields = ['word', 'count']

    print(top_words)
    with open('my.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(top_words)

    df = pd.read_csv('my.csv')

    circles = circlify.circlify(df['count'][0:99].tolist(), 
                            show_enclosure=False, 
                            target_enclosure=circlify.Circle(x=0, y=0)
                           )
    
    n = df['count'][0:99].max()
    color_dict=get_colordict('RdYlBu_r', n, 1)

    fig, ax = plt.subplots(figsize=(9,9), facecolor='white')
    ax.axis('off')
    lim = max(max(abs(circle.x)+circle.r, abs(circle.y)+circle.r,) for circle in circles)
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)

    # list of labels
    labels = list(df['word'][0:99])
    counts = list(df['count'][0:99])
    labels.reverse()
    counts.reverse()

    # print circles
    for circle, label, count in zip(circles, labels, counts):
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r, alpha=0.9, color = color_dict.get(count)))
        plt.annotate(label +'\n'+ str(count), (x,y), size=12, va='center', ha='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

choose_year("2021")