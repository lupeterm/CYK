import eingabe
import cyk
import tabular
import cnf



word = eingabe.new_word()
grammar = eingabe.cfg()
eingabe.cfg.new_grammar(grammar)

grammar = cnf.epsilon_elim(grammar)             #hier wird cnf aufgerufen
table = cyk.cyk(word)

tableau = tabular.to_latex(table,len(word))

file = open(file="CYK_Tableau.tex", mode="w")
file.write(tableau)
print("\nwritten in CYK_Tableau.tex")
