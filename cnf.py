def cnf(grammar):
    ngrammar = epsilon_elim(grammar)
    return ngrammar

def epsilon_elim(grammar):
    V_Epsilon = []
    for var, rule in grammar:           # grammar durchgehen
        if rule == '/E':                # Epsilon-Regeln finden
            V_Epsilon.append(var)       # ... und abspeichern               +++
            grammar.pop(var[rule])      # ... und entfernen
        else:
            continue
    else:
        print(V_Epsilon)                # alle Epsilon-Variablen printen
        for var, rule in grammar:       # grammar durchgehen
            if var in V_Epsilon:        # alle Variablen mit Epsilon-Regel durchgehen
                nrules = []              # array für neue Regeln
                for i in range (len(rule)):     # rule Zeichen für Zeichen durchgehen           +++ find
                    if var == rule[i]:          # wenn Variable mit Epsilon-Regel an Stelle i der Regel auftaucht
                        nrules = nrules.append(rule[0:i-1] + rule[i+1: len(rule)-1])  # neue Regel mit String von rule ohne Stelle i
                        continue
                grammar[var].apppend(nrules)     # neue Regeln hinzufügen
    return grammar

def cyclus_elim(grammar):
    ngrammar = rek_cyclus_elim(grammar, 0)      # Zyklen rekursiv finden
    return ngrammar

def rek_cyclus_elim(grammar, var):

    return

def chain_elim(grammar):

    return grammar

def uniso_term_right_elim(grammar):

    return grammar

def longright_elim(grammar):

    return grammar