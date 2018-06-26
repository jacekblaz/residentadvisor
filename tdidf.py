import math

def tf(terms, tokenized_reviews):
    tf = {}
    for term in terms:
        for key, value in tokenized_reviews.items():
            freq = value.count(term)
            length = len(value)
            tf[(term, key)] = freq / length
    return tf

def idf(terms, tokenized_reviews):
    num_of_docs = len(tokenized_reviews)
    idft = {}
    for term in terms:
        occurences = 0
        for key, value in tokenized_reviews.items():
            if term in tokenized_reviews[key]:
                occurences += 1
        if occurences > 0:
            term_idft = math.log(num_of_docs/occurences)
            idft[term] = term_idft
        else:
            idft[term] = 0
    return idft

def tfidf(terms, tokenized_reviews, reviews_urls):
    tfidf = {}
    term_freqs = tf(terms, tokenized_reviews)
    inverted_freqs = idf(terms, tokenized_reviews)

    for rev in reviews_urls:
        tfidf[rev] = 0

    for term in terms:
        if inverted_freqs[term] > 0:
            for rev_url in reviews_urls:
                term_freq = term_freqs[(term, rev_url)]
                inverted_freq = inverted_freqs[term]
                value = tfidf[rev_url]
                tfidf[rev_url] = value + (term_freq/inverted_freq)
    return tfidf