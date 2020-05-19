import eingabe
import cyk
import tabular



word = eingabe.new_word()
grammar = cfg ()
cfg.new_grammar(grammar)
#hier wird cnf aufgerufen
table = cyk.cyk(word)

tableau = tabular.to_latex(table,len(word))

file = open(file="CYK_Tableau.tex", mode="w")
file.write(tableau)
print("\nwritten in CYK_Tableau.tex")
