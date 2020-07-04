import eingabe
import cyk
import tabular
import cnf

grammar = eingabe.cfg()
#eingabe.cfg.new_grammar(grammar)
word = eingabe.new_word()
grammar.rules = {
            'S': {'LR', r'\E'},
            'L': {'ALA', 'BLB', r'\E'},
            'R': {'ARA', 'BRB', r'\E'},
            'A': {'a'},
            'B': {'b'}
}
grammar.start = 'S'
grammar.variables = list(key for key in grammar.rules)
grammar.rules = cnf.cnf(grammar)  # bring CFG in Chomsky NF
table = cyk.cyk(grammar, word)       # run CYK algorithm
tableau = tabular.to_latex(table, len(word), grammar.start)  # format the CYK table into a LaTeX string

file = open(file="CYK_Tableau.tex", mode="w")
file.write(tableau)
print("\nwritten in CYK_Tableau.tex")
