import string
from sortedcontainers import SortedSet
import CnfTest
import cyk

ALPH = SortedSet(string.ascii_uppercase)


def cnf(grammar):
    grammar.rules = epsilon_elim(grammar.start, grammar.rules)  # epsilon elimination
    # grammar.rules = chain_elim(grammar.rules)
    CnfTest.print_grammar(grammar.rules)
    grammar.rules = noniso_term_elim(grammar)
    CnfTest.print_grammar(grammar.rules)
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
            tmprule.update(v.replace(char, "") for char in tmpkey for v in value if
                           char in v)  # create rules by removing characters
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


def chain_elim(grammar):
    keys = [key for key in grammar.keys()]
    new_dict = {}
    for key in list(reversed(keys)):
        new_dict.update({key: grammar[key]})
        newkeys = cyk.check_rule(grammar, key)
        for k in newkeys:
            grammar[k].update(grammar[key])
            grammar[k].remove(key)
    return new_dict


# search rules for non-isolated terminal symbols (e.g. in the form of 'aa' or 'aA'...)
def noniso_term_elim(grammar):
    global ALPH
    ALPH -= set(grammar.variables)
    newdict = dict()
    for keys, values in grammar.rules.items():  # iterate over dict
        tmpval = values  # save temporary copy of values
        for val in tmpval:  # iterate over set of strings
            tmpstr = val  # save temporary copy of string

            map_term_notterm = [(char, ALPH.pop()) for char in val if char in grammar.alphabet]
            for char in val:
                for tup in map_term_notterm:
                    if char in tup:
                        if not cyk.check_rule(grammar.rules, char):
                            if not len(cyk.check_rule(newdict, char)) == 1:
                                tmpstr = tmpstr.replace(char, tup[1])  # replace terminal with nonterminal symbol
                                newdict[tup[1]] = set(char)
                            else :
                                tmpstr = tmpstr.replace(char, cyk.check_rule(newdict, char)[0])
                                newdict[cyk.check_rule(newdict, char)[0]] = set(char)

                        else:
                            tmpstr = tmpstr.replace(char, cyk.check_rule(grammar.rules, char)[0])
            tmpval.remove(val)
            tmpval.add(tmpstr)
        newdict[keys] = tmpval
        #CnfTest.print_grammar(newdict)
    return newdict


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
