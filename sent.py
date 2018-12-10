from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
import random
import json

from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Input, Dense
from keras.optimizers import Adam



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
        scores_dict = json.load(scores_json)
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
    indexes = random.sample(range(len(reviews)), round(len(reviews) * split))
    indexes.sort(reverse=True)

    for index in indexes:
        train_texts.append(reviews.pop(index))
        train_labels.append(scores.pop(index))
        train_urls.append(urls.pop(index))

    validation_texts = reviews
    validation_labels = scores
    validation_urls = urls

    if len(validation_texts) != len(validation_labels) != len(validation_urls):
        raise ValueError('Data stets are not equally divided (split_data function has a bug)')

    return train_texts, train_labels, train_urls, validation_texts, validation_labels, validation_urls


def count_vectors(train_texts, validation_texts):
    all_texts = train_texts + validation_texts
    count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}', strip_accents='unicode')
    count_vect.fit(all_texts)

    train_vector = count_vect.transform(train_texts)
    validation_vector = count_vect.transform(validation_texts)

    return train_vector, validation_vector


def preprocessing():
    reviews, scores, urls = load_raw_data()
    scores = scores_to_digits(scores)
    print('Creating datasets')
    train_texts, train_labels, train_urls, validation_texts, validation_labels, validation_urls = split_data(reviews,
                                                                                                             scores,
                                                                                                             urls, 0.7)
    print('Vectorizing texts')
    train_vector, validation_vector = count_vectors(train_texts, validation_texts)
    print('Preprocessing is done')

    # targets should be in categorical format (e.g. if you have 10 classes, the target for each sample should be a
    # 10-dimensional vector that is all-zeros except for a 1). For categorical crossentropy loss
    train_labels = to_categorical(train_labels, num_classes=None)
    validation_labels = to_categorical(validation_labels, num_classes=None)

    return train_vector, train_labels, validation_vector, validation_labels


def shallow_network_architecture(num_dim, train_vector, train_labels, validation_vector, validation_labels):
    model = Sequential()
    model.add(Dense(100, activation='relu', input_dim=num_dim))
    model.add(Dense(6, activation="softmax"))

    model.compile(optimizer=Adam(),
                       loss='categorical_crossentropy',
                       metrics=['accuracy'])

    model.fit(train_vector, train_labels, epochs=5, batch_size=32)
    loss_and_metrics = model.evaluate(validation_vector, validation_labels, batch_size=128)
    print("Validation {}: {}".format(model.metrics_names[1], loss_and_metrics[1]))

def main():
    train_vector, train_labels, validation_vector, validation_labels = preprocessing()
    num_dim = train_vector.shape[1]
    shallow_network_architecture(num_dim, train_vector, train_labels, validation_vector, validation_labels)
if __name__ == "__main__":
    main()
