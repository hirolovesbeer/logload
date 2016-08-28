
### generator
import random

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
            return ['grp']
        else:
            return ['grp', n[0]] + n[1]

    def make_list(n):
        if n is None:
            return ['lis']
        else:
            return ['lis', n[0]] + n[1]
        
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
        return n
    
    def make_string(n):
        return unescape(n[1:-1])

    name = toktype('Name') >> make_name
    string = toktype('String') >> make_string
    value = forward_decl()

    group = (
        op_('[') +
        maybe(value + many(op_(',') + value)) +
        op_(']')
        >> make_group)

    lis = (
        op_('(') +
        maybe(value + many(op_(',') + value)) +
        op_(')')
        >> make_list)

    value.define(string | name)
    
    logload = lis | group
    logload_text = logload + skip(finished)

    return logload_text.parse(seq)

### main & options
    
class LogLineGenerator:

    def set_pattern(pat):
        self.spec = parse(tokenize(pat))

    def lines(i):
        pass
    
def main():
    pass

if __name__ == "__main__":
    main()
    
