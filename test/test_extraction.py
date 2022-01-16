# content of test_class.py
from extraction import text_preproc,jaccard_similarity,my_tokenizer

class TestClass(unittest.TestCase):

    def test_text_preproc(self):
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

    def test_jaccard_similarity(self):

        dict1 = {"Pdf1": "Software, open source, bug"}
        dict2 = {"Pdf2": "Hardware, bug, private"}
        dict3 = {"Pdf2": 0.16666666666666666}

        assert jaccard_similarity(dict1, dict2) == dict3

    def test_my_tokenizer(self):

        words1 = 'John goes to school with his friends'
        words2 = ['john', 'goe', 'school', 'friend']

        assert my_tokenizer(words1) == words2

