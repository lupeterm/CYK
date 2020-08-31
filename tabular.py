from string import Template
import tabulate


def to_latex(table, length_word, start):
    v_indices = (str(x + 1) for x in range(length_word))
    h_indices = (str(x + 1) for x in range(length_word))
    template = r'\documentclass[10pt]{article}\n ' \
               r'\usepackage{threeparttable}\n ' \
               r'\usepackage[a4paper, left=0cm, right=0cm, top=2cm]{geometry}\n ' \
               r'\begin{document} \n ' \
               r'$table\n ' \
               r'\begin{tablenotes}\item[1] $wL$\end{tablenotes}' \
               r'\end{document}%'
    latex_string = str(tabulate.tabulate(table, tablefmt="latex", showindex=iter(v_indices), headers=iter(h_indices)))
    latex_string = latex_string.replace("  1 & ", r"\hline \n  1 & ", 1)
    latex_string = latex_string.replace("[]", r"$\emptyset$")
    latex_string = Template(template).safe_substitute(table=latex_string)
    latex_string = latex_string.replace(r'\begin{tabular}'r'{r' + "l" * length_word,
                                        r"\begin{tabular}{|r" + "|c" * length_word + "|")
    latex_string = latex_string.replace("['", r"\{")
    latex_string = latex_string.replace("']", r"\}")
    latex_string = latex_string.replace("', '", ", ")
    if not table[0][-1]:
        latex_string = latex_string.replace(r"$wL$", r"$w \notin L$")
        return latex_string

    elif table[0][-1][0].find(start) != -1:
        latex_string = latex_string.replace("$wL$", r"$w \in L$")
        return latex_string

    else:
        latex_string = latex_string.replace(r"$wL$", r"$w \notin L$")
        return latex_string
