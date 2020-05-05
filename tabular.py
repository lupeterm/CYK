import numpy as np
from tabulate import tabulate
from string import Template
import string

cyk = []
w = "Hallo"
a = []
for i in w:
    a.append(i)
cyk.append(a)

for i in range(0, 6):
    cyk.append(np.random.choice(list(string.ascii_lowercase), size=5))

vindices = (str(x+1) for x in range(len(cyk)))
hindices = (str(x+1) for x in range(len(w)))
latex_string = str(tabulate(cyk, tablefmt="latex", showindex=iter(vindices), headers=iter(hindices)))
test = latex_string.replace("\\begin{tabular}{rlllll}", "\\begin{tabular}{|r|l|l|l|l|l|}", 1)
test2 = test.replace("  1 & ", "\hline \n  1 & ", 1)

test2 = Template("\documentclass[12pt]{article}\n \\begin{document} \n $table\n\end{document}%").safe_substitute(
    table=test2)

b = open(file="test6.tex", mode="w")
b.write(test2)
print(test2)
print("\nwritten in test.tex")
