import input
word = ["b", "a", "b", "a","b","a"]
n = len(word)
grammar = input.cfg
input.cfg.new_grammar(grammar)
print(grammar.rules)


# get index of nonterminal the rule "belongs" to
def check_rule(w_teil):
    for nonT_rules in grammar.rules:
        if nonT_rules.find(w_teil) != -1:
            return grammar.rules.index(nonT_rules)
    return 999

# to check if the word is in a language

def cyk(word):
    tableau = []
    # filling the diagonale with the nonterminals for each letter of the word
    for i in range(0, len(word)):
        tableau.append([""] * len(word))
        tableau[i][i] = grammar.variables[check_rule(word[i])]

    for s in range(1, n):
        for i in range(1, n - s + 1):
            for k in range(i, i + s):
                tmp1 = tableau[i-1][k-1]
                tmp2 = tableau[k][i + s-1]
                if check_rule(tmp1 + tmp2) != 999:
                    tableau[i-1][i + s-1] = grammar.rules[check_rule(tmp1 + tmp2)][0]


tab = cyk(word)
#  S, A
#  a
#  S -> SS | AA, A -> a
for i in tab:
    print(i)
if tab[0][-1]=="S":
    print("w is in L")
else:
    print("w is not in L")

#S-> XZ | ZY, X -> ZX | a, Y -> XZ | a, Z -> YY | b