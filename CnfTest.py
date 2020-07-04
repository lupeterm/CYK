import cnf
import eingabe
import unittest

errmsg_elim = "something went wrong: unexpected occurrence of '\E'"
errmsg_longright = "something went wrong: expected length was <3"


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
                self.assertNotIn(r'\E', val, errmsg_elim)
                print("all occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_A[grammar.start], errmsg_elim)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_A[grammar.start], "\n")
        # print(eliminated_A)

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
                self.assertNotIn(r'\E', val, errmsg_elim)
                print("all occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_B[grammar.start], errmsg_elim)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_B[grammar.start], "\n")

    def test_elim_C(self):
        grammar = eingabe.cfg
        TEST_C = {
            'S': {'ASA', 'BSB', r'\E'},
            'A': {'a'},
            'B': {'b'}
        }
        grammar.variables = set(key for key in TEST_C)
        grammar.start = 'S'
        print("Grammar: ", TEST_C)
        eliminated_C = cnf.epsilon_elim(grammar.start, TEST_C)
        eliminated_C = cnf.longright_elim(grammar.variables, eliminated_C)

        for key, val in eliminated_C.items():
            if key is not grammar.start:
                self.assertNotIn(r'\E', val, errmsg_elim)
                print("all occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_C[grammar.start], errmsg_elim)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_C[grammar.start])
        print(eliminated_C)

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
                self.assertNotIn(r'\E', val, errmsg_elim)
                print("all occurences eliminated in ", key, ":", val)
        self.assertIn(r'\E', eliminated_D[grammar.start], errmsg_elim)
        print("added '\E'-rule for ", grammar.start, ":", eliminated_D[grammar.start], "\n")


class TestLongRight(unittest.TestCase):
    def test_long_right_A(self):
        grammar = eingabe.cfg()

        TEST_A = {
            'S': {'AA', 'AB'},
            'A': {'a', r'\E'},
            'B': {'BB', 'b'}
        }

        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_A)
        grammar.start = 'S'
        print("Grammar: ", TEST_A)
        shorted_A = cnf.longright_elim(set(grammar.variables), TEST_A)
        for key, value in shorted_A.items():
            for val in value:
                self.assertIsNot(len(val), len(val) > 2, errmsg_longright)
        print("successfully eliminated long right sides for TEST_A: ", TEST_A)

    def test_long_right_B(self):
        grammar = eingabe.cfg()

        TEST_B = {
            'S': {'TU'},
            'T': {'aTb', r'\E'},
            'U': {'Ucc', r'\E'}

        }

        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_B)
        grammar.start = 'S'
        print("Grammar: ", TEST_B)
        shorted_A = cnf.longright_elim(set(grammar.variables), TEST_B)
        for key, value in shorted_A.items():
            for val in value:
                self.assertIsNot(len(val), len(val) > 2, errmsg_longright)
        print("successfully eliminated long right sides for TEST_A: ", TEST_B)

    def test_long_right_C(self):
        grammar = eingabe.cfg()

        TEST_C = {
            'S': {'ASA', 'BSB', r'\E'},
            'A': {'a'},
            'B': {'b'}
        }

        grammar.alphabet = {'a', 'b'}
        grammar.variables = list(key for key in TEST_C)
        grammar.start = 'S'
        print("Grammar: ", TEST_C)
        shorted_A = cnf.longright_elim(set(grammar.variables), TEST_C)
        for key, value in shorted_A.items():
            for val in value:
                self.assertIsNot(len(val), len(val) > 2, errmsg_longright)
        print("successfully eliminated long right sides for TEST_A: ", TEST_C)

        def test_long_right_D(self):
            grammar = eingabe.cfg()

            TEST_D = {
                'S': {'LR', r'\E'},
                'L': {'ALA', 'BLB', r'\E'},
                'R': {'ARA', 'BRB', r'\E'},
                'A': {'a'},
                'B': {'b'}
            }

            grammar.alphabet = {'a', 'b'}
            grammar.variables = list(key for key in TEST_D)
            grammar.start = 'S'
            print("Grammar: ", TEST_D)
            shorted_A = cnf.longright_elim(set(grammar.variables), TEST_D)
            for key, value in shorted_A.items():
                for val in value:
                    self.assertIsNot(len(val), len(val) > 2, errmsg_longright)
            print("successfully eliminated long right sides for TEST_A: ", TEST_D)


if __name__ == '__main__':
    unittest.main()
