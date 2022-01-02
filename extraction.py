import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import snowball

#ROBERTO

def text_preproc(x):
    x = x.replace("xbd", " ").replace("xef", " ").replace("xbf", " ").replace(".", " ").replace(":", " ").replace("\\n",
                                                                                                                  " ").replace(
        "\\xc2\\xb7", " ").replace("\t", " ").replace("\\", " ").replace("\\xe2", " ").replace("\\x94", " ").replace(
        "\\x80", " ")
    x = x.lower()  # all lowercase
    x = x.encode('ascii', 'ignore').decode()  # Encoding
    x = re.sub(r'https*\S+', ' ', x)  # Remove mentions
    x = re.sub(r'@\S+', ' ', x)  # Remove URL
    x = re.sub(r'#\S+', ' ', x)  # Remove Hashtags
    x = re.sub(r'\'\w+', '', x)  # Remove ticks and the next character
    x = re.sub(r'\w*\d+\w*', '', x)  # Remove numbers
    x = re.sub(r'\s{2,}', ' ', x)  # Replace the over spaces

    return x


def my_tokenizer(text):
    """tokenization function"""
    sw = stopwords.words('english')
    stemmer = snowball.SnowballStemmer(language="english")
    tokens = word_tokenize(text)
    pruned = [stemmer.stem(t.lower()) for t in tokens if re.search(r"^\w", t) and not t.lower() in sw]
    return pruned


def cos_similarity(input_query, section):
    texts = []
    for key in sorted(section.keys()):
        # Creates an array of tokenized documents
        texts.append(section[key])
    vectorizer = CountVectorizer(tokenizer=my_tokenizer)
    # creates the model
    model = vectorizer.fit_transform(texts)
    # adds a query to the model
    query = vectorizer.transform([input_query])
    cos = cosine_similarity(query, model)
    print(np.mean(cos))
    print(np.max(cos))


def jaccard_similarity(doc1, doc2):
    # List the unique words in a document
    words_doc1 = set(doc1.lower().replace(",", "").split())
    words_doc2 = set(doc2.lower().replace(",", "").split())

    # Find the intersection of words list of doc1 & doc2
    intersection = words_doc1.intersection(words_doc2)

    # Find the union of words list of doc1 & doc2
    union = words_doc1.union(words_doc2)

    # Calculate Jaccard similarity score
    # using length of intersection set divided by length of union set
    return float(len(intersection)) / len(union)