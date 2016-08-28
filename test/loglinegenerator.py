import unittest

from logload import logload

class TestLogLineGenerator(unittest.TestCase):
    def test_simple(self):
        gen = logload.LogLineGenerator()
        gen.set_pattern('(["foo", "bar", "baz"], "=", rand)')
        print(gen.lines(10))
        

if __name__ == "__main__":
    unittest.main()
