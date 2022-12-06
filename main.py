import subprocess
import cfg_input
import cyk.cyk as cyk
import tabular.tabular as tabular
import cnf.cnf as cnf
import cnf.cnf_test as cnf_test
import copy


def run_pdflatex(file_name: str = "CYK_Tableau.tex", path: str = "."):
    """
    Call pdflatex on the genereated .tex file to create the PDF
    """
    return subprocess.call(['pdflatex', file_name], cwd=path)

def main(): 
    grammar = cfg_input.CFG()

    if input("Do you want to import your grammar? [y/N] ") in ['Y', 'y']:
        grammar.file_input()
    else:
        grammar.new_grammar()

    word = input("Please enter the word. \n")

    grammar_copy = copy.deepcopy(grammar.rules)
    cnf_test.print_grammar(grammar.rules)
    grammar.rules = cnf.transform_to_cnf(grammar)

    print("Transformation to context-free grammar done.")

    cnf_test.print_grammar(grammar.rules)
    table = cyk.cyk(grammar, word)

    if input("Do you want to export your table as markdown or LaTeX? [M/L] ") in ['L']:
        tableau = tabular.to_latex(table, word, grammar.start, grammar.rules, grammar_copy)
        with open(file = "CYK_Tableau.tex", mode = "w") as file:
            file.write(tableau)
            print(f"\nWritten output to {file.name}")
            run_pdflatex()
            print("\nOutput saved to CYK_Tableau.pdf")
    else:
        tableau = tabular.to_markdown(table, word, grammar.start)
        with open(file = "CYK_Tableau.md", mode = "w") as file:
            file.write(tableau)
            print(f"\nWritten output to {file.name}")


if __name__ == "__main__":
    main()
