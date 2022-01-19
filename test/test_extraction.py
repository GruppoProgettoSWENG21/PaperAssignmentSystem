# content of test_extraction.py
from sklearn.feature_extraction.text import CountVectorizer
from extraction import find_path_for_extraction,text_preproc,cos_similarity,jaccard_similarity,my_tokenizer,create_tokenized_documents,create_model,user_choice,calculate_jaccard,calculate_table_values
import unittest
import numpy as np
from numpy import array
from mock_test import set_keyboard_input,get_display_output

class TestClass(unittest.TestCase):

    def test_text_preproc(self):  #pragma no cover

        #wb
        x1 = "xbd"
        x2 = "xef"
        x3 = "xbf"
        x4 = "."
        x5 = ":"
        x6 = "\\n"
        x7 = "\\xc2\\xb7"
        x8 = "\t"
        x9 = "\\"
        x10 = "\\xe2"
        x11 = "\\x94"
        x12 = "\\x80"
        x13 = "CIAO   1"
        x14 = "https://www.google.it/"
        x15 = "#software@"
        x16 = "'f for"

        assert text_preproc(x1) == " "
        assert text_preproc(x2) == " "
        assert text_preproc(x3) == " "
        assert text_preproc(x4) == " "
        assert text_preproc(x5) == " "
        assert text_preproc(x6) == " "
        assert text_preproc(x7) == " "
        assert text_preproc(x8) == " "
        assert text_preproc(x9) == " "
        assert text_preproc(x10) == " "
        assert text_preproc(x11) == " "
        assert text_preproc(x12) == " "
        assert text_preproc(x13) == "ciao "
        assert text_preproc(x14) == " //www google it/"
        assert text_preproc(x15) == " "
        assert text_preproc(x16) == " for"

    def test_jaccard_similarity(self):  #bb

        # il test lo vado a fare su una parte del requisito da implementare

        dict1 = {"Pdf1": "Software, open source, bug"}
        dict2 = {"Pdf2": "Hardware, bug, private"}
        dict3 = {"Pdf2": 0.16666666666666666}

        assert jaccard_similarity(dict1, dict2) == dict3

    def test_my_tokenizer(self): #pragma no cover
        # wb
        words1 = 'John goes to school with his friends'
        words2 = ['john', 'goe', 'school', 'friend']

        assert my_tokenizer(words1) == words2

    def test_create_tokenized_documents(self):  #pragma no cover

        #wb

        dict1 = {"Pdf1": "Abstract del primo pdf", "Pdf2":"Abstract del secondo pdf"}
        texts = ["Abstract del primo pdf","Abstract del secondo pdf"]

        assert create_tokenized_documents(dict1) == texts

    def test_user_choice(self):

        # bb
        set_keyboard_input(['media'])
        user_choice()
        output1 = get_display_output()
        set_keyboard_input(['valore massimo'])
        user_choice()
        output2 = get_display_output()

        assert output1 == ["L'utente desidera utilizzare la media o il valore massimo per il confronto delle sezioni 'titoli' e 'titoli+abstract'? ", "L'utente ha scelto l'opzione media"]
        assert output2 == ["L'utente desidera utilizzare la media o il valore massimo per il confronto delle sezioni 'titoli' e 'titoli+abstract'? ", "L'utente ha scelto l'opzione valore massimo"]

    def test_calculate_jaccard(self):  #bb

        dict1 = {"Pdf1": "Software, open source, bug"}
        dict2 = {"Pdf2": "Hardware, bug, private"}
        dict3 = {"Massimiliano Di Penta": dict1,"Alfredo Di Geronimo":dict2}
        dict4 = {"Pdf1": 0.16666666666666666}
        dict5 = {"Alfredo Di Geronimo": dict4}

        assert calculate_jaccard(dict3) == dict5

    def test_calculate_table_values(self): #bb

        dict1 = {"Pdf1": 0.16666666666666666}
        dict2 = {"Alfredo Di Geronimo": dict1}
        pdf_list = ["Pdf1"]
        authors = ["Alfredo Di Geronimo","Massimiliano Di Penta"]
        lista = [0.16666666666666666]
        dict3 = {"Pdf1": lista}

        assert calculate_table_values(pdf_list, dict2, authors) == dict3

if __name__ == '__main__':
    TestClass.main()