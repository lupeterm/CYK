"""format CYK table to LaTeX string"""
from string import Template
import tabulate


def to_latex(table, word, start):
    """still formatting"""
    v_indices = [str(x + 1)for x in range(len(word))]
    h_indices = [word[x - 1] for x in range(1, len(word)+1)]
    template = "\\documentclass[10pt]{article}\n" \
               "\\usepackage{threeparttable}\n" \
               "\\usepackage[a4paper, left=0cm, right=0cm, top=2cm]{geometry}\n" \
               "\\begin{document}\n" \
               "$table\n" \
               "\\begin{tablenotes}\\item[1] $wL$\n " \
               "\\end{tablenotes}\n" \
               "\\end{document}%"
    latex_string = str(tabulate.tabulate(table,
                                         tablefmt="latex",
                                         showindex=iter(v_indices),
                                         headers=iter(h_indices)))
    latex_string = latex_string.replace("1 & ", "\\hline\n 1 & ", 1)
    latex_string = latex_string.replace("[]", r'$\emptyset$')
    latex_string = Template(template).safe_substitute(table=latex_string)
    latex_string = latex_string.replace(r'\begin{tabular}'r'{r' + ("l" * len(word)),
                                        r"\begin{tabular}{|r" + "|c" * len(word) + "|")
    latex_string = latex_string.replace("['", r'\{')
    latex_string = latex_string.replace("']", r'\}')
    latex_string = latex_string.replace("', '", ", ")
    if not table[0][-1]:
        latex_string = latex_string.replace(r'$wL$', r'$w \notin L$')
        return latex_string

    if table[0][-1][0].find(start) != -1:
        latex_string = latex_string.replace('$wL$', r'$w \in L$')
        return latex_string

    latex_string = latex_string.replace(r'$wL$', r'$w \notin L$')
    return latex_string
