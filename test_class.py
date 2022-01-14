# content of test_class.py
import unittest
from extraction import text_preproc, jaccard_similarity, my_tokenizer, cos_similarity
import re

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
        x13 = "CIAO"

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
        assert text_preproc(x13) == "ciao"

    def test_jaccard_similarity(self):

        dict1 = {"Pdf1": "Software, open source, bug"}
        dict2 = {"Pdf2": "Hardware, bug, private"}
        dict3 = {"Pdf2": 0.16666666666666666}

        assert jaccard_similarity(dict1, dict2) == dict3

    def test_my_tokenizer(self):

        words1 = 'John goes to school with his friends'
        words2 = ['john', 'goe', 'school', 'friend']

        assert my_tokenizer(words1) == words2

    '''
    def test_cos_similarity(self):
        dict3 = {}
        abstract1 =  "  In recent software development and distribution scenarios, \
                            app stores are playing a major role, especially for mobile apps. \
                            On one hand, app stores allow continuous releases of app updates. \
                            On the other hand, they have become the premier \
                            point of interaction between app providers and users."

        abstract = re.findall('recent(.*?)providers', abstract1)

        dict1 = {"Pdf1": abstract[0]}


        abstract2 = "  Online shopping is one of the most important \
                            applications on the Internet and it is one that has been steadily \
                            growing over the last decade. With increasing numbers of online \
                            shopping transactions there are also raising concerns over privacy \
                            and protection of the customer data collected by the webshops. \
                            This is why, we need privacy-preserving technologies for online \
                            shopping, in the interest of both users and businesses."


        abstact3 = re.findall('shopping(.*?)users', abstract2)


        dict2 = {"Pdf3": abstact3[0]}

        dict3.update({"Pdf3": 0.18257419})

        assert cos_similarity(dict1, dict2) == dict3
    '''

if __name__ == '__main__':
    unittest.main()