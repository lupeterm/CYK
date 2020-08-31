splitter = ['.', ';', '  ', ',']


def new_word():
    word = input("Please enter the word. \n")
    c = []
    for i in word:
        c.append(i)
    return c


class cfg:

    def __init__(self):
        self.variables = []
        self.alphabet = []
        self.rules = dict(set())
        self.start = None

    def set_variables(self, variables):
        self.variables = variables

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def set_rules(self, key, value):
        if key not in self.rules:
            self.rules.update({key: set()})
        self.rules[key].add(value)

    def set_start(self, start):
        self.start = start

    def new_grammar(self):
        var = input("Please enter all symbols.\n")
        for i in splitter:
            var = var.replace(i, ' ')
        self.set_variables(var.split())

        var = input("Please enter all terminal symbols.\n")
        for i in splitter:
            var = var.replace(i, ' ')
        self.set_alphabet(var.split())

        for i in self.variables:
            var = input(
                "Please enter all rules for " + i +
                ".\nPlease enter \\E for epsilon (if needed).\n")
            for k in splitter:
                var = var.replace(k, ' ')
            var = var.split()
            self.check_syntax(self.variables, self.alphabet, var)
            for k in var:
                self.set_rules(i, k)

        self.set_start(input("Please enter the starting Symbol.\n"))
        self.check_start(self.variables, self.start)

    def check_syntax(self, variables, alphabet, rules):
        lower = []
        upper = []
        for i in rules:
            if i != r'\E':
                for j in i:
                    if j.islower():
                        lower.append(j)
                    if j.isupper():
                        upper.append(j)

        for low in lower:
            if not (low in alphabet):
                print("Inappropriate terminal symbols have been entered.\n")
                raise SystemExit

        for up in upper:
            if not (up in variables):
                print("Inappropriate symbols have been entered. \n")
                raise SystemExit

    def check_start(self, variables, start):
        if not (start in variables):
            print("The starting Symbol has to be part of the symbols. \n")
            raise SystemExit
