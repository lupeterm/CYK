"""functions to bring grammar into CNF"""
import string
import cnf_test
import cyk


def cnf(grammar):
    """sequentially call distinct functions"""
    grammar.rules = epsilon_elim(grammar.start, grammar.rules)
    print("Occurrences of epsilon eliminated.")
    cnf_test.print_grammar(grammar.rules)
    grammar.rules = chain_elim(grammar.rules)
    print("Occurrences of chained rules eliminated.")
    cnf_test.print_grammar(grammar.rules)
    grammar.rules = non_iso_term_elim(grammar.rules, grammar.variables, grammar.alphabet)
    print("Occurrences of non isolated terminal symbols eliminated.")
    cnf_test.print_grammar(grammar.rules)
    grammar.rules = long_right_elim(grammar.rules)
    print("Occurrences of long right sides eliminated.")
    cnf_test.print_grammar(grammar.rules)
    return grammar.rules


def epsilon_elim(start, rules):
    """eliminate epsilon"""
    eps = r'\E'
    eps_keys = cyk.check_rule(rules, eps)  # find occurrences of epsilon in rules
    if not eps_keys:
        return rules
    for key, value in rules.items():
        tmpkey = set()
        tmprule = set()
        for val in value:
            # get keys to remove from tmpkey
            tmpkey.update(char for char in eps_keys if char in val)
            tmprule.update(val.replace(char, "") for char in tmpkey for val in value if
                           char in val)  # create rules by removing characters
        value.update(tmprule)
    for key, values in rules.items():  # replace empty sets with epsilon
        tmpval = values.copy()
        for word in values:
            if not word:
                tmpval.add(eps)
                tmpval.remove('')
        rules[key] = tmpval
    for key in eps_keys:
        rules[key].remove(r'\E')
    eps_keys = cyk.check_rule(rules, eps)
    if len(eps_keys) > 1 or not (len(eps_keys) == 1 and start in eps_keys):
        return epsilon_elim(start, rules)

    return rules


def chain_elim(rules):
    """eliminate chained rules"""
    keys = []
    for key in rules.keys():
        keys.append(key)
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
    """eliminate non isolated terminal symbols"""
    alph = set(string.ascii_uppercase) - set(variables)
    new_dict = dict()
    map_term_not_term = [(char, symbol) for char, symbol
                         in zip(alphabet, alph)]
    for keys, values in rules.items():
        new_dict[keys] = set()
        tmpval = values.copy()  # save temporary copy of values
        for val in tmpval:  # iterate over set of strings
            tmp_str = val
            # substitute new variable with every occurrence of terminal symbol..
            for term in map_term_not_term:
                # if the terminal symbol is not isolated
                if term[0] in tmp_str and len(tmp_str) > 1:
                    tmp_str = tmp_str.replace(term[0], term[1])
                    new_dict[term[1]] = set(term[0])
            tmpval.remove(val)
            tmpval.add(tmp_str)

        new_dict[keys].update(tmpval)
    for value in new_dict.values():  # make sure it worked, reiterate if needed
        for strings in value:
            if len(strings) > 1:
                for term in alphabet:
                    if term in strings:
                        non_iso_term_elim(new_dict,
                                          (key for key, values in new_dict.items()),
                                          alphabet)
    return new_dict


def long_right_elim(rules):
    """eliminate long right sides"""
    alph = set(string.ascii_uppercase) - set(key for key in rules)
    new_dict = {}
    for key, values in rules.items():
        tmp_val = values.copy()
        new_dict[key] = tmp_val
        for strings in values:
            length = len(strings)
            if length > 2:
                tmp_str = strings
                new_val = tmp_str[-2:]  # ABC -> A BC (split last two vars)
                new_key = alph.pop()  # new variable X
                tmp_str = tmp_str[:-2] + new_key  # updated rule AX
                new_dict[key].remove(strings)
                new_dict[key].add(tmp_str)
                new_dict[new_key] = set()
                new_dict[new_key].add(new_val)  # new rule: X -> BC
    repeat = False
    for key, values in rules.items():  # not pretty i know. if needed, reiterate
        for strings in values:
            if len(strings) > 2:
                repeat = True
    if repeat:
        return long_right_elim(new_dict)
    return new_dict
