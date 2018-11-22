from urllib.request import Request
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
import re
import textwrap
import json
import time
from time import sleep
from tdidf import tfidf
import nltk
from nltk.stem import WordNetLemmatizer
import string

start_time = time.time()

def make_soup(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        page = response.read()
    sleep(0.2)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

#get reviews urls from one page
def get_reviews_urls(input_adress):
    reviews_to_crawl = []
    index = []
    p = re.compile(r'/reviews/+[0-9]*')
    main_page = make_soup(input_adress)
    for review in main_page.find_all("a"):
        reviews_to_crawl.append(review.get('href'))

    for review in reviews_to_crawl:
        if p.fullmatch(str(review)):
            if p.fullmatch(str(review)) not in index:
                index.append(review)
    return index

#gather urls of all reviews and export theme to json file
def export_urls_to_json():
    all_reviews_urls = []
    d = str(datetime.now())
    current_year = d[0:4]
    current_month = d[5:7]

    for year in range(2002, int(current_year) - 1):
        sleep(0.5)
        for month in range(1,12):
            urls_from_month = get_reviews_urls('https://www.residentadvisor.net/reviews.aspx?format=album&yr={0}&mn={1}'.format(year, month))
            for review in urls_from_month:
                if review not in all_reviews_urls:
                    all_reviews_urls.append(review)

    for month in range(1,12):
        sleep(0.5)
        urls_from_month = get_reviews_urls('https://www.residentadvisor.net/reviews.aspx?format=album&yr={0}&mn={1}'.format(current_year, month))
        for review in urls_from_month:
            if review not in all_reviews_urls:
                all_reviews_urls.append(review)

    all_reviews_urls.sort()
    json_file = open('rev_urls.json', 'w')
    json.dump(all_reviews_urls, json_file)

#get review text from review page
def get_review_text(rev_url):
    whole_rev = make_soup('https://www.residentadvisor.net' + rev_url)
    text_content = str(whole_rev.find('span', attrs= {'class' : 'reading-line-height'}).prettify())
    text_content = text_content.rstrip()
    text_content = text_content.replace('\\', '')
    text_content = BeautifulSoup(text_content, 'lxml').text
    text_content = textwrap.fill(text_content)
    return text_content

def get_review_score(rev_url):
    whole_rev = make_soup('https://www.residentadvisor.net' + rev_url)
    score = whole_rev.find('span', attrs= {'itemprop' : 'rating'})
    score = str(score)[39:42]
    return score

#create json dictionary with review url and review content
def export_reviews_to_json(reviews_urls):
    reviews_dict = {}
    break_counter = 0
    counter = 0
    for review_url in reviews_urls:
        sleep(0.2)
        content = get_review_text(review_url)
        content = content.replace('\n', ' ')
        content = content.rstrip()
        reviews_dict[review_url] = content

        break_counter += 1
        counter += 1
        print(counter)
        if break_counter == 10:
            sleep(1)
            break_counter = 0

    with open('reviews.json', 'w') as json_file:
        json.dump(reviews_dict, json_file, )
        json_file.write('\n')



#make list/dict of tokens and lemmatisation
def tokenize_dict(reviews):
    tokenized_reviews = {}
    translator = str.maketrans('', '', string.punctuation)
    wordnet_lemmatizer = WordNetLemmatizer()
    for key, value in reviews.items():
        tokens = nltk.wordpunct_tokenize(value.translate(translator).lower())
        tokens = [wordnet_lemmatizer.lemmatize(token) for token in tokens]
        tokenized_reviews[key] = tokens
    return tokenized_reviews

def tokenize_list(searching_string):
    wordnet_lemmatizer = WordNetLemmatizer()
    searching_tokens = []
    for term in searching_string.split():
        token = wordnet_lemmatizer.lemmatize(term.lower())
        searching_tokens.append(token)
    return searching_tokens

def sort_dict(tfidf_relevant):
    scores = []
    sorted_dict ={}
    for key, value in tfidf_relevant.items():
        scores.append(value)
    scores.sort(reverse = True)
    for score in scores:
        for key, value in tfidf_relevant.items():
            if value == score:
                sorted_dict[key] = value
    return sorted_dict

def get_ra_rate(urls_list):
    rates = {}
    urls_list = list(urls_list)[0:10]
    for rev_url in urls_list:
        whole_rev = make_soup('https://www.residentadvisor.net' + rev_url)
        text_content = str(whole_rev.find('span', attrs={'class': 'rating'}).prettify())
        text_content = text_content.rstrip()
        text_content = text_content.replace('\\', '')
        text_content = BeautifulSoup(text_content, 'lxml').text
        text_content = textwrap.fill(text_content)
        rates['https://www.residentadvisor.net' + rev_url] = float(text_content[2:5])
    return rates

#export functions need to be run only once to download RA's website content to local json files:

def export_scores_to_json(reviews_urls):
    scores_dict = {}
    break_counter = 0
    counter = 0
    for review_url in reviews_urls:
        sleep(0.2)
        score = get_review_score(review_url)
        scores_dict[review_url] = score

        break_counter += 1
        counter += 1
        print(counter)
        if break_counter == 10:
            sleep(1)
            break_counter = 0

    with open('scores.json', 'w') as json_file:
        json.dump(scores_dict, json_file, )
        json_file.write('\n')

#import_urls_to_json()
with open('rev_urls.json', 'r') as reviews_urls_json:
    reviews_urls = json.load(reviews_urls_json)
#export_reviews_to_json(reviews_urls)
with open('reviews.json', 'r') as reviews_json:
    reviews = json.load(reviews_json)
export_scores_to_json(reviews_urls)

