"""alternative cnf functions in case the alphabet runs out of symbols"""
import string


def non_iso_term_elim_alternative(rules, variables, alphabet):
    """alternative version of elimination of non isolated terminal symbols"""
    alph = set(string.ascii_uppercase) - set(variables)
    length_difference = len(alphabet) - len(alph)
    alternate_alph = set(string.ascii_uppercase)
    needed_symbols = [alternate_alph.pop() for _ in range(int(length_difference / 10) + 1)]
    new_dict = dict()
    for symbol in needed_symbols:
        for diff in range(length_difference):
            alph.add(symbol + str(diff))
    map_term_not_term = [(char, symbol) for char, symbol
                         in zip(alphabet, alph)]
    for keys, values in rules.items():
        new_dict[keys] = set()
        tmp_val = values.copy()
        for val in tmp_val:
            tmp_str = val
            for term_symbol in map_term_not_term:
                if term_symbol[0] in tmp_str and len(tmp_str) > 1:
                    tmp_str = tmp_str.replace(term_symbol[0], term_symbol[1])
                    new_dict[term_symbol[1]] = set(term_symbol[0])
            tmp_val.remove(val)
            tmp_val.add(tmp_str)

        new_dict[keys].update(tmp_val)
    repeat = False
    for value in new_dict.values():  # make sure it worked, reiterate if needed
        for strings in value:
            if len(strings) > 1:
                for term in alphabet:
                    if term in strings:
                        repeat = True
    if repeat:
        return non_iso_term_elim_alternative(new_dict,
                                             (key for key, values in new_dict.items()),
                                             alphabet)
    return new_dict, True


def long_right_alternative(rules):
    """alternative method of eliminating long right sided rules"""
    alternate_keys = [list(key)[0] for key in rules.keys() if len(key) > 1]
    alph = set(string.ascii_uppercase) - set(alternate_keys)
    new_dict = dict()
    am_new_keys = 0
    new_key = alph.pop()+str(am_new_keys)
    for key, values in rules.items():
        tmp_val = values.copy()
        new_dict[key] = tmp_val
        for strings in values:
            amount_integers = len([num for num in [char for char in strings]
                                   if num not in string.ascii_uppercase])
            if len(strings) - amount_integers > 2:
                tmp_str = strings
                count = 0
                new_val = ""
                for char in reversed(tmp_str):
                    if count == 2:
                        break
                    if char not in string.ascii_uppercase:
                        new_val = char + new_val
                        continue
                    new_val = char + new_val
                    count += 1
                am_new_keys += 1
                if am_new_keys > 9:
                    new_key = alph.pop()
                    am_new_keys = 0
                if len(new_key) > 1:
                    new_key = ''.join(list(new_key)[:-1]) + str(am_new_keys)
                tmp_str = tmp_str[:-len(new_val)] + new_key
                new_dict[key].remove(strings)
                new_dict[key].add(tmp_str)
                new_dict[new_key] = set()
                new_dict[new_key].add(new_val)
    repeat = False
    for key, values in new_dict.items():
        for strings in values:
            amount_integers = len([num for num in
                                   [char for char in strings]
                                   if num not in string.ascii_uppercase])
            if len(strings) - amount_integers > 2:
                repeat = True
    if repeat:
        return long_right_alternative(new_dict)
    return new_dict
