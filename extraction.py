import re
import os
import numpy as np
import main
from selenium import webdriver
from tika import parser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import snowball


def text_preproc(x):
    x = x.replace("xbd", " ").replace("xef", " ").replace("xbf", " ") \
        .replace(".", " ").replace(":", " ").replace("\\n"," ") \
        .replace("\\xc2\\xb7", " ").replace("\t", " ").replace("\\", " ") \
        .replace("\\xe2", " ").replace("\\x94", " ").replace("\\x80", " ")
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
    pruned = [stemmer.stem(t.lower()) \
              for t in tokens if re.search(r"^\w", t) and not t.lower() in sw]
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



if __name__ == '__main__':  # MAIN! ESTRAZIONE CONTENUTI PDF E VALUTAZIONE DELLA SOMIGLIANZA

    title_abstract = {}
    keywords = {}
    titles = {}

    path = main.find_path()
    # for per il prelievo di titolo abstract e keywords
    for file_PDF, sub_directory, files in os.walk(path, followlinks=True):
        for file_name in files:

            parsed_pdf = parser.from_file(path + file_name)
            output = parsed_pdf['content']


            with open('output.txt', 'w') as the_file:
                if output: the_file.write(str(output.lower().encode('utf8', errors='ignore')))

            file_output = open("output.txt", "r", encoding="utf8").readline()
            file_output = text_preproc(file_output)

            try:
                titl = re.findall('^.{0,120}', file_output)
                titles[file_name] = titl[0]
                if "abstract" in file_output[:1000]:
                    if "keywords" in file_output and not "index terms" in file_output:
                        abstr = re.findall('abstract(.*?)keywords', file_output)
                        title_abstract[file_name] = abstr[0] + titl[0]
                        keyw = re.findall('keywords(.*?)introduction', file_output)
                        keywords[file_name] = keyw[0]

                    elif "index terms" in file_output:
                        abstr = re.findall('abstract(.*?)index terms', file_output)
                        title_abstract[file_name] = abstr[0] + titl[0]
                        keyw = re.findall('index terms(.*?)introduction', file_output)
                        keywords[file_name] = keyw[0]

                    elif "introduction" in file_output:
                        abstr = re.findall('abstract(.*?)introduction', file_output)
                        title_abstract[file_name] = abstr[0] + titl[0]
                        keywords[file_name] = " "

                    else:
                        print("Non funziona")
                        print(file_name)

                elif "summary" in file_output[:1000]:
                    if "keywords" in file_output and not "index terms" in file_output:
                        abstr = re.findall('summary(.*?)keywords', file_output)
                        title_abstract[file_name] = abstr[0] + titl[0]
                        keyw = re.findall('keywords(.*?)introduction', file_output)
                        keywords[file_name] = keyw[0]

                    elif "index terms" in file_output:
                        abstr = re.findall('summary(.*?)index terms', file_output)
                        title_abstract[file_name] = abstr[0] + titl[0]
                        keyw = re.findall('index terms(.*?)introduction', file_output)
                        keywords[file_name] = keyw[0]

                    elif "introduction" in file_output:
                        abstr = re.findall('summary(.*?)introduction', file_output)
                        title_abstract[file_name] = abstr[0] + titl[0]
                        keywords[file_name] = " "

                    else:
                        print("Non trova nulla")
                        print(file_name)

                else:
                    abstr = re.findall('(.*?)introduction', file_output)
                    title_abstract[file_name] = abstr[0] + titl[0]
                    keywords[file_name] = " "

            except:
                print("Error in filename " + file_name + str(IOError))
                continue

    print("EXTRACTION ENDED SUCCESSFULLY")

    # 1) utilizzo della funzione jaccard per le KEYWORDS

    doc2 = "mobile app evolution, user reviews, mining app stores, empirical study"

    for key in sorted(keywords.keys()):
        string = ""
        # Creates an array of tokenized documents
        # texts.append(title_abstract[key])
        string = string + keywords[key]
        # print(string)
        print("KEYWORD")
        print(jaccard_similarity(string, doc2))
    print("*****************")

    # 2) utilizzo della funzione cosine similarity sul TITOLO e ABSTRACT

    my_abstract = "A major problem with user-written bug reports, indicated by developers and documented by researchers, " \
                  "is the (lack of high) quality of the reported steps to reproduce the bugs. Low-quality steps to " \
                  "reproduce lead to excessive manual effort spent on bug triage and resolution. This paper proposes " \
                  "Euler, an approach that automatically identifies and assesses the quality of the steps to reproduce in " \
                  "a bug report, providing feedback to the reporters, which they can use to improve the bug report. The " \
                  "feedback provided by Euler was assessed by external evaluators and the results indicate that Euler " \
                  "correctly identified 98% of the existing steps to reproduce and 58%of the missing ones, while 73% of " \
                  "its quality annotations are correct "

    print("ABSTRACT+TITOLI")
    print(cos_similarity(my_abstract, title_abstract))

    # 3) utilizzo della funzione cosine similarity sul TITOLO
    my_title = "Who (Self) Admits Technical Debt? Gianmarco Fucci, Fiorella Zampetti University of Sannio, " \
               "Italy {name.surname }@unisannio.it Alexander Serebrenik Eindhoven University of Technology," \
               "The netherlandsa.serebrenik@tue.nl Massimiliano Di Penta University of Sannio, Italy dipenta@unisannio.it "
    print("TITOLI")
    print(cos_similarity(my_title, titles))