# Defines all possible meta-symbols by which
# to separate rules
splitter = ['.', ';', '  ', ',', '|']


class CFG:

    def __init__(self):
        self.variables = []
        self.alphabet = []
        self.rules = dict(set())
        self.start = ""

    def set_variables(self, variables: list[str]):
        self.variables = variables

    def set_alphabet(self, alphabet: list[str]):
        self.alphabet = alphabet

    def set_rules(self, key, value):
        if key not in self.rules:
            self.rules.update({key: set()})
        self.rules[key].add(value)

    def set_start(self, start: str):
        self.start = start

    def new_grammar(self):
        non_terminals = input("Please enter all non-terminal symbols.\n")
        terminals = input("Please enter all terminal symbols.\n")

        for i in splitter:
            non_terminals = non_terminals.replace(i, ' ')
            terminals = terminals.replace(i, ' ')

        self.set_variables(non_terminals.split())
        self.set_alphabet(terminals.split())

        for i in self.variables:
            rule = input(
                "Please enter all rules for " + i +
                ".\nPlease enter \\E for epsilon (if needed).\n")

            for k in splitter:
                rule = rule.replace(k, ' ')
            rule = rule.split()

            check_syntax(self.variables, self.alphabet, rule)
            for k in rule:
                self.set_rules(i, k)

        start = input("Please enter the starting symbol.\n")
        if not start in self.variables:
            print(f"The starting symbol {start} has to be part of the non-terminals!\n")
            raise SystemExit
        else:
            self.set_start(start)


    def file_input(self):
        file = open(input("Enter filename you want to import.\n"), "r").read().splitlines()
        file = [line for line in file if line] # remove empty lines

        # set non-terminals and terminals by looking at the first two
        # lines of the file and replacing separators
        for i in splitter:
            file[0] = file[0].replace(i, ' ')
            file[1] = file[1].replace(i, ' ')

        self.set_variables(file[0].split())
        self.set_alphabet(file[1].split())

        if not file[2] in self.variables:
            print(f"The starting symbol {file[2]} has to be part of the non-terminals!\n")
            raise SystemExit
        else:
            self.set_start(file[2])

        # set rules from line 4 onwards
        for rules in file[3:]:
            # left part of rule
            non_terminal = rules[0]

            for i in splitter:
                rules = rules.replace(i, ' ')

            rules = rules.split()
            rules.remove(non_terminal)
            rules.remove("->")
            check_syntax(self.variables, self.alphabet, rules)

            for r in rules:
                self.set_rules(non_terminal, r)


def check_syntax(variables: list[str], alphabet: list[str], rules: list[str]):
    """
    Checks if terminals and non-terminals that were entered at the rule stage
    are actually present in the list of terminals and non-terminals.

    Terminates if this is not the case.
    """
    for r in rules:
        if r != r'\E':
            for i in r:
                if i.islower() and i not in alphabet:
                    print("Inappropriate terminal symbols have been entered.\n")
                    raise SystemExit
                if i.isupper() and i not in variables:
                    print("Inappropriate symbols have been entered. \n")
                    raise SystemExit
