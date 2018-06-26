import sklearn.preprocessing
import numpy as np
import json
import matplotlib.pyplot as plt

with open('sentiment.json', 'r') as sentiment_json:
    sentiment = json.load(sentiment_json)

all_sentiments_list = []
for key, value in sentiment.items():
    all_sentiments_list.append(value)

sentiments = np.asarray(all_sentiments_list)
sentiments /= np.max(np.abs(sentiments),axis=0)

with open('scores.json', 'r') as scores_json:
    scores = json.load(scores_json)


all_scores_list = []
for key, value in scores.items():
    print(key)
    all_scores_list.append(float(value))

scores = np.asarray(all_scores_list)
scores /= np.max(np.abs(scores),axis=0)

difference = scores - sentiments
difference = np.average(difference)
sentiments = sentiments
print(difference)
print(len(all_scores_list))
plt.figure()
#plt.errorbar(scores,sentiments, fmt = 'o')
plt.plot(sentiments)
plt.plot(scores)
plt.show()