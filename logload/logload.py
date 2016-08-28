
import random

from funcparserlib.lexer import make_tokenizer, Token, LexerError

def tokenize(str):
    """ str -> Sequence(Token) """
    specs = [
        (u'Space', (ur'[ \t\r\n]+', )),
        (u'String', (ur'"(%(unescaped)s | %(escaped)s)*"' % regexps, VERBOSE)),
        (u'Op', (ur'[\[\],]', )),
        (u'Name', (ur'[A-Za-z_][A-Za-z_0-9]*',)),
    ]
    empty = [u'Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in empty]

class Fragment:
    def expand(self):
        return ""

class RandomSelection(Fragment):
    def __init__(self, lis):
        self.lis = random.shuffle(lis)
        self.length = len(lis)
        self.ptr = 0

    def expand(self):
        self.ptr = self.ptr + 1
        if self.ptr >= self.length:
            self.ptr = 0
        return self.lis[ptr]

class StaticSelection(Fragment):
    def __init__(self, s):
        self.s = s

    def expand(self):
        return s
    
class LogLineGenerator:

    def set_pattern(pat):
        pass

    def lines(i):
        pass

def main():
    pass

if __name__ == "__main__":
    main()
    
