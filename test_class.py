# content of test_class.py
from extraction import text_preproc


class TestClass:

    def test_one(self):
        x = "xbd"
        assert text_preproc(x) == " "