def check_rule(rules, rhs):
    symbols = [key for key, value in rules.items() if rhs in value]
    return symbols


def matrixmult(rules, lhs, rhs):
    non_terminals = []
    non_terminals_left = list()
    non_terminals_right = list()
    if len(lhs) > 2 and lhs[1].isnumeric():
        non_terminals_left.append(lhs[:2])
        non_terminals_left.append(lhs[2:])
    else:
        non_terminals_left = lhs
    if len(rhs) > 2 and rhs[1].isnumeric():
        non_terminals_right.append(rhs[:2])
        non_terminals_right.append(rhs[2:])
    else:
        non_terminals_right = rhs

    for nterms_left in non_terminals_left:
        for nterms_right in non_terminals_right:
            non_terminals.append(check_rule(rules, nterms_left + nterms_right))
    nonterminals_flatted = [x for inner in non_terminals for x in inner]
    return nonterminals_flatted


def cyk(grammar, word):
    tableau = []
    word_length = len(word)
    for i in range(0, word_length):
        tableau.append([""] * word_length)
        tableau[i][i] = [x for x in check_rule(grammar.rules, word[i])]

    for s in range(1, word_length):
        for i in range(1, word_length - s + 1):
            result = []
            for k in range(i, i + s):
                horizontal = tableau[i - 1][k - 1]
                vertical = tableau[k][i + s - 1]
                result += (matrixmult(grammar.rules, horizontal, vertical))
            tableau[i - 1][i + s - 1] = list(dict.fromkeys(result))
    return tableau
