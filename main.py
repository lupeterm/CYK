from typing import List, Any


class Cfg:

    def __init__(self, variables, alphabet, rules, start):
        self.variables = variables
        self.alphabet = alphabet
        self.rules = rules
        self.start = start

    def set_grammar_from_input(self):
        grammar = list((input("Insert grammar here: ")))
        # G = ({S, A, B, C},{a, b, c}, R, S)
        boundaries = []
        for char in range(0, len(grammar)):
            if grammar[char] == "}":
                boundaries.append(char)
        v = []
        a = []
        r = []
        for i in range(0, len(grammar)):

            if i < boundaries[0] and str.isupper(grammar[i]):
                v.append(grammar[i])
            if boundaries[0] < i < boundaries[1] and str.islower(grammar[i]):
                a.append(grammar[i])
            if i >= len(grammar) - 2 and str.isupper(grammar[i]):
                self.start = grammar[i]
        self.alphabet = a
        self.variables = v



    def to_string(self):
        stri = "G = (V,Σ,R," + self.start + ")\nV = {"
        for i in self.variables:
            stri += i + ","
        stri += "}\nΣ = {"
        for i in self.alphabet:
            stri += i + ","
        stri += "}\nR = {"
        #for lhs in self.rules:
        #    stri += "\n" + lhs[0] + " → "
        #    for i in range(1, len(lhs)):
        #        stri += lhs[i]
        #        stri += " | "
        stri += "}\n"
        print(stri)

    def set_alpha(self):
        n = int(input("how many terminals? "))
        self.alphabet = []
        for i in range(0, n):
            self.alphabet.append(str(input("")))

    def set_var(self):
        self.variables = []
        n = int(input("how many nonterminals? "))
        for i in range(0, n):
            self.variables.append(str(input("")))

    def set_rules(self):
        self.rules = []
        for i in range(len(self.variables)):
            rule = [self.variables[i]]
            while True:
                s = input(self.variables[i] + "→ ")
                if s == "0":
                    break
                rule.append(s)
            self.rules.append(rule)
        print(self.rules)


test = Cfg

# Cfg.set_var(test)
# Cfg.set_alpha(test)
# Cfg.set_rules(test)
# test.start = str(input("What is the starting Symbol? "))
Cfg.set_grammar_from_input(test)
test.to_string(test)
print(test)
