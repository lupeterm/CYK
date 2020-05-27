import eingabe

def cnf(grammar):
    ngrammar = epsilon_elim(grammar)
    return ngrammar


def epsilon_elim(grammar):
    V_Epsilon = set()
    for var in grammar:  # grammar durchgehen
        print(var + '   1')
        for rule in grammar[var]:
            print(rule + '   2')
            if rule == '\E':  # Epsilon-Regeln finden
                print('3')
                V_Epsilon.add(var)  # ... und abspeichern               +++
                del_rule = grammar[var]     # ... und Regeln aufspalten (für Löschung)
                print(grammar)
                i = del_rule.index('\E')
                del_rule1 = []
                del_rule2 = []
                j = 0
                while (j < i) :
                    del_rule1.append(del_rule[j])
                    j = j + 1
                for g in range(i+1, len(del_rule)):
                    del_rule2.append(del_rule[g])
                del_rule = del_rule1.extend(del_rule2)
                grammar = grammar.update({var : del_rule})  # ... und entfernen
                print(grammar)
            else:
                print('4')
                continue
    else:
        print('5')
        print(V_Epsilon)  # alle Epsilon-Variablen printen
        for var in grammar:  # grammar durchgehen
            for rule in grammar[var]:
                if var in V_Epsilon:  # alle Variablen mit Epsilon-Regel durchgehen
                    nrules = rek_nrules(rule, var, {})  # array für neue Regeln
                    grammar[var].apppend(nrules)  # neue Regeln hinzufügen
    return grammar


def rek_nrules(rule, var, nrule):               # nrule ist ein Set: keine Duplikate, ungeordnet
    x = rule.rindex(var)
    rule = rule[0:x - 1] + rule[x + 1:len(rule) - 1]
    nrule = nrule.append(rule)
    if var in rule:
        return rek_nrules(rule, var, nrule)
    else:
        return nrule

def cyclus_elim(grammar):
    ngrammar = rek_cyclus_elim(grammar, 0)  # Zyklen rekursiv finden
    return ngrammar


def rek_cyclus_elim(grammar, var):
    return


def chain_elim(grammar):
    return grammar


def uniso_term_right_elim(grammar):
    return grammar


def longright_elim(grammar):
    return grammar
