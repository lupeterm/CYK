import cyk
import eingabe


def cnf(grammar):
    nrules = epsilon_elim(grammar.start, grammar.rules)
    return nrules


def epsilon_elim(start,rules):
    # idea: get keys that lead to epsilon and then transform other rules
    eps = r'\E'
    eps_keys = cyk.check_rule(rules, eps)
    if not eps_keys:
        return rules
    for key, value in rules.items():
        tmpkey = set()
        tmprule = set()
        for v in value:
            tmpkey.update(char for char in eps_keys if char in v)
            tmprule.update(v.replace(char, "") for char in tmpkey for v in value if char in v)  # create rules by removing characters
        value.update(tmprule)


    for k, v in rules.items():
        for j in v:
            if j == '':
                v.add(r'\E')
                v.remove('')
    for e in eps_keys:
            rules[e].remove(r'\E')
    rules[start].add(r'\E')
    return rules


def rek_nrules(rule, var, nrule):  # nrule ist ein Set: keine Duplikate, ungeordnet
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
