import eingabe
import cyk
import tabular
import cnf
import cnfTest

grammar = eingabe.cfg()
#eingabe.cfg.new_grammar(grammar)
word = eingabe.new_word()
cnfTest.print_grammar(grammar.rules)
grammar.rules = {
            'S': {'aACa'},
            'A': {'B', 'a'},
            'B': {'C', 'c'},
            'C': {'cC', r'\E'}
        }
grammar.start = 'S'
grammar.alphabet = {'a', 'b', 'c'}
grammar.variables = set(key for key in grammar.rules)
grammar.rules = cnf.cnf(grammar)  # bring CFG in Chomsky NF
print("cnf done")
cnfTest.print_grammar(grammar.rules)
table = cyk.cyk(grammar, word)  # run CYK algorithm
tableau = tabular.to_latex(table, len(word), grammar.start)  # format the CYK table into a LaTeX string

file = open(file="CYK_Tableau.tex", mode="w")
file.write(tableau)
print("\nwritten in CYK_Tableau.tex")
