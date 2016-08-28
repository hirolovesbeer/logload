
import random

### tokenizer

from re import VERBOSE

from funcparserlib.lexer import make_tokenizer, Token, LexerError

regexps = {
    'escaped': r'''
        \\                                  # Escape
          ((?P<standard>["\\/bfnrt])        # Standard escapes
        | (u(?P<unicode>[0-9A-Fa-f]{4})))   # uXXXX
        ''',
    'unescaped': r'''
        [^"\\]                              # Unescaped: avoid ["\\]
        ''',
}

def tokenize(str):
    """ str -> Sequence(Token) """
    specs = [
        ('Space', (r'[ \t\r\n]+', )),
        ('String', (r'"(%(unescaped)s | %(escaped)s)*"' % regexps, VERBOSE)),
        ('Op', (r'[\[\],]', )),
        ('Name', (r'[A-Za-z_][A-Za-z_0-9]*',)),
    ]
    empty = ['Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in empty]

### parser


### generator

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

### main & options
    
def main():
    pass

if __name__ == "__main__":
    main()
    
