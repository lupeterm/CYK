import cnf
import eingabe


grammar = eingabe.cfg()

grammar.rules = {
    'S' :   ['AA' , 'AB'],
    'A' :   ['a' , '\E'],
    'B' :   ['BB' , 'b']
}

grammar.alphabet = ['a' , 'b']
grammar.variables = ['S' , 'A' , 'B']
grammar.start = 'S'

print(cnf.epsilon_elim(grammar.rules))