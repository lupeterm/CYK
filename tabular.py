"""format CYK table to LaTeX string"""
from string import Template
import tabulate


def to_latex(table, word, start):
    """still formatting"""

    # custom indices for table
    v_indices = [str(x + 1)for x in range(len(word))]
    h_indices = [word[x - 1] for x in range(1, len(word)+1)]

    # import the template
    template = ''.join(open("latex_template.txt.txt", "r").read().splitlines())
    latex_string = str(tabulate.tabulate(table,
                                         tablefmt="latex",
                                         showindex=iter(v_indices),
                                         headers=iter(h_indices)))

    # conclusion and insertion of cyk table
    if table[0][-1]:
        is_in = r'$w \in L$' if start in table[0][-1][0] else r'$w \notin L$'
    else:
        is_in = r'$w \notin L$'
    latex_string = Template(template).safe_substitute(table=latex_string, word=is_in)

    # center columns
    latex_string = latex_string.replace(r'\begin{tabular}'r'{r' + ("l" * len(word)),
                                        r"\begin{tabular}{|r" + "|c" * len(word) + "|")

    # cosmetics
    latex_string = latex_string.replace("['", r'\{')
    latex_string = latex_string.replace("']", r'\}')
    latex_string = latex_string.replace("', '", ", ")
    latex_string = latex_string.replace("1 & ", "\\hline\n 1 & ", 1)
    latex_string = latex_string.replace("[]", r'$\emptyset$')

    return latex_string
