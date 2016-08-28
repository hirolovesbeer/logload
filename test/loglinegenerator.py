import unittest

from logload import logload

class TestLogLineGenerator(unittest.TestCase):
    def test_randword(self):
        gen = logload.LogLineGenerator()
        gen.set_pattern('(["foo", "bar", "baz"], "=", randword)')
        print(gen.lines(10))

    def test_timestamp(self):
        gen = logload.LogLineGenerator()
        gen.set_pattern('("<13>", timestamp, " mymachine ", ["postmaster[14333]", "httpd[17663]"], ": Oww, i must terminate!")')
        print(gen.lines(5))

if __name__ == "__main__":
    unittest.main()
