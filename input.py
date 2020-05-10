import array
import re

splitter = ['.', ';', '  ', ',']

class cfg:
    def __init__(self):
        self.variables = []
        self.aplhabet = []
        self.rules = []
        self.start

    def set_variables(self, variables):
        self.variables = variables
    def set_alphabet(self, alphabet):
        self.alphabet = alphabet
    def set_rules(self, rules):
        self.rules = rules
    def set_start(self, start):
        self.start = start

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
        #Checkt ob alle benutzen Buchstaben in den Regeln auch im Alphabet gegeben sind
        for i in range(0, len(lower)):
            wrong = 0
            for j in range(0, len(alphabet)):
                if lower[i] != alphabet[j]:
                    wrong+=1
            if wrong == len(alphabet):
                print(2)
                return -1
        #Checkt ob alle benutzen Variabeln in den Regeln auch gegeben sind
        for i in range(0, len(upper)):
            wrong = 0
            for j in range(0, len(variables)):
                if upper[i] != variables[j]:
                    wrong += 1
            if wrong == len(variables):
                print(3)
                return -1
        return 1

    def new_grammar(self):
        #Variabeln input
        var = input("Bitte geben sie alle Variabeln ein.\n")
        for i in range(0, len(splitter)):
            var = var.replace(splitter[i], ' ')
        cfg.set_variables(cfg, var.split())
        #Aplhabet input
        var = input("Bitte geben sie das Alphabet an.\n")
        for i in range(0, len(splitter)):
            var = var.replace(splitter[i], ' ')
        cfg.set_alphabet(self, var.split())
        #Regeln input
        var = input("Bitte geben sie die Regeln der Gramatik an.\n")
        var = var.replace(' ', '')
        #cfg.set_rules(self, re.split(';|,|.', var))
        cfg.set_rules(self, re.split(';|,', var))
        #Start input
        cfg.set_start(self, input("Bitte geben sie die start Variable an.\n"))
        if cfg.check_syntax(self, self.variables, self.alphabet, self.rules, self.start) != 1:
            print("Es gibt Syntaktische Fehler in der Grammatik, bitte beheben sie diese und Proboieren sie es noch einmal.\n")
            raise SystemExit

grammar = cfg
cfg.new_grammar(grammar)
print(grammar.rules)
