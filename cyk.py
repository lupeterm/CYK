import eingabe


grammar = eingabe.cfg()
eingabe.cfg.new_grammar(grammar)


def check_rule(rhs):
    symbols = [key for key, value in grammar.rules.items() if rhs in value or rhs[::1] in value]
    
    return symbols


def matrix_mult(lhs, rhs):
    nonTs = []
    for ntl in lhs:
        for ntr in rhs:
            nonTs.append(check_rule( ntl + ntr))
    t = [x for inner in nonTs for x in inner]
    return t



def cyk(word):
    tableau = []
    n = len(word)
    for i in range(0, n):
        tableau.append([""] * n)
        tableau[i][i] = [x for x in check_rule(word[i])]

    for s in range(1, n):
        for i in range(1, n - s + 1):
            result = []
            for k in range(i, i + s):
                horizontal = tableau[i - 1][k - 1]
                vertical = tableau[k][i + s - 1]
                result += (matrix_mult(horizontal, vertical))
            tableau[i - 1][i + s - 1] = list(dict.fromkeys(result))
    return tableau