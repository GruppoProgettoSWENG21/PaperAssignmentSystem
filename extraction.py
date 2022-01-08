import re
import os
import io
import numpy as np
import main
from tika import parser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import snowball


def text_preproc(x):
    x = x.replace("xbd", " ").replace("xef", " ").replace("xbf", " ") \
        .replace(".", " ").replace(":", " ").replace("\\n", " ") \
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
    """Funzione di cosine similarity fatta tra la query e i documenti"""

    texts = []
    values = []

    for key in sorted(section.keys()):
        # Creates an array of tokenized documents
        texts.append(section[key])
    for key_query in sorted(input_query.keys()):
        vectorizer = CountVectorizer(tokenizer=my_tokenizer)
        # creates the model
        model = vectorizer.fit_transform(texts)
        # adds a query to the model
        query = vectorizer.transform([input_query[key_query]])
        cos = cosine_similarity(query, model)
        values.append(cos)

    media = np.mean(values)
    massimo = np.max(values)

    return media, massimo


def jaccard_similarity(input_query_key, section_keyword):
    values_keywords = []
    for input_key in sorted(input_query_key.keys()):
        for section_key in sorted(section_keyword.keys()):
            # List the unique words in a document
            words_doc1 = set(input_query_key[input_key].lower().replace(",", "").split())
            words_doc2 = set(section_keyword[section_key].lower().replace(",", "").split())

            # Find the intersection of words list of doc1 & doc2
            intersection = words_doc1.intersection(words_doc2)

            # Find the union of words list of doc1 & doc2
            union = words_doc1.union(words_doc2)

            # Calculate Jaccard similarity score
            # using length of intersection set divided by length of union set
            if not len(union) == 0:
                values_keywords.append((float(len(intersection)) / len(union)))
            else:
                values_keywords.append(0.0)

    massimo_keyword = np.max(values_keywords)

    return massimo_keyword


if __name__ == '__main__':  # MAIN! ESTRAZIONE CONTENUTI PDF E VALUTAZIONE DELLA SOMIGLIANZA

    autori = []
    author_title_abstact = {}
    author_keywords = {}
    author_titles = {}

    path = main.find_path()
    # for per il prelievo di titolo abstract e keywords
    for file_PDF, sub_directory, files in os.walk(path, followlinks=True):
        for my_directory in sub_directory:
            title_abstract = {}
            keywords = {}
            titles = {}
            my_path = path + my_directory + "\\"
            author_name = my_directory
            for sub_filePDF, sub_dir, sub_files in os.walk(my_path, followlinks=True):
                for file_name in sub_files:

                    parsed_pdf = parser.from_file(my_path + file_name)
                    output = parsed_pdf['content']

                    with io.open('output.txt', 'w', encoding='utf8') as the_file:
                        if output:
                            the_file.write(str(output.lower().encode('utf8', errors='ignore')))

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

            author_title_abstact[author_name] = title_abstract
            author_keywords[author_name] = keywords
            author_titles[author_name] = titles
            autori.append(author_name)

    print("EXTRACTION ENDED SUCCESSFULLY")


# 1) utilizzo della funzione jaccard per le KEYWORDS
massimo_keywords = []
for key in sorted(author_keywords.keys()):
    if not "Massimiliano Di Penta" in key:
        max = jaccard_similarity(author_keywords[key], author_keywords["Massimiliano Di Penta"])
        print(key + " --------> " + str(max))
        massimo_keywords.append(max)

print("********************************")
print()
