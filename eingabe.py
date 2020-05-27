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

        # Aplhabet input
        var = input("Bitte geben Sie das Alphabet an.\n")
        for i in splitter:
            var = var.replace(i, ' ')
        self.set_alphabet(var.split())

        # Regeln input
        for i in self.variables:
            print("Bitte geben Sie alle Regeln für " + i + " an:")
            var = input("\"\E\" Wird als Epsilon behandelt.\n")
            for k in splitter:
                var = var.replace(k, ' ')
            var = var.split()
            self.check_syntax(self.variables, self.alphabet, var)
            for k in var:
                self.set_rules(i, k)

        # Start input
        self.set_start(input("Bitte geben sie die start Variable an.\n"))
        self.check_start(self.variables, self.start)

    def check_syntax(self, variables, alphabet, rules):
        lower = []
        upper = []
        for i in rules:
            if i != "\E":
                for j in i:
                    if j.islower():
                        lower.append(j)
                    if j.isupper():
                        upper.append(j)
        print(lower)
        print(upper)
        # Checkt ob alle benutzen Buchstaben in den Regeln auch im Alphabet gegeben sind

        for low in lower:
            if not(low in alphabet):
                print("Es wurden undefinierte Buchstaben angegeben.\n")
                raise SystemExit

        # Checkt ob alle benutzen Variablen in den Regeln auch gegeben sind
        for up in upper:
            if not(up in variables):
                print("Es wurden undefinierte Variabeln angegeben.\n")
                raise SystemExit

    def check_start(self, variables, start):
            if not(start in variables):
                print("Es wurde ein undefiniertes Startsymbol angegeben. \n")
                raise SystemExit