
class Fragment:
    def expand(self):
        return ""

class RandomSelection(Fragment):
    def __init__(self, lis):
        self.lis = random.shiffule(lis)
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
    
