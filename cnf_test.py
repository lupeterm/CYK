"""module for unit testing"""
import unittest
import cnf
import eingabe
import cyk

ERRMSG_ELIM = r'something went wrong: unexpected occurrence of \E.'
ERRMSG_NON_ISO = "something went wrong: unexpected occurrence of terminal symbol."
ERRMSG_LONG_RIGHT = "something went wrong: expected length was <3."
ERRMSG_CHAIN = "something went wrong: unexpected single non-terminal symbol."


class TestCasesA(unittest.TestCase):
    """Unittests for cnf.py"""
    def setUp(self) -> None:
        self.grammar = eingabe.CFG()
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
        """unit test epsilon elimination"""
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in self.grammar.rules.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated_ all occurrences of epsilon:")
        print_grammar(self.grammar.rules)

    def test_elim_chains(self):
        """unit test of elimination of chained rules"""
        eliminated_a = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_a.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_a)

    def test_elim_nonisoterm(self):
        """unit test of elimination of non-isolated terminal symbols"""
        self.grammar.rules = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )

        for value in self.grammar.rules.values():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        """unit test of elimination of long right sides"""
        self.grammar.rules = cnf.cnf(self.grammar)
        print_grammar(self.grammar.rules)
        for value in self.grammar.rules.values():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_A: ")
        print_grammar(self.grammar.rules)


class TestCasesB(unittest.TestCase):
    """Unittests for cnf.py"""

    def setUp(self):
        self.grammar = eingabe.CFG()
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
        """unit test epsilon elimination"""

        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        eps_keys = cyk.check_rule(self.grammar.rules, r'\E')
        self.assertLessEqual(len(eps_keys), 1)
        if len(eps_keys) == 1:
            self.assertIn(self.grammar.start, eps_keys)
        print("eliminated_ all occurrences of epsilon:")
        print_grammar(self.grammar.rules)

    def test_elim_chains(self):
        """unit test of elimination of chained rules"""
        eliminated_b = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_b.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_b)

    def test_elim_nonisoterm(self):
        """unit test of elimination of non-isolated terminal symbols"""
        eliminated_b = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        print_grammar(self.grammar.rules)

        for value in eliminated_b.values():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        """unit test of elimination of long right sides"""
        shorted_b = cnf.long_right_elim(self.grammar.rules)
        for value in shorted_b.values():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_A: ")
        print_grammar(shorted_b)


class TestCasesC(unittest.TestCase):
    """Unittests for cnf.py"""

    def setUp(self):
        self.grammar = eingabe.CFG()
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
        """unit test epsilon elimination"""

        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        eliminated_c = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in eliminated_c.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated_ all occurrences of epsilon:")
        print_grammar(eliminated_c)

    def test_elim_chains(self):
        """unit test of elimination of chained rules"""
        eliminated_c = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_c.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_c)

    def test_elim_nonisoterm(self):
        """unit test of elimination of non-isolated terminal symbols"""
        eliminated_c = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        print_grammar(self.grammar.rules)

        for value in eliminated_c.values():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        """unit test of elimination of long right sides"""
        shorted_c = cnf.long_right_elim(self.grammar.rules)
        for value in shorted_c.values():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_A: ")
        print_grammar(shorted_c)


class TestCasesD(unittest.TestCase):

    """Unittests for cnf.py"""

    def setUp(self):
        self.grammar = eingabe.CFG()
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
        """unit test epsilon elimination"""

        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        print_grammar(self.grammar.rules)
        for key, val in self.grammar.rules.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated_ all occurrences of epsilon:")

    def test_elim_chains(self):
        """unit test of elimination of chained rules"""
        eliminated_d = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_d.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_d)

    def test_elim_nonisoterm(self):
        """unit test of elimination of non-isolated terminal symbols"""
        eliminated_d = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet)
        print_grammar(self.grammar.rules)

        for value in eliminated_d.values():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        """unit test of elimination of long right sides"""
        self.grammar.rules = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        print_grammar(self.grammar.rules)
        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        print_grammar(self.grammar.rules)
        self.grammar.rules = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        print_grammar(self.grammar.rules)
        shorted_d = cnf.long_right_elim(self.grammar.rules)
        for value in shorted_d.values():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_A: ")
        print_grammar(shorted_d)


class TestCasesE(unittest.TestCase):
    """Unittests for cnf.py"""

    def setUp(self):
        self.grammar = eingabe.CFG()
        self.grammar = eingabe.CFG()
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
        """unit test epsilon elimination"""

        self.grammar.rules = cnf.chain_elim(self.grammar.rules)
        eliminated_e = cnf.epsilon_elim(self.grammar.start, self.grammar.rules)
        for key, val in eliminated_e.items():
            if key is not self.grammar.start:
                self.assertNotIn(r'\E', val, ERRMSG_ELIM)
        print("eliminated_ all occurrences of epsilon:")
        print_grammar(eliminated_e)

    def test_elim_chains(self):
        """unit test of elimination of chained rules"""
        eliminated_e = cnf.chain_elim(self.grammar.rules)
        for values in eliminated_e.values():
            for val in values:
                self.assertFalse(val.isupper() and len(val) == 1, ERRMSG_CHAIN)
        print("eliminated_ all occurrences of chained rules:")
        print_grammar(eliminated_e)

    def test_elim_nonisoterm(self):
        """unit test of elimination of non-isolated terminal symbols"""
        eliminated_e = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        print_grammar(self.grammar.rules)

        for value in eliminated_e.values():
            for string in value:
                if len(string) > 1:
                    for term in self.grammar.alphabet:
                        self.assertNotIn(term, string, ERRMSG_NON_ISO)
        print("Successfully eliminated_ all occurrences of non-isolated terminal symbols.")

    def test_elim_long_right(self):
        """unit test of elimination of long right sides"""
        self.grammar.rules = cnf.non_iso_term_elim(
            self.grammar.rules, self.grammar.variables, self.grammar.alphabet
        )
        print_grammar(self.grammar.rules)
        shorted_e = cnf.long_right_elim(self.grammar.rules)
        print_grammar(shorted_e)
        for value in shorted_e.values():
            for val in value:
                self.assertIsNot(len(val), 3 or 4 or 5, ERRMSG_LONG_RIGHT)
        print("successfully eliminated_ long right sides for TEST_E: ")


def print_grammar(rules):
    """pretty print grammar"""
    for key, value in rules.items():
        print(key, " --> ", value)
    print("\n")


if __name__ == '__main__':
    unittest.main()
