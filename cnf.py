"""functions to bring grammar into CNF"""
import string
import cnf_test
import cyk
import cnf_alternative


def cnf(grammar):
    """sequentially call distinct functions"""
    grammar.rules = epsilon_elim(grammar.start, grammar.rules)
    print("Occurrences of epsilon eliminated.")
    cnf_test.print_grammar(grammar.rules)
    grammar.rules = chain_elim(grammar.rules)
    print("Occurrences of chained rules eliminated.")
    cnf_test.print_grammar(grammar.rules)
    grammar_alternative = non_iso_term_elim(grammar.rules, grammar.variables, grammar.alphabet)
    print("Occurrences of non isolated terminal symbols eliminated.")
    cnf_test.print_grammar(grammar_alternative[0])
    if grammar_alternative[1]:
        grammar_alternative = cnf_alternative.long_right_alternative(grammar_alternative[0])
        print("Occurrences of long right sides eliminated.")
        return grammar_alternative
    grammar.rules = long_right_elim(grammar_alternative[0], grammar.alphabet)
    print("Occurrences of long right sides eliminated.")
    cnf_test.print_grammar(grammar.rules)
    return grammar.rules


def epsilon_elim(start, rules):
    """eliminate epsilon"""
    eps = r'\E'
    eps_keys = cyk.check_rule(rules, eps)  # find occurrences of epsilon in rules
    if not eps_keys:
        return rules
    for key, set_of_strings in rules.items():
        updated_set = set()
        for strings in set_of_strings:
            # get keys to remove from tmp_key
            keys_to_remove = set(char for char in eps_keys if char in strings)
            updated_set.update(strings.replace(key, "")
                               for key in keys_to_remove
                               for strings in set_of_strings if key in strings)
            set_of_strings.update(updated_set)
    for key, set_of_strings in rules.items():  # replace empty sets with epsilon
        empty_string_to_epsilon = set_of_strings.copy()
        for strings in set_of_strings:
            if not strings:
                empty_string_to_epsilon.add(eps)
                empty_string_to_epsilon.remove('')
        rules[key] = empty_string_to_epsilon
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
    for key in keys:
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
    if len(alphabet) > len(alph):
        return cnf_alternative.non_iso_term_elim_alternative(rules, variables, alphabet)
    map_term_not_term = []
    for char, symbol in zip(alphabet, alph):
        map_term_not_term.append((char, symbol))
    for keys, set_of_strings in rules.items():
        string_set = set_of_strings.copy()  # save temporary copy of values
        for strings in string_set:  # iterate over set of strings
            updated_char = strings
            # substitute new variable with every occurrence of terminal symbol..
            for alphabet_symbols in map_term_not_term:
                # if the terminal symbol is not isolated
                if alphabet_symbols[0] in updated_char and len(updated_char) > 1:
                    updated_char = updated_char.replace(alphabet_symbols[0], alphabet_symbols[1])
                    new_dict[alphabet_symbols[1]] = set(alphabet_symbols[0])
            string_set.remove(strings)
            string_set.add(updated_char)
        new_dict.update({keys: string_set})
    for set_of_strings in new_dict.values():  # make sure it worked, reiterate if needed
        for strings in set_of_strings:
            if len(strings) > 1:
                for chars in alphabet:
                    if chars in strings:
                        non_iso_term_elim(new_dict, new_dict.keys(), alphabet)
    return new_dict, False


def long_right_elim(rules, alphabet):
    """eliminate long right sides"""
    alph = set(string.ascii_uppercase) - set(key for key in rules)
    if len(alphabet) > len(alph):
        return cnf_alternative.long_right_alternative(rules)
    new_dict = dict()
    for key, sets_of_strings in rules.items():
        new_dict[key] = sets_of_strings.copy()
        for strings in sets_of_strings:
            if len(strings) > 2:
                new_values = strings
                new_value = new_values[-2:]  # ABC -> A BC (split last two vars)
                new_key = alph.pop()  # new variable X
                new_values = new_values[:-2] + new_key  # updated rule AX
                new_dict[key].remove(strings)
                new_dict[key].add(new_values)
                new_dict[new_key] = set(new_value)  # new rule: X -> BC
    for key, sets_of_strings in new_dict.items():  # if needed, reiterate
        for strings in sets_of_strings:
            if len(strings) > 2:
                return long_right_elim(new_dict, alphabet)
    return new_dict
