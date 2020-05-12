from string import Template
import cyk
import tabulate
import eingabe

def toLatex(tab):
    v_indices = (str(x + 1) for x in range(n))
    h_indices = (str(x + 1) for x in range(n))

    latex_string = str(tabulate.tabulate(tab, tablefmt="latex", showindex=iter(v_indices), headers=iter(h_indices)))
    test2 = latex_string.replace("  1 & ", "\hline \n  1 & ", 1)
    test3 = test2.replace("[]", "$\emptyset$")
    test3 = Template("\documentclass[12pt]{article}\n \\usepackage{threeparttable}\n \\begin{document} \n $table\n \\begin{tablenotes}\item[1] $wL$\end{tablenotes}\end{document}%").safe_substitute(table=test3)
    test4 = test3.replace("\\begin{tabular}{r"+"l"*n,"\\begin{tabular}{|r"+"|l"*n+"|")
    test5 = test4.replace("['", "\{")
    test6 = test5.replace("']", "\}")
    test7 = test6.replace("', '", ", ")
    if tab[0][-1][0].find(cyk.grammar.rules[0][0]) != -1:
        test8 = test7.replace("$wL$", "$w \in L$")
        return test8
    else:
        test8 = test7.replace("$wL$", "$w \\notin L$")
        return test8


word = cyk.get_word()
n = len(word)
tab = cyk.cyk(word)

tabular = toLatex(tab)

b = open(file="cyk.tex", mode="w")
b.write(tabular)
print(tabular)
print("\nwritten in test.tex")
