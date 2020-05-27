def cnf(grammar):
    ngrammar = epsilon_elim(grammar)
    return ngrammar


def epsilon_elim(grammar):
    V_Epsilon = []
    for var in grammar:  # grammar durchgehen
        for rule in grammar[var]:
            if rule == '/E':  # Epsilon-Regeln finden
                V_Epsilon.append(var)  # ... und abspeichern               +++
                grammar.pop(var[rule])  # ... und entfernen
        else:
            continue
    else:
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
