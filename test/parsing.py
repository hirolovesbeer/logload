import unittest

from logload import logload

class TestTokenizer(unittest.TestCase):
    def test_name(self):
        logload.tokenize("foobar")

    def test_string(self):
        logload.tokenize("\"foobar\"")

    def test_group(self):
        logload.tokenize("[ \"foo\", \"bar\" ]")


if __name__ == "__main__":
    unittest.main()
