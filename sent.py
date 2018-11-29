from textblob import TextBlob
import random
import json




def blob_sentiment_calculate():
    with open('reviews.json', 'r') as reviews_json:
        reviews = json.load(reviews_json)

    sentiment = {}
    counter = 0
    for key, value in reviews.items():
        blob = TextBlob(value)
        sentiment[key] = blob.sentiment.polarity
        counter += 1
        if counter % 100 == 0:
                print('Calculated sentiment for {} of {} reviews'.format(counter, len(reviews)))

    with open('sentiment.json', 'w') as json_file:
        json.dump(sentiment, json_file)
        json_file.write('\n')


# lists
def load_raw_data():
    reviews = []
    scores = []
    urls = []

    with open('reviews.json', 'r') as reviews_json:
        reviews_dict = json.load(reviews_json)
    for url, content in reviews_dict.items():
        reviews.append(content)
        urls.append(url)
    with open('scores.json', 'r') as scores_json:
        scores_dict= json.load(scores_json)
    for url, content in scores_dict.items():
        scores.append(content)

    return reviews, scores, urls


def scores_to_digits(scores):
    scores[:] = [int(round(float(score))) for score in scores]
    return scores

# split-> fraction of data used for training
def split_data(reviews, scores, urls, split):
    if len(reviews) != len(scores) != len(urls):
        raise ValueError('Inputs has different length.')
    if 0 > split < 1:
        raise ValueError('Split should be in range 0-1')

    train_texts = []
    train_labels = []
    train_urls = []
    validation_texts = []
    validation_labels = []
    validation_urls = []
    indexes = random.sample(range(len(reviews)), round(len(reviews)*split))
    indexes.sort(reverse=True)

    for index in indexes:
        train_texts.append(reviews.pop(index))
        train_labels.append(scores.pop(index))
        train_urls.append(urls.pop(index))

    validation_texts = reviews
    validation_labels = scores
    validation_urls = urls

    if len(validation_texts) != len(validation_labels) != len(validation_urls):
        raise ValueError('Not equally divided (function has error)')

    print(train_texts[100] + train_urls[100])

    return train_texts, train_labels, train_urls, validation_texts, validation_labels, validation_urls



def main():
    reviews, scores, urls =load_raw_data()
    scores = scores_to_digits(scores)
    train_texts, train_labels, train_urls, validation_texts, validation_labels, validation_urls = split_data(reviews, scores, urls, 0.7)



if __name__ == "__main__":
    main()
