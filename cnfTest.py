import cnf
import eingabe
import unittest
import cyk

ERRMSG_ELIM = "something went wrong: unexpected occurrence of '\E'."
ERRMSG_NON_ISO = "something went wrong: unexpected occurrence of terminal symbol."
ERRMSG_LONG_RIGHT = "something went wrong: expected length was <3."
ERRMSG_CHAIN = "something went wrong: unexpected single non-terminal symbol."


class TestCases_A(unittest.TestCase):

    def setUp(self) -> None:
        self.grammar = eingabe.cfg()
        self.grammar.rules = {
            'S': {'aACa'},
            'A': {'B', 'a'},
            'B': {'C', 'c'},
            'C': {'cC', r'\E'}
        }
        self.grammar.alphabet = {'a', 'b', 'c'}
        self.grammar.variables = set(key for key in self.grammar.rules)
        self.grammar.start = 'S'
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in self.grammar.rules.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")
        print_grammar(self.grammar.rules)

    def test_elim_chains(self):
        eliminated_A = cnf.chain_elim(self.grammar.rules)
        for key, values in eliminated_A.items():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated all occurrences of chained rules:")
        print_grammar(eliminated_A)

    def test_elim_nonisoterm(self):

        self.grammar.rules = cnf.non_iso_term_elim(self.grammar.rules, self.grammar.variables, self.grammar.alphabet)

        for key, value in self.grammar.rules.items():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        self.grammar.rules = cnf.cnf(self.grammar)
        print_grammar(self.grammar.rules)
        for key, value in self.grammar.rules.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated long right sides for TEST_A: ")
        print_grammar(self.grammar.rules)


class TestCases_B(unittest.TestCase):

    def setUp(self):
        self.grammar = eingabe.cfg()
        self.grammar.rules = {
            'S': {'TU'},
            'T': {'aTb', r'\E'},
            'U': {'R'},
            'R': {'Ucc', r'\E'}
        }
        self.grammar.alphabet = {'a', 'b', 'c'}
        self.grammar.variables = set(key for key in self.grammar.rules)
        self.grammar.start = 'S'
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        eps_keys = cyk.check_rule(self.grammar.rules, r'\E')
        self.assertLessEqual(len(eps_keys), 1)
        if len(eps_keys) == 1:
            self.assertIn(self.grammar.start, eps_keys)
        print("eliminated all occurrences of epsilon:")
        print_grammar(self.grammar.rules)

    def test_elim_chains(self):
        eliminated_B = cnf.chain_elim(self.grammar.rules)
        for key, values in eliminated_B.items():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated all occurrences of chained rules:")
        print_grammar(eliminated_B)

    def test_elim_nonisoterm(self):

        eliminated_B = cnf.non_iso_term_elim(self.grammar.rules, self.grammar.variables, self.grammar.alphabet)
        print_grammar(self.grammar.rules)

        for key, value in eliminated_B.items():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        shorted_B = cnf.long_right_elim(self.grammar.rules)
        for key, value in shorted_B.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated long right sides for TEST_A: ")
        print_grammar(shorted_B)


class TestCases_C(unittest.TestCase):

    def setUp(self):
        self.grammar = eingabe.cfg()
        self.grammar.rules = {
            'S': {'ASA', 'BSB', r'\E'},
            'A': {'a'},
            'B': {'b'}
        }
        self.grammar.alphabet = {'a', 'b'}
        self.grammar.variables = set(key for key in self.grammar.rules)
        self.grammar.start = 'S'
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):
        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        eliminated_C = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in eliminated_C.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")
        print_grammar(eliminated_C)

    def test_elim_chains(self):
        eliminated_C = cnf.chain_elim(self.grammar.rules)
        for key, values in eliminated_C.items():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated all occurrences of chained rules:")
        print_grammar(eliminated_C)

    def test_elim_nonisoterm(self):

        eliminated_C = cnf.non_iso_term_elim(self.grammar.rules, self.grammar.variables, self.grammar.alphabet)
        print_grammar(self.grammar.rules)

        for key, value in eliminated_C.items():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        shorted_C = cnf.long_right_elim(self.grammar.rules)
        for key, value in shorted_C.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated long right sides for TEST_A: ")
        print_grammar(shorted_C)


class TestCases_D(unittest.TestCase):

    def setUp(self):
        self.grammar = eingabe.cfg()
        self.grammar.rules = {
            'S': {'LR', r'\E'},
            'L': {'ALLA', 'BLLB', r'\E'},
            'R': {'ARA', 'BRB', r'\E'},
            'A': {'a'},
            'B': {'b'}
        }
        self.grammar.alphabet = {'a', 'b'}
        self.grammar.variables = set(key for key in self.grammar.rules)
        self.grammar.start = 'S'
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):
        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        print_grammar(self.grammar.rules)
        for key, val in self.grammar.rules.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")

    def test_elim_chains(self):
        eliminated_D = cnf.chain_elim(self.grammar.rules)
        for key, values in eliminated_D.items():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated all occurrences of chained rules:")
        print_grammar(eliminated_D)

    def test_elim_nonisoterm(self):

        eliminated_D = cnf.non_iso_term_elim(self.grammar.rules, self.grammar.variables, self.grammar.alphabet)
        print_grammar(self.grammar.rules)

        for key, value in eliminated_D.items():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        print_grammar(self.grammar.rules)
        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        print_grammar(self.grammar.rules)
        self.grammar.rules = cnf.non_iso_term_elim(self.grammar.rules, self.grammar.variables, self.grammar.alphabet)
        print_grammar(self.grammar.rules)
        shorted_D = cnf.long_right_elim(self.grammar.rules)
        for key, value in shorted_D.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated long right sides for TEST_A: ")
        print_grammar(shorted_D)


class TestCases_E(unittest.TestCase):

    def setUp(self):
        self.grammar = eingabe.cfg()
        self.grammar = eingabe.cfg()
        self.grammar.rules = {
            'S': {'aaA'},
            'A': {'BAB', 'B', r'\E'},
            'B': {'bb'}
        }
        self.grammar.alphabet = {'a', 'b'}
        self.grammar.variables = set(key for key in self.grammar.rules)
        self.grammar.start = 'S'
        print("grammar:")
        print_grammar(self.grammar.rules)

    def test_epsilon_elim(self):
        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        eliminated_E = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in eliminated_E.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated all occurrences of epsilon:")
        print_grammar(eliminated_E)

    def test_elim_chains(self):
        eliminated_E = cnf.chain_elim(self.grammar.rules)
        for key, values in eliminated_E.items():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated all occurrences of chained rules:")
        print_grammar(eliminated_E)

    def test_elim_nonisoterm(self):

        eliminated_E = cnf.non_iso_term_elim(self.grammar.rules, self.grammar.variables, self.grammar.alphabet)
        print_grammar(self.grammar.rules)

        for key, value in eliminated_E.items():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        self.grammar.rules = cnf.non_iso_term_elim(self.grammar.rules, self.grammar.variables, self.grammar.alphabet)
        print_grammar(self.grammar.rules)
        shorted_E = cnf.long_right_elim(self.grammar.rules)
        print_grammar(shorted_E)
        for key, value in shorted_E.items():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated long right sides for TEST_E: ")


def print_grammar(rules):
    for key, value in rules.items():
        print(key, " --> ", value)
    print("\n")


if __name__ == '__main__':
    unittest.main()
