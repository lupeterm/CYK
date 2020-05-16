from string import Template
import cyk
import tabulate

def to_latex(table,length_word):
    v_indices = (str(x + 1) for x in range(length_word))
    h_indices = (str(x + 1) for x in range(length_word))

    latex_string = str(tabulate.tabulate(table, tablefmt="latex", showindex=iter(v_indices), headers=iter(h_indices)))
    latex_string = latex_string.replace("  1 & ", r"\hline \n  1 & ", 1)
    latex_string = latex_string.replace("[]", r"$\emptyset$")
    latex_string = Template(r'\documentclass[12pt]{article}\n \usepackage{threeparttable}\n \begin{document} \n $table\n \begin{tablenotes}\item[1] $wL$\end{tablenotes}\end{document}%').safe_substitute(table=latex_string)
    latex_string = latex_string.replace(r'\begin{tabular}{r"+"l"*n',r'\begin{tabular}{|r"+"|l"*n+"|')
    latex_string = latex_string.replace("['", r"\{")
    latex_string = latex_string.replace("']", r"\}")
    latex_string = latex_string.replace("', '", ", ")
    
    if table[0][-1] == []:
        latex_string = latex_string.replace(r"$wL$", r"$w \notin L$")
        return latex_string
    
    elif table[0][-1][0].find(cyk.grammar.rules[0][0]) != -1:
        latex_string = latex_string.replace("$wL$", r"$w \in L$")
        return latex_string
    
    else:
        latex_string = latex_string.replace(r"$wL$", r"$w \notin L$")
        return latex_string