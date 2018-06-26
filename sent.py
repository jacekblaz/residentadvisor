import json
from wyszukiwarka import tokenize_dict
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

with open('reviews.json', 'r') as reviews_json:
    reviews = json.load(reviews_json)

sentiment = {}

for key, value in reviews.items():
    blob = TextBlob(value)
    sentiment[key] = blob.sentiment.polarity

with open('sentiment.json', 'w') as json_file:
    json.dump(sentiment, json_file)
    json_file.write('\n')