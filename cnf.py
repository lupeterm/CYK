import string
from sortedcontainers import SortedSet
import cyk

ALPH = SortedSet(string.ascii_uppercase)


def cnf(grammar):
    grammar.rules = epsilon_elim(grammar.start, grammar.rules)  # epsilon elimination

    grammar.rules = noniso_term_elim(grammar)
    grammar.rules = longright_elim(grammar.variables, grammar.rules)  # long right side elimination
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
            tmpkey.update(char for char in eps_keys if char in v)  # get keys to remove from tmpkey
            tmprule.update(v.replace(char, "") for char in tmpkey for v in value if char in v)  # create rules by removing characters
        value.update(tmprule)

    for key, val in rules.items():  # replace empty sets with epsilon
        for v in val:
            if v == '':
                val.add(r'\E')
                val.remove('')
    for e in eps_keys:  # remove epsilon from all rules and add one to S
        rules[e].remove(r'\E')
    rules[start].add(r'\E')
    return rules


def rek_nrules(rule, var, nrule):  # nrule ist ein Set: keine Duplikate, ungeordnet
    x = rule.rindex(var)
    rule = rule[0:x - 1] + rule[x + 1:len(rule) - 1]
    nrule = nrule.append(rule)
    if var in rule:
        return rek_nrules(rule, var, nrule)

    return nrule


# def cyclus_elim(grammar):


# def chain_elim(grammar):
#   return grammar


# search rules for non-isolated terminal symbols (e.g. in the form of 'aa' or 'aA'...)


def noniso_term_elim(grammar):
    global ALPH
    ALPH -= set(grammar.variables)
    new_rules = {}

    for keys, values in grammar.rules.items():
        new_rules.update({keys: values})
        for term in grammar.alphabet:
            for val in values:
                if term in val:
                    if term is not val:
                        tmpval = val
                        if cyk.check_rule(grammar.rules, term):
                            tmpval = tmpval.replace(term, cyk.check_rule(grammar.rules, term).pop())
                            new_rules.get(keys).remove(val)
                            new_rules.get(keys).add(tmpval)

                        elif cyk.check_rule(new_rules, term):
                            tmpval = tmpval.replace(term, cyk.check_rule(new_rules, term).pop())
                            new_rules.get(keys).remove(val)
                            new_rules.get(keys).add(tmpval)

                        else:
                            new_key = ALPH.pop()
                            tmpval = tmpval.replace(term, new_key)
                            new_rules.get(keys).remove(val)
                            new_rules.get(keys).add(tmpval)
                            new_rules.update({new_key: set(term)})

# extract values and keys from dict and use lists?

    return new_rules


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
                new_key = ALPH.pop()  # generates new key while also preventing redundancy
                new_values = {val[-2:]}  # last two characters of val
                val1 = val[:-2] + new_key  # create new rule out of lhs part of val and new key
                tmpcpy.remove(val)  # remove old rule
                tmpcpy.add(val1)  # add updated rule
                new_rules.update({new_key: new_values})
        new_rules.update({key: set(tmpval)})
        if repeat:
            longright_elim(set(x for x in new_rules.keys()), new_rules)
    return new_rules
