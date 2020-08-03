import string
import cnfTest
import cyk


def cnf(grammar):
    grammar.rules = epsilon_elim(grammar.start, grammar.rules)
    cnfTest.print_grammar(grammar.rules)
    grammar.rules = chain_elim(grammar.rules)
    cnfTest.print_grammar(grammar.rules)
    grammar.rules = non_iso_term_elim(grammar.rules, grammar.variables, grammar.alphabet)
    cnfTest.print_grammar(grammar.rules)
    grammar.rules = long_right_elim(grammar.rules)
    cnfTest.print_grammar(grammar.rules)
    return grammar.rules


def epsilon_elim(start, rules):
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

    for key, values in rules.items():  # replace empty sets with epsilon
        for string in values:
            if not string:
                values.add(eps)
                values.remove('')
    for e in eps_keys:  # remove epsilon from all rules and add one to S
        rules[e].remove(r'\E')
    eps_keys = cyk.check_rule(rules, eps)
    if len(eps_keys) > 1 or not (len(eps_keys) == 1 and start in eps_keys):  # reiterate if new eps rules were created
        return epsilon_elim(start, rules)
    else:
        return rules


def chain_elim(rules):
    keys = [key for key in rules.keys()]
    new_dict = {}
    for key in list(keys):
        new_dict.update({key: rules[key]})
        new_keys = cyk.check_rule(rules, key)  # get vars that point to singular variables
        for k in new_keys:  # substitute rules of V on rhs with V itself
            rules[k].update(rules[key])
            rules[k].remove(key)
    return new_dict


# search rules for non-isolated terminal symbols (e.g. in the form of 'aa' or 'aA'...)
def non_iso_term_elim(rules, variables, alphabet):
    ALPH = set(string.ascii_uppercase) - set(variables)
    new_dict = dict()
    map_term_not_term = [(char, symbol) for char, symbol in zip(alphabet, ALPH)]  # map term symbols to a new variable
    for keys, values in rules.items():
        new_dict[keys] = set()
        tmpval = values.copy()  # save temporary copy of values
        for s in tmpval:  # iterate over set of strings
            tmp_str = s
            for t in map_term_not_term:  # substitute new variable with every occurrence of terminal symbol..
                if t[0] in tmp_str and len(tmp_str) > 1: # if the terminal symbol is not isolated
                    tmp_str = tmp_str.replace(t[0], t[1])
                    new_dict[t[1]] = set(t[0])
            tmpval.remove(s)
            tmpval.add(tmp_str)

        new_dict[keys].update(tmpval)
    for key, value in new_dict.items():  # make sure it worked, reiterate if needed
        for strings in value:
            if len(strings) > 1:
                for term in alphabet:
                    if term in strings:
                        non_iso_term_elim(new_dict, (key for key, values in new_dict.items()), alphabet)
    return new_dict


def long_right_elim(rules):
    ALPH = set(string.ascii_uppercase) - set(key for key in rules)
    new_dict = {}
    for key, values in rules.items():
        tmp_val = values.copy()
        new_dict[key] = tmp_val
        for strings in values:
            length = len(strings)
            if length > 2:
                tmp_str = strings
                new_val = tmp_str[-2:]  # ABC -> A BC (split last two vars)
                new_key = ALPH.pop()       # new variable X
                tmp_str = tmp_str[:-2] + new_key  # updated rule AX
                new_dict[key].remove(strings)
                new_dict[key].add(tmp_str)
                new_dict[new_key] = set()
                new_dict[new_key].add(new_val)  # new rule: X -> BC
    repeat = False
    for key, values in rules.items(): # not pretty i know. if needed, reiterate
        for strings in values:
            if len(strings) > 2:
                repeat = True
    if repeat:
        return long_right_elim(new_dict)
    else:
        return new_dict
