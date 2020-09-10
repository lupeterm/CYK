"""alternative cnf functions in case the alphabet runs out of symbols"""
import string


def non_iso_term_elim_alternative(rules, variables, alphabet):
    """alternative version of elimination of non isolated terminal symbols"""
    alph = set(string.ascii_uppercase) - set(variables)
    length_difference = len(alphabet) - len(alph)
    needed_symbols = [set(string.ascii_uppercase).pop() for _ in range(int(length_difference / 10) + 1)]
    new_dict = dict()
    for symbol in needed_symbols:
        for diff in range(length_difference):
            alph.add(symbol + str(diff))
    map_term_not_term = [(char, symbol) for char, symbol
                         in zip(alphabet, alph)]
    for keys, sets_of_strings in rules.items():
        string_set = sets_of_strings.copy()
        for strings in string_set:
            string_update = strings
            for term_symbol in map_term_not_term:
                if term_symbol[0] in string_update and len(string_update) > 1:
                    string_update = string_update.replace(term_symbol[0], term_symbol[1])
                    new_dict[term_symbol[1]] = set(term_symbol[0])
            string_set.remove(strings)
            string_set.add(string_update)

        new_dict[keys] = string_set
    for set_of_strings in new_dict.values():  # TODO: make it work without iterating twice
        for string_set in set_of_strings:
            if len(string_set) > 1:
                for term in alphabet:
                    if term in string_set:
                        return non_iso_term_elim_alternative(new_dict, new_dict.keys(), alphabet)
    return new_dict, True


def long_right_alternative(rules):
    """alternative method of eliminating long right sided rules"""
    alternate_keys = [list(key)[0] for key in rules.keys() if len(key) > 1]
    alph = set(string.ascii_uppercase) - set(alternate_keys)
    new_dict = dict()
    am_new_keys = 0
    new_key = alph.pop() + str(am_new_keys)
    for key, sets_of_strings in rules.items():
        string_set = sets_of_strings.copy()
        new_dict[key] = string_set
        for old_value in sets_of_strings:
            amount_integers = len([num for num in [char for char in old_value]
                                   if num not in string.ascii_uppercase])
            if len(old_value) - amount_integers > 2:
                updated_value = old_value
                count = 0
                new_value = ""
                for char in reversed(updated_value):
                    if count == 2:
                        break
                    if char not in string.ascii_uppercase:
                        new_value = char + new_value
                        continue
                    new_value = char + new_value
                    count += 1
                am_new_keys += 1
                if am_new_keys > 9:
                    new_key = alph.pop()
                    am_new_keys = 0
                if len(new_key) > 1:
                    new_key = ''.join(list(new_key)[:-1]) + str(am_new_keys)
                updated_value = updated_value[:-len(new_value)] + new_key
                new_dict[key].remove(old_value)
                new_dict[key].add(updated_value)
                new_dict[new_key] = set(new_value)
    for key, sets_of_strings in new_dict.items():
        for strings in sets_of_strings:
            amount_integers = len([num for num in
                                   [char for char in strings]
                                   if num not in string.ascii_uppercase])
            if len(strings) - amount_integers > 2:
                return long_right_alternative(new_dict)
    return new_dict
