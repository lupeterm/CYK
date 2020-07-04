import cnf
import eingabe
import unittest

errmsg = "something went wrong: unexpected occurrence of '\E'"


class TestEpsilonElim(unittest.TestCase):
    def test_elim_A(self):
        grammar = eingabe.cfg()

        TEST_A = {
            'S': {'AA', 'AB'},
            'A': {'a', r'\E'},
            'B': {'BB', 'b'}
        }

        # grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_A)
        grammar.start = 'S'
        print("Grammar: ", TEST_A)

        eliminated_A = cnf.epsilon_elim(grammar.start, TEST_A)
        for key, val in eliminated_A.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, errmsg)
                print("all occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_A[grammar.start], errmsg)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_A[grammar.start], "\n")

    def test_elim_B(self):
        grammar = eingabe.cfg()
        TEST_B = {
            'S': {'TU'},
            'T': {'aTb', r'\E'},
            'U': {'Ucc', r'\E'}

        }
        grammar.start = 'S'
        grammar.variables = list(key for key in TEST_B)
        print("Grammar: ", TEST_B)

        eliminated_B = cnf.epsilon_elim(grammar.start, TEST_B)
        for key, val in eliminated_B.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, errmsg)
                print("all occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_B[grammar.start], errmsg)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_B[grammar.start], "\n")

    def test_elim_C(self):
        grammar = eingabe.cfg
        TEST_C = {
            'S': {'ASA', 'BSB', r'\E'},
            'A': {'a'},
            'B': {'b'}
        }
        grammar.variables = list(key for key in TEST_C)
        grammar.start = 'S'
        print("Grammar: ", TEST_C)
        eliminated_C = cnf.epsilon_elim(grammar.start, TEST_C)
        for key, val in eliminated_C.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, errmsg)
                print("all occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_C[grammar.start], errmsg)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_C[grammar.start], "\n")

    def test_elim_D(self):
        grammar = eingabe.cfg
        TEST_D = {
            'S': {'LR', r'\E'},
            'L': {'ALA', 'BLB', r'\E'},
            'R': {'ARA', 'BRB', r'\E'},
            'A': {'a'},
            'B': {'b'}

        }
        grammar.variables = list(key for key in TEST_D)
        grammar.start = 'S'
        print("Grammar: ", TEST_D)

        eliminated_D = cnf.epsilon_elim(grammar.start, TEST_D)
        for key, val in eliminated_D.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, errmsg)
                print("all occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_D[grammar.start], errmsg)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_D[grammar.start], "\n")

    if __name__ == '__main__':
        unittest.main()
