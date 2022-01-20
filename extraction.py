import re
import os
import platform
import getpass
import io
import numpy as np
import pandas as pd
import nltk
nltk.download('popular')
from tika import parser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import snowball
from tabulate import tabulate
from PyPDF2 import PdfFileReader


def find_path_for_extraction():

    """
        Funzione che mi permette di ottenere il path dove sono presenti i pdf dei possibili revisori e dei pdf da assegnare

        :return path: path in cui sono presenti i pdf da valutare

    """

    path = ""
    so = platform.system()
    print("Il sistema operativo è: " + so)

    username = getpass.getuser()
    print("L'utente è: " + username)

    if so == "Windows":
        path = "C:\\Users\\" + username + "\\Desktop\\PDFRidotti\\"
        print(path)
    elif so == "Mac OS X":
        path = "/Users/" + username + "/Desktop/FilePDF"
        print(path)
    elif so == "Linux":
        path = "/home/" + username + "/Desktop/FilePDF"

    return path

def text_preproc(x):


    """
    Preprocessing function

        :param x: stringa su cui effettuare il preprocessing
        :return x: stringa

    """
    x = x.replace("xbd", " ").replace("xef", " ").replace("xbf", " ") \
        .replace(".", " ").replace(":", " ").replace("\\n", " ") \
        .replace("\\xc2\\xb7", " ").replace("\t", " ").replace("\\", " ") \
        .replace("\\xe2", " ").replace("\\x94", " ").replace("\\x80", " ")
    x = x.lower()  # all lowercase
    x = x.encode('ascii', 'ignore').decode()  # Encoding
    x = re.sub(r'https*\S+', ' ', x)  # Remove mentions
    x = re.sub(r'@\S+', ' ', x)  # Remove URL
    x = re.sub(r'#\S+', ' ', x)  # Remove Hashtags
    x = re.sub(r'\'\w+', '', x)  # Remove ticks and the next word
    x = re.sub(r'\w*\d+\w*', '', x)  # Remove numbers
    x = re.sub(r'\s{2,}', ' ', x)  # Replace the over spaces

    return x

def my_tokenizer(text):

    """
    Tokenization function (funzione che mi permette di eliminare stopwords e effettuare lo stemming)

        :param text: testo che deve essere tokenizzato
        :return pruned: lista di stringe

    """

    sw = stopwords.words('english')
    stemmer = snowball.SnowballStemmer(language="english")
    tokens = word_tokenize(text)
    pruned = [stemmer.stem(t.lower()) \
              for t in tokens if re.search(r"^\w", t) and not t.lower() in sw]
    return pruned

def create_tokenized_documents(reviewer_dict):

    texts = []

    for key in sorted(reviewer_dict.keys()):
        # Creates an array of tokenized documents
        texts.append(reviewer_dict[key])

    return texts

def create_model(vectorizer,texts):

    """

        Funzione di cosine similarity fatta tra la query e i documenti

            :param reviewer_dict:  dizionario contenente come valore il titolo/titoli+abstract dei pdf dei revisori
            :param input_dict: dizionario contenente come valore il titolo/titoli+abstract della query
            :return values:  dizionario contente come valore la lista dei valori di cos_similarity tra la query e i pdf dei revisori

    """
    # creates the model
    model = vectorizer.fit_transform(texts)

    return model

def cos_similarity(reviewer_dict, input_dict):
    
    """
        Funzione di cosine similarity fatta tra la query e i documenti

            :param reviewer_dict:  dizionario contenente come valore il titolo/titoli+abstract dei pdf dei revisori
            :param input_dict: dizionario contenente come valore il titolo/titoli+abstract della query
            :return values:  dizionario contente come valore la lista dei valori di cos_similarity tra la query e i pdf dei revisori

    """


    values = {}

    for pdf in sorted(input_dict.keys()):
        # adds a query to the model
        texts = create_tokenized_documents(reviewer_dict)
        vectorizer = CountVectorizer(tokenizer=my_tokenizer)
        model = create_model(vectorizer,texts)
        query = vectorizer.transform([input_dict[pdf]])
        cos = cosine_similarity(query, model)
        values.update({pdf: cos})

    return values

def jaccard_similarity(reviewer_dict, input_dict):
    
    """
    Funzione di jaccard similarity tra la query e i singoli documenti

        :param reviewer_dict: dizionario contenente come valore le keywords dei pdf dei reviori
        :param input_dict: dizionario contenente come valore le keywords dei pdf della query
        :return values_calculated: dizionario contenente come valore il massimo valore dello jaccard per ogni pdf query

    """

    values_keywords = []
    values_calculated = {}

    for file_pdf in sorted(input_dict.keys()):
        for pfd_autore in sorted(reviewer_dict.keys()):
            # List the unique words in a document
            words_doc1 = set(reviewer_dict[pfd_autore].lower().replace(",", "").split())
            words_doc2 = set(input_dict[file_pdf].lower().replace(",", "").split())

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
        massimo_keyword = float(np.max(values_keywords))
        values_calculated.update({file_pdf: massimo_keyword})

    return values_calculated

def user_choice():

    decision = ''
    # Possibilità di far scegliere all'utente tra valore massimo e media
    while decision != "media" and decision != "valore massimo":
            decision = input("L'utente desidera utilizzare la media o il valore massimo per il confronto delle sezioni 'titoli' e 'titoli+abstract'? ").lower()
            if decision != "media" and decision != "valore massimo":
                print("Input non valido inserire media o valore massimo")

    print("L'utente ha scelto l'opzione {}".format(decision))


    return decision

def calculate_jaccard(dict_reviewer):

    massimo_keywords = {}

    for nome_autore in sorted(dict_reviewer.keys()):
        if not "Massimiliano Di Penta" in nome_autore:
            valori_massimi = jaccard_similarity(dict_reviewer[nome_autore], dict_reviewer["Massimiliano Di Penta"])
            massimo_keywords.update({nome_autore: valori_massimi})

    return massimo_keywords

def calculate_table_values_keywords(pdf_di_penta,massimo_keywords,authors):

    autori_keywords = {}
    val_max_keywords_tabella = []

    for pdf in sorted(pdf_di_penta):
        print(pdf)
        for autore in sorted(authors):
            if not "Massimiliano Di Penta" in autore:
                print(autore + " -----> " + str(massimo_keywords[autore][pdf]))
                val_max_keywords_tabella.append(massimo_keywords[autore][pdf])
        autori_keywords.update({pdf: val_max_keywords_tabella})
        val_max_keywords_tabella = []
        print("<---------------------------------------------------->")

    return autori_keywords

def extraction(file_name,file_output):

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

    return title_abstract,titles,keywords

def calculate_table_value_abstract_tit_and_tit(pdf_letti,autori_letti,sezione,decision):

    sezione_tit_or_ab = {}
    val_tit_ab_tabella = []

    for pdf in sorted(pdf_letti):
        print(pdf)
        for autore in sorted(autori_letti):
            if not "Massimiliano Di Penta" in autore:
                if decision == "media":
                    print(autore + " -----> " + str(np.mean(sezione[autore][pdf])))
                    val_tit_ab_tabella.append(float(np.mean(sezione[autore][pdf])))
                elif decision == "valore massimo":
                    print(autore + " -----> " + str(np.max(sezione[autore][pdf])))
                    val_tit_ab_tabella.append(float(np.max(sezione[autore][pdf])))
        sezione_tit_or_ab.update({pdf: val_tit_ab_tabella})
        val_tit_ab_tabella = []
        print("<---------------------------------------------------->")



    return sezione_tit_or_ab

if __name__ == '__main__':


    authors = []
    author_title_abstact = {}
    author_keywords = {}
    author_titles = {}

    path = find_path_for_extraction()

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
                        title_abstract,titles,keyword = extraction(file_name,file_output)
                    except:
                        print("Error in filename " + file_name + str(IOError))
                        continue

            author_title_abstact[author_name] = title_abstract
            author_keywords[author_name] = keywords
            author_titles[author_name] = titles
            authors.append(author_name)

    print("EXTRACTION ENDED SUCCESSFULLY")


    decision = user_choice()

    pdf_di_penta = []
    for pdf in sorted(author_titles["Massimiliano Di Penta"].keys()):
        print(pdf)
        pdf_di_penta.append(pdf)

    print("********************************")
    print()


    # 1) utilizzo della funzione jaccard per le KEYWORDS

    massimo_keywords = calculate_jaccard(author_keywords)
    autori_keywords = calculate_table_values_keywords(pdf_di_penta,massimo_keywords,authors)


    print("********************************")
    print()

    # 2) utilizzo della funzione cosine similarity sul TITOLO e ABSTRACT

    print("ABSTRACT+TITOLI")

    tit_ab = {}

    for nome_autore in sorted(author_title_abstact.keys()):
        if not "Massimiliano Di Penta" in nome_autore:
            valori_ab_tit = cos_similarity(author_title_abstact[nome_autore],
                                           author_title_abstact["Massimiliano Di Penta"])
            tit_ab.update({nome_autore: valori_ab_tit})

    autori_tit_ab = {}

    autori_tit_ab = calculate_table_value_abstract_tit_and_tit(pdf_di_penta,authors,tit_ab,decision)

    print("********************************")
    print()

    # 3) utilizzo della funzione cosine similarity sul TITOLO

    print("TITOLI")

    tit = {}

    for nome_autore in sorted(author_titles.keys()):
        if not "Massimiliano Di Penta" in nome_autore:
            valori_tit = cos_similarity(author_titles[nome_autore], author_titles["Massimiliano Di Penta"])
            print(type(valori_tit["1934a880.pdf"]))
            tit.update({nome_autore: valori_tit})

    autori_titoli = {}

    autori_titoli = calculate_table_value_abstract_tit_and_tit(pdf_di_penta,authors,tit,decision)

    print("<---------------------------------------------------->")


    authors.remove("Massimiliano Di Penta")

    for pdf in pdf_di_penta:
        info = {'Possibili Revisori': authors, 'Cosine Similarity: Titoli': autori_titoli[pdf],
                'Cosine Similarity: Titoli+Abstract': autori_tit_ab[pdf],
                'Jaccard Similarity: Keywords': autori_keywords[pdf]}

        with open(path + "Massimiliano Di Penta\\" + pdf, 'rb') as f:
            pdf_reader = PdfFileReader(f)
            titolo = pdf_reader.getDocumentInfo().title
            print(titolo)
            print(tabulate(info, headers='keys', tablefmt='fancy_grid'))
            print()
            print()