from abc import ABC, abstractmethod

class LanguageModel:

    class LanguageElement(ABC):

        @abstractmethod
        def scan(self, tokens: list[str]) -> list[tuple[int]]:
            raise NotImplementedError
        
        def run_scan(self, tokens: list[str]) -> list[tuple[int]]:
            return [x for x in self.scan(tokens)]

    class Contractions(LanguageElement):

        def __init__(self, **kwargs):
            self.contractions = kwargs

        def __getitem__(self, s):
            return self.contractions(s)
        
        def scan(self, tokens):
            for i, x in enumerate(tokens):
                if x in self.contractions.keys():
                    yield i

        def map(self, tokens):
            result = []
            for x in tokens:
                if x in self.contractions.keys():
                    result.append(self[x])
                else:
                    result.append(None)
            return result

    class Semantic(LanguageElement):

        def __init__(self, label: str, *tokens):
            self.label = label
            self.tokens = tokens

        def __iter__(self):
            return iter(self.tokens)

        def scan(self, tokens):
            for i, x in enumerate(tokens):
                if x in self:
                    yield i
    
    class Clause(LanguageElement):

        def __init__(self, l, *psps):
            self.label = l
            self.pairs = psps
            self.prefixes = [x[0] for x in psps]
            self.suffixes = [x[1] for x in psps]

        def scan(self, tokens):
            a = None
            b = None
            for i, x in enumerate(tokens):
                if x in self.prefixes:
                    a = i
                    break
            for j, y in enumerate(tokens):
                if y in self.suffixes:
                    b = j
                    break
            if i is not None and j is not None:
                yield (i, j)

    def __init__(self, sw_semantic: Semantic, contra: Contractions, *elements: list[LanguageElement]) -> None:
        self.elements = elements
        self.stopwords = sw_semantic
        self.contractions = contra

    def tokenize_sentence(self, sentence):
        ssplit = sentence.split(" ")
        destopped = []
        contraction_map = self.contractions.map(ssplit)
        for i, x in enumerate(ssplit):
            if contraction_map[i] is not None:
                for tok in contraction_map[i]:
                    destopped.append(tok)
                else:
                    destopped.append(x)
        for i in self.stopwords.scan(destopped):
            destopped[i] = None
        destopped = [x for x in destopped if x is not None]
        result = []
        for x in destopped:
            if x[-1] in ",.?;()!":
                result.append(x[:-1])
                result.append(x[-1])
            else:
                result.append(x)
        return result