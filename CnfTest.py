import cnf
import eingabe
import unittest
from sortedcontainers import SortedDict

ERRMSG_ELIM = "something went wrong: unexpected occurrence of '\E'."
ERRMSG_NONISO = "something went wrong: unexpected occurrence of terminal symbol."
ERRMSG_LONGRIGHT = "something went wrong: expected length was <3."

TEST_A = {
    'S': {'AA', 'AB'},
    'A': {'a', r'\E'},
    'B': {'BB', 'b'}
}
TEST_B = {
    'S': {'TU'},
    'T': {'aTb', r'\E'},
    'U': {'Ucc', r'\E'}

}
TEST_C = {
    'S': {'ASA', 'BSB', r'\E'},
    'A': {'a'},
    'B': {'b'}
}
TEST_D = {
    'S': {'LR', r'\E'},
    'L': {'ALLA', 'BLLB', r'\E'},
    'R': {'ARA', 'BRB', r'\E'},
    'A': {'a'},
    'B': {'b'}
}
TEST_E = {
    'S': {'aaA'},
    'A': {'BAB', 'B', r'\E'},
    'B': {'bb'}
}


class TestEpsilonElim(unittest.TestCase):
    def test_elim_A(self):
        grammar = eingabe.cfg()

        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_A)
        grammar.start = 'S'
        print("Grammar: ", TEST_A)

        eliminated_A = cnf.epsilon_elim(grammar.start, TEST_A)
        for key, val in eliminated_A.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
                print("all epsilon occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_A[grammar.start], ERRMSG_ELIM)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_A[grammar.start], "\n")
        # print(eliminated_A)

    def test_elim_B(self):
        grammar = eingabe.cfg()

        grammar.start = 'S'
        grammar.variables = list(key for key in TEST_B)
        print("Grammar: ", TEST_B)

        eliminated_B = cnf.epsilon_elim(grammar.start, TEST_B)

        for key, val in eliminated_B.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
                print("all epsilon occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_B[grammar.start], ERRMSG_ELIM)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_B[grammar.start], "\n")

    def test_elim_C(self):
        grammar = eingabe.cfg

        grammar.variables = set(key for key in TEST_C)
        grammar.start = 'S'
        print("Grammar: ", TEST_C)
        eliminated_C = cnf.epsilon_elim(grammar.start, TEST_C)
        eliminated_C = cnf.longright_elim(grammar.variables, eliminated_C)

        for key, val in eliminated_C.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
                print("all epsilon occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_C[grammar.start], ERRMSG_ELIM)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_C[grammar.start])
        print(eliminated_C)

    def test_elim_D(self):
        grammar = eingabe.cfg
        grammar.variables = list(key for key in TEST_D)
        grammar.start = 'S'
        print("Grammar: ", TEST_D)

        eliminated_D = cnf.epsilon_elim(grammar.start, TEST_D)
        for key, val in eliminated_D.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
                print("all epsilon occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_D[grammar.start], ERRMSG_ELIM)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_D[grammar.start], "\n")

    def test_elim_E(self):
        grammar = eingabe.cfg
        grammar.variables = list(key for key in TEST_E)
        grammar.start = 'S'
        print_grammar(TEST_E)

        eliminated_D = cnf.epsilon_elim(grammar.start, TEST_E)
        for key, val in eliminated_D.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
                print("all epsilon occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_D[grammar.start], ERRMSG_ELIM)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_D[grammar.start], "\n")
        print_grammar(eliminated_D)


class TestNonIsoTerm(unittest.TestCase):

    def test_nonisoterm_E(self):
        grammar = eingabe.cfg()
        grammar.rules = TEST_E
        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_E)
        grammar.start = 'S'
        print_grammar(TEST_E)

        grammar.rules = cnf.noniso_term_elim(grammar)
        print_grammar(grammar.rules)

        for key, value in grammar.rules.items():
            for val in value:
                for term in grammar.alphabet:
                    self.assertNotIn(term, val, ERRMSG_NONISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols.")


class TestLongRight(unittest.TestCase):
    def test_long_right_A(self):
        grammar = eingabe.cfg()

        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_A)
        grammar.start = 'S'
        print("Grammar: ", TEST_A)
        shorted_A = cnf.longright_elim(set(grammar.variables), TEST_A)
        print_grammar(shorted_A)
        for key, value in shorted_A.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for TEST_A: ")
        print_grammar(TEST_A)

    def test_long_right_B(self):
        grammar = eingabe.cfg()

        print_grammar(TEST_B)
        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_B)
        grammar.start = 'S'

        shorted_B = cnf.longright_elim(set(grammar.variables), TEST_B)
        for key, value in shorted_B.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for TEST_B: ")
        print_grammar(shorted_B)

    def test_long_right_C(self):
        grammar = eingabe.cfg()

        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_C)
        grammar.start = 'S'
        print("Grammar: ", TEST_C)
        shorted_C = cnf.longright_elim(set(grammar.variables), TEST_C)
        print_grammar(shorted_C)
        for key, value in shorted_C.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for TEST_C: ", TEST_C)

    def test_long_right_D(self):
        grammar = eingabe.cfg()

        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_D)
        grammar.start = 'S'
        print("Grammar: ", TEST_D)
        shorted_D = cnf.longright_elim(set(grammar.variables), TEST_D)
        print_grammar(shorted_D)
        for key, value in shorted_D.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for TEST_D: ")


class TestALL(unittest.TestCase):
    def test_ALL_A(self):
        print("Test A:")
        print_grammar(TEST_A)
        grammar = eingabe.cfg
        grammar.alphabet = {'a', 'b'}
        grammar.rules = TEST_A
        grammar.variables = list(key for key in TEST_A)
        grammar.start = 'S'
        chomsky_grammar_A = cnf.cnf(grammar)

        for key, val in chomsky_grammar_A.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        self.assertIn(r'\E', chomsky_grammar_A[grammar.start], ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")
        for key, value in chomsky_grammar_A.items():
            for val in value:
                for term in grammar.alphabet:
                    if term is not val:
                        self.assertNotIn(term, val, ERRMSG_NONISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols. ")

        for key, value in chomsky_grammar_A.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for chomsky_grammar: ")
        print_grammar(chomsky_grammar_A)

        print("\n\n")

    def test_ALL_B(self):

        print("Test B:")
        print_grammar(TEST_B)

        grammar = eingabe.cfg
        grammar.rules = TEST_B
        grammar.variables = list(key for key in TEST_B)
        grammar.start = 'S'
        grammar.alphabet = {'a', 'b', 'c'}
        chomsky_grammar_B = cnf.cnf(grammar)

        for key, val in chomsky_grammar_B.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        self.assertIn(r'\E', chomsky_grammar_B[grammar.start], ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")

        for key, value in chomsky_grammar_B.items():
            for val in value:
                for term in grammar.alphabet:
                    if term is not val:
                        self.assertNotIn(term, val, ERRMSG_NONISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols. ")

        for key, value in chomsky_grammar_B.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for chomsky_grammar: ")
        print_grammar(chomsky_grammar_B)

        print("\n\n")

    def test_ALL_C(self):
        print("Test C:")
        print_grammar(TEST_C)
        grammar = eingabe.cfg
        grammar.rules = SortedDict(TEST_C)
        grammar.variables = list(key for key in TEST_C)
        grammar.alphabet = {'a','b'}
        grammar.start = 'S'
        chomsky_grammar_C = cnf.cnf(grammar)

        for key, val in chomsky_grammar_C.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        self.assertIn(r'\E', chomsky_grammar_C[grammar.start], ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")

        for key, value in chomsky_grammar_C.items():
            for val in value:
                for term in grammar.alphabet:
                    if term is not val:
                        self.assertNotIn(term, val, ERRMSG_NONISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols.")

        for key, value in chomsky_grammar_C.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for chomsky_grammar: ")
        print_grammar(chomsky_grammar_C)
        print("\n\n")

    def test_ALL_D(self):

        print("Test D:")
        print_grammar(TEST_D)

        grammar = eingabe.cfg
        grammar.rules = TEST_D
        grammar.variables = list(key for key in TEST_D)
        grammar.start = 'S'
        chomsky_grammar_D = cnf.cnf(grammar)
        for key, val in chomsky_grammar_D.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        self.assertIn(r'\E', chomsky_grammar_D[grammar.start], ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")

        for key, value in chomsky_grammar_D.items():
            for val in value:
                for term in grammar.alphabet:
                    if term is not val:
                        self.assertNotIn(term, val, ERRMSG_NONISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols. ")

        for key, value in chomsky_grammar_D.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for chomsky_grammar: ")
        print_grammar(chomsky_grammar_D)
        print("\n\n")

    def test_ALL_E(self):
        print("Test E:")
        print_grammar(TEST_E)

        grammar = eingabe.cfg
        grammar.alphabet = {'a', 'b'}
        grammar.rules = TEST_E
        grammar.variables = list(key for key in TEST_E)
        grammar.start = 'S'
        print_grammar(grammar.rules)
        chomsky_grammar_E = cnf.cnf(grammar)

        for key, val in chomsky_grammar_E.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        self.assertIn(r'\E', chomsky_grammar_E[grammar.start], ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")

        for key, value in chomsky_grammar_E.items():
            for val in value:
                for term in grammar.alphabet:
                    if term is not val:
                        self.assertNotIn(term, val, ERRMSG_NONISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols. ")

        for key, value in chomsky_grammar_E.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONGRIGHT)
        print("successfully eliminated long right sides for chomsky_grammar: ")
        print_grammar(chomsky_grammar_E)
        print("\n\n")


def print_grammar(rules):
    for key, value in rules.items():
        print(key, " --> ", value)
    print("\n")


if __name__ == '__main__':
    unittest.main()
