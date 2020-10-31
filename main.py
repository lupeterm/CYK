"""run this file"""
import subprocess
import eingabe
import cyk
import tabular
import cnf
import cnf_test
import copy

def run_pdflatex(file_name='CYK_Tableau.tex', path='.'):
    """convert tex file to pdf"""
    return subprocess.call(['pdflatex', file_name], cwd=path)


grammar = eingabe.CFG()
if input("Do you want to import your Grammar? [y/N] ") in ['Y', 'y']:
    eingabe.CFG.file_input(grammar)
else:
    eingabe.CFG.new_grammar(grammar)
    
word = eingabe.new_word()
# cnf_test.print_grammar(grammar.rules)
# grammar.rules = dict(S={'aACa'}, A={'B', 'a'}, B={'C', 'c'}, C={'cC', r'\E'})
# grammar.start = 'S'
# grammar.alphabet = {'a', 'b', 'c'}
# grammar.variables = set(key for key in grammar.rules)
saveGrammar = copy.deepcopy(grammar.rules)
grammar.rules = cnf.cnf(grammar)  # bring CFG in Chomsky NF
print("cnf done")
cnf_test.print_grammar(grammar.rules)
table = cyk.cyk(grammar, word)  # run CYK algorithm
tableau = tabular.to_latex(table, word, grammar.start, grammar.rules, saveGrammar)
file = open(file="CYK_Tableau.tex", mode="w")
file.write(tableau)
file.close()
print('\nwritten in CYK_Tableau.tex')
run_pdflatex()
print('\noutput saved to CYK_Tableau.pdf')
