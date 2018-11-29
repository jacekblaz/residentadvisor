from sklearn import preprocessing
import numpy as np
import json
import matplotlib.pyplot as plt
import random

def open_files():
    with open('sentiment.json', 'r') as sentiment_json:
        sentiment = json.load(sentiment_json)

    all_sentiments_list = []
    for key, value in sentiment.items():
        all_sentiments_list.append(value)

    sentiments = np.asarray(all_sentiments_list)

    with open('scores.json', 'r') as scores_json:
        scores = json.load(scores_json)

    all_scores_list = []
    for key, value in scores.items():
        all_scores_list.append(float(value))

    scores = np.asarray(all_scores_list)
    scores = np.interp(scores, (scores.min(), scores.max()), (-1, +1))
    return sentiments, scores


def calculate_stats_and_plots(sentiments, scores):
    total_diff = 0
    scores_is_higher = 0
    for index in range(0,len(scores)):
        total_diff += abs(scores[index] - sentiments[index])
        if scores[index] > sentiments[index]:
            scores_is_higher += 1

    def score_in_range(diffrence):
        scores_in_range = 0
        for index in range(0,len(scores)):
            if abs(scores[index] - sentiments[index]) < diffrence/2.5:
                scores_in_range += 1
        return scores_in_range
    differences = []
    score_names = [0.0, 0.2, 0.4, 0.6, 0.8, 1, 1.5, 2, 3, 4, 5]
    for i in score_names:
        differences.append(score_in_range(i)/len(scores)*100)

    scores_above_avg = 0
    for score in scores:
        if score > np.average(scores):
            scores_above_avg += 1

    sentiments_above_avg = 0
    for sent in sentiments:
        if sent > np.average(sentiments):
            sentiments_above_avg += 1
    print("procent recenzji gdzie ocena portalu jest wyzsza od sentymentu" +': ' + str(scores_is_higher/index*100) + '%')
    print('srednia sentymentu (skala -1 do 1): ' + str(np.average(sentiments)) + '\n' 'srednia oceny z portalu (skala -1 do 1): ' + str(np.average(scores)))
    print('srednia roznica: ' + str(total_diff/len(scores)))
    print('procent recenzji ktorych roznica miedzy sentymentem a ocena mniejsza niz 1 (skala 1-5): ' + str(score_in_range(0.2)/len(scores)*100))
    print('ilosc ocen powyzej sredni: ' + str(scores_above_avg))
    print('ilosc sentymentow powyzej sredniej: ' + str(sentiments_above_avg))
    print('ilosc recenzji: ' + str(len(scores)) + '\n' + str(len(sentiments)))


    #how big is difference plot
    plt.figure(1, figsize=(9,3))
    plt.xlim(right=2.2)
    plt.bar(score_names, differences, width = 0.1)
    plt.suptitle('Sentiment analysis accuracy')
    plt.xlabel('Scores difference smaller than')
    plt.ylabel('Percent of reviews')

    #scatter for scores and sentiments
    plt.figure(2)
    plt.subplot(211)
    plt.title('Scores from RA')
    plt.ylabel('Review number')
    plt.xlabel('RA score')
    plt.scatter(scores, range(0,len(scores)))

    plt.subplot(212)
    plt.title('Scores from sentiment analysis')
    plt.ylabel('Review number')
    plt.xlabel('Sentiment analysis score')
    plt.scatter(sentiments, range(0,len(sentiments)))



    plt.figure(3)
    plt.title('Histogram')
    plt.subplot(211)
    plt.title('Histogram RA')
    plt.xlabel('Score interval')
    plt.ylabel('Amount of reviews')
    plt.hist(scores,bins = np.linspace(-1,1,20))
    plt.subplot(212)
    plt.title('Histogram sentiment analysis')
    plt.xlabel('Score interval')
    plt.ylabel('Amount of reviews')
    plt.hist(sentiments, bins=np.linspace(-1,1,20))

    plt.show()

def show_stats_and_plots():
    sentiments, scores = open_files()
    calculate_stats_and_plots(sentiments, scores)

if __name__ == "__main__":
    show_stats_and_plots()