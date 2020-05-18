import re
from collections import defaultdict

splitter = ['.', ';', '  ', ',']

def new_word():
        word = input("what is the word?\n")
        c = []
        for i in word:
            c.append(i)
        return c

class cfg:

    def __init__(self):
        self.variables = []
        self.alphabet = []
        self.rules = defaultdict(list)
        self.start = None

    def set_variables(self, variables):
        self.variables = variables

    def set_alphabet(self,alphabet):
        self.alphabet = alphabet

    def set_rules(self, key, value):
        self.rules[key].append(value)

    def set_start(self, start):
        self.start = start

    def new_grammar(self):
        # Variabeln input
        var = input("Bitte geben Sie alle Variablen ein.\n")
        for i in splitter:
            var = var.replace(i, ' ')
        self.set_variables(var.split())
        print(self.variables)
        # Aplhabet input
        var = input("Bitte geben Sie das Alphabet an.\n")
        for i in splitter:
            var = var.replace(i, ' ')
        self.set_alphabet(var.split())
        print(self.alphabet)
        # Regeln input
        for i in self.variables:
            var = input("Bitte geben Sie alle Regeln für " + i + " an:\n")
            for k in splitter:
                var = var.replace(k, ' ')
            var = var.split()
            for k in var:
                self.set_rules(i, k)
            print(self.rules)
        # Start input
        cfg.set_start(self, input("Bitte geben sie die start Variable an.\n"))
        #if cfg.check_syntax(self, self.variables, self.alphabet, self.rules, self.start) != 1:
         #   print(
          #      "Es gibt Syntaktische Fehler in der Grammatik, bitte beheben sie diese und Probieren sie es noch einmal.\n")
           # raise SystemExit

    def check_syntax(self, variables, alphabet, rules, start):
        lower = []
        upper = []
        wrong = 0
        for i in range(0, len(rules)):
            if rules[i].find(start, 0, 1) == -1:
                wrong += 1
            var = rules[i]
            for j in range(0, len(var)):
                if var[j].islower():
                    lower.append(var[j])
                if var[j].isupper():
                    upper.append(var[j])
        if wrong == len(rules):
            print(1)
            return -1
        # Checkt ob alle benutzen Buchstaben in den Regeln auch im Alphabet gegeben sind
        for i in range(0, len(lower)):
            wrong = 0
            for j in range(0, len(alphabet)):
                if lower[i] != alphabet[j]:
                    wrong += 1
            if wrong == len(alphabet):
                print(2)
                return -1
        # Checkt ob alle benutzen Variablen in den Regeln auch gegeben sind
        for i in range(0, len(upper)):
            wrong = 0
            for j in range(0, len(variables)):
                if upper[i] != variables[j]:
                    wrong += 1
            if wrong == len(variables):
                print(3)
                return -1
        return 1

test = cfg()
cfg.new_grammar(test)
