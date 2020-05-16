import eingabe

grammar = eingabe.cfg
eingabe.cfg.new_grammar(grammar)


def check_rule(rhs):
    indices = []
    for lhs in grammar.rules:
        if lhs.find(rhs) != -1:
            indices.append(grammar.rules.index(lhs))
        elif lhs.find(rhs[::1]) != -1 and len(rhs) > 1:
            indices.append(grammar.rules.index(lhs))
    return indices


def matrix_mult(lhs, rhs):
    nonTs = []
    for ntl in lhs:
        for ntr in rhs:
            nonTs.append(grammar.rules[x][0] for x in check_rule(ntl + ntr))
    t = [x for inner in nonTs for x in inner]
    return t


tableau = []


def cyk(word):
    n = len(word)
    for i in range(0, n):
        tableau.append([""] * n)
        tableau[i][i] = [grammar.variables[x] for x in check_rule(word[i])]

    for s in range(1, n):
        for i in range(1, n - s + 1):
            result = []
            for k in range(i, i + s):
                horizontal = tableau[i - 1][k - 1]
                vertical = tableau[k][i + s - 1]
                result += (matrix_mult(horizontal, vertical))
            tableau[i - 1][i + s - 1] = list(dict.fromkeys(result))
    return tableau