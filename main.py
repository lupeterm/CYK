"""run this file"""
import eingabe
import cyk
import tabular
import cnf
import cnf_test

grammar = eingabe.CFG()
# eingabe.cfg.new_grammar(grammar)
word = eingabe.new_word()
cnf_test.print_grammar(grammar.rules)
grammar.rules = dict(S={'aACa'}, A={'B', 'a'}, B={'C', 'c'}, C={'cC', r'\E'})
grammar.start = 'S'
grammar.alphabet = {'a', 'b', 'c'}
grammar.variables = set(key for key in grammar.rules)
grammar.rules = cnf.cnf(grammar)  # bring CFG in Chomsky NF
print("cnf done")
cnf_test.print_grammar(grammar.rules)
table = cyk.cyk(grammar, word)  # run CYK algorithm
tableau = tabular.to_latex(table, word, grammar.start, grammar.rules)
file = open(file="CYK_Tableau.tex", mode="w")
file.write(tableau)
file.close()
print("\nwritten in CYK_Tableau.tex")
