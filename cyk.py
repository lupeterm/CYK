def check_rule(rules, rhs):
    # gets keys for given right hand side
    symbols = [key for key, value in rules.items() if rhs in value]  # or rhs[::1] in value
    return symbols


def matrixmult(rules, lhs, rhs):
    nonTs = []
    for ntl in lhs:
        for ntr in rhs:
            nonTs.append(check_rule(rules, ntl + ntr))
    t = [x for inner in nonTs for x in inner]
    return t


def cyk(grammar, word):
    tableau = []
    n = len(word)
    for i in range(0, n):
        tableau.append([""] * n)
        tableau[i][i] = [x for x in check_rule(grammar.rules, word[i])]

    for s in range(1, n):
        for i in range(1, n - s + 1):
            result = []
            for k in range(i, i + s):
                horizontal = tableau[i - 1][k - 1]
                vertical = tableau[k][i + s - 1]
                result += (matrixmult(grammar.rules, horizontal, vertical))
            tableau[i - 1][i + s - 1] = list(dict.fromkeys(result))
    return tableau
