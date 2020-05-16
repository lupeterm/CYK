import eingabe
import cyk
import tabular


word = eingabe.new_word()
n = len(word)
tab = cyk.cyk(word)

table = tabular.to_latex(tab,n)

b = open(file="cyk.tex", mode="w")
b.write(table)
print(table)
print("\nwritten in test.tex")
