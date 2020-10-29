"""define input of CFG"""
splitter = ['.', ';', '  ', ',', '|']


def new_word():
    """get word from user"""
    word = input("Please enter the word. \n")
    char_list = []
    for i in word:
        char_list.append(i)
    return char_list


class CFG:
    """Definition of context-free Grammar"""

    def __init__(self):
        self.variables = []
        self.alphabet = []
        self.rules = dict(set())
        self.start = None

    def set_variables(self, variables):
        """set variables"""
        self.variables = variables

    def set_alphabet(self, alphabet):
        """set alphabet"""
        self.alphabet = alphabet

    def set_rules(self, key, value):
        """set rules"""
        if key not in self.rules:
            self.rules.update({key: set()})
        self.rules[key].add(value)

    def set_start(self, start):
        """set starting symbol"""
        self.start = start

    def new_grammar(self):
        """get grammar from user input"""
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
            check_syntax(self.variables, self.alphabet, var)
            for k in var:
                self.set_rules(i, k)

        self.set_start(input("Please enter the starting Symbol.\n"))
        check_start(self.variables, self.start)

    def file_input(self):
        
        file = open(input("Enter filename you want to import.\n"), "r").read().splitlines()
        #Remove Empty Lines from the list
        for i in file:
            if i == '':
                file.remove(i)
        #Extract the Terminal Symbols and the Alphabet from the file
        for i in splitter:
            file[0] = file[0].replace(i, ' ')
            file[1] = file[1].replace(i, ' ')
        self.set_variables(file[0].split())
        self.set_alphabet(file[1].split())

        self.set_start(file[2])
        check_start(self.variables, self.start)
        #delete the first three Elements from the List (Variables, Alphabet and Starting Symbol)
        del file[0:3]

        for rules in file:
            nterminal = rules[0]
            for i in splitter:
                rules = rules.replace(i, ' ')
            rules = rules.split()
            del rules[0]
            rules.remove('->')
            check_syntax(self.variables, self.alphabet, rules)
            for k in rules:
                self.set_rules(nterminal, k)



def check_syntax(variables, alphabet, rules):
    """check input syntax"""
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
        if low not in alphabet:
            print("Inappropriate terminal symbols have been entered.\n")
            raise SystemExit

    for upp in upper:
        if upp not in variables:
            print("Inappropriate symbols have been entered. \n")
            raise SystemExit


def check_start(variables, start):
    """check if starting symbol is in grammar"""
    if start not in variables:
        print("The starting Symbol has to be part of the symbols. \n")
        raise SystemExit
