
### generator
import random

class Fragment:
    def expand(self):
        return ""

class RandomSelection(Fragment):
    def __init__(self, lis):
        self.lis = lis
        random.shuffle(self.lis)
        self.length = len(lis)
        self.ptr = 0

    def expand(self):
        self.ptr = self.ptr + 1
        if self.ptr >= self.length:
            self.ptr = 0
        return self.lis[self.ptr]

class RandomWord(Fragment):
    def __init__(self, name):
        self.name = name
        with open('logload/words.txt') as x: self.words = x.readlines()

    def expand(self):
        return random.choice(self.words)
    
class StaticSelection(Fragment):
    def __init__(self, s):
        self.s = s

    def expand(self):
        return s

from datetime import datetime

class Timestamp(Fragment):
    def expand(self):
        dt = datetime.now()
        return dt.isoformat()
    
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
        ('Op', (r'[\[\],()]', )),
        ('Name', (r'[A-Za-z_][A-Za-z_0-9]*',)),
    ]
    empty = ['Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in empty]

### parser

class NameError(Exception):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Name not available: " + self.name

import re

re_esc = re.compile(regexps[u'escaped'], VERBOSE)

from funcparserlib.parser import (some, a, maybe, many, finished, skip,
                                  forward_decl, NoParseError)

def parse(seq):
    tokval = lambda x: x.value
    toktype = lambda t: some(lambda x: x.type == t) >> tokval
    op = lambda s: a(Token('Op', s)) >> tokval
    op_ = lambda s: skip(op(s))

    def make_group(n):
        if n is None:
            return RandomSelection([])
        else:
            return RandomSelection([n[0]] + n[1])

    def make_list(n):
        if n is None:
            return []
        else:
            return [n[0]] + n[1]
        
    def unescape(s):
        std = {
            u'"': u'"', u'\\': u'\\', u'/': u'/', u'b': u'\b', u'f': u'\f',
            u'n': u'\n', u'r': u'\r', u't': u'\t',
        }

        def sub(m):
            if m.group('standard') is not None:
                return std[m.group('standard')]
            else:
                return unichr(int(m.group('unicode'), 16))

        return re_esc.sub(sub, s)

    def make_name(n):
        if n == "randword":
            return RandomWord(n)
        elif n == "timestamp":
            return Timestamp()
        else:
            raise NameError(n)
    
    def make_string(n):
        return unescape(n[1:-1])

    name = toktype('Name') >> make_name
    string = toktype('String') >> make_string
    atom = string | name
    
    group = (
        op_('[') +
        maybe(atom + many(op_(',') + atom)) +
        op_(']')
        >> make_group)

    value = atom | group
    
    lis = (
        op_('(') +
        maybe(value + many(op_(',') + value)) +
        op_(')')
        >> make_list)

    logload = lis | value
    logload_text = logload + skip(finished)

    return logload_text.parse(seq)

### main & options

class LogLineGenerator:

    def set_pattern(self, pat):
        self.spec = parse(tokenize(pat))

    def execute(self, spec):
        if type(spec) is list:
            return ''.join([ self.execute(sp) for sp in spec])
        if type(spec) is str:
            return spec
        if isinstance(spec, Fragment):
            return spec.expand()
        
        
    def lines(self, i):
        return [self.execute(self.spec) for x in range(i)]
    
def main():
    pass

if __name__ == "__main__":
    main()
    
