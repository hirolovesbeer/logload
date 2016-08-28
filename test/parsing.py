import unittest

from logload import logload

class TestTokenizer(unittest.TestCase):
    def test_name(self):
        logload.tokenize("foobar")

    def test_string(self):
        logload.tokenize("\"foobar\"")

    def test_group(self):
        logload.tokenize("[ \"foo\", \"bar\" ]")

    def test_list(self):
        logload.tokenize("( \"foo\", glorg )")

    def test_empty(self):
        logload.tokenize("")

class TestParser(unittest.TestCase):
    @unittest.expectedFailure
    def test_empty(self):
        logload.parse(logload.tokenize(""))

    def test_empty_list(self):
        logload.parse(logload.tokenize("( )"))
        
    def test_list_string(self):
        logload.parse(logload.tokenize("( \"foobar\" )"))

    def test_empty_group(self):
        logload.parse(logload.tokenize("[ \"foobar\", rand ]"))
        
if __name__ == "__main__":
    unittest.main()
