import string

import cyk

ALPH = set(string.ascii_uppercase)


def cnf(grammar):
    grammar.rules = epsilon_elim(grammar.start, grammar.rules)   # epsilon elimination
    grammar.rules = longright_elim(grammar.variables, grammar.rules) # long right side elimination
    return grammar.rules


def epsilon_elim(start, rules):
    # get keys that lead to epsilon and then transform other rules
    eps = r'\E'
    eps_keys = cyk.check_rule(rules, eps)  # find occurrences of epsilon in rules
    if not eps_keys:
        return rules
    for key, value in rules.items():
        tmpkey = set()
        tmprule = set()
        for v in value:
            tmpkey.update(char for char in eps_keys if char in v) # get keys to remove from tmpkey
            tmprule.update(v.replace(char, "") for char in tmpkey for v in value if
                           char in v)  # create rules by removing characters
        value.update(tmprule)

    for key, val in rules.items():  # replace empty sets with epsilon
        for v in val:
            if v == '':
                val.add(r'\E')
                val.remove('')
    for e in eps_keys:    # remove epsilon from all rules and add one to S
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


def longright_elim(variables, rules):
    global ALPH  # use set of the literal alphabet
    ALPH -= set(variables)  # minus the alphabet of the CFG
    new_rules = {}
    for key in list(rules.keys()):
        tmpval = (rules.get(key))  # values per key
        tmpcpy = tmpval  # mutable copy of tmpval
        repeat = False  # in case we have to iterate multiple times
        for val in tmpval:
            if len(val) > 2:
                repeat = True
                new_key = ALPH.pop()  # generates new key while also preventing multi-usage of characters
                new_values = {val[-2:]}  # last two characters of val
                val1 = val[:-2] + new_key  # create new rule out of lhs part of val and new key
                tmpcpy.remove(val)  # remove old rule
                tmpcpy.add(val1)  # add updated rule
                new_rules.update({new_key: new_values})
        new_rules.update({key: set(tmpval)})
        if repeat:
            longright_elim(set(x for x in new_rules.keys()), new_rules)
    return new_rules
