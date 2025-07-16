from abc import ABC, abstractmethod

class LanguageModel:

    class LanguageElement:



    class Semantic:

        def __init__(self, label: str, *tokens):
            self.label = label
            self.tokens = tokens

        def __iter__(self):
            return iter(self.tokens)

        def scan(self, tokens):
            for i, x in enumerate(tokens):
                if x in self:
                    yield (i,)

        def run_scan(self, tokens):
            return [i for i in self.scan(tokens)]
    
    class Clause:

        def __init__(self, l, *psps):
            self.label = label
            self.pairs = psps
            self.prefixes = [x[0] for x in psps]
            self.suffixes = [x[1] for x in psps]

        def scan(self, tokens):
            