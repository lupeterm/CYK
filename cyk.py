import eingabe

grammar = eingabe.cfg
eingabe.cfg.new_grammar(grammar)


def get_word():
    word = input("what is the word?\n")
    c = []
    for i in word:
        c.append(i)
    return c


# get index of nonterminal the rule "belongs" to
def check_rule(nonTs):
    indices = []
    for lhs in grammar.rules:
        if lhs.find(nonTs) != -1:
            indices.append(grammar.rules.index(lhs))
        elif lhs.find(nonTs[::1]) != -1 and len(nonTs) > 1:
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
    # filling the diagonale with the nonterminals for each letter of the word
    n = len(word)
    for i in range(0, n):
        tableau.append([""] * n)
        tableau[i][i] = [grammar.variables[x] for x in check_rule(word[i])]

    for s in range(1, n):
        for i in range(1, n - s + 1):
            res = []
            for k in range(i, i + s):
                horizontal = tableau[i - 1][k - 1]
                vertical = tableau[k][i + s - 1]
                res += (matrix_mult(horizontal, vertical))
            tableau[i - 1][i + s - 1] = list(dict.fromkeys(res))
    return tableau


#word = get_word()
#n = len(word)
#tab = cyk(word)
#  S, A
#  a
#  S -> SS | AA, A -> a
#for i in tab:
#    print(i)


# S-> XZ | ZY, X -> ZX | a, Y -> XZ | a, Z -> YY | b
