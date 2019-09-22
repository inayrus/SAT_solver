# This is example input
dict = {111: False, -111: True, 112: '?', -112: '?', 113: '?', -113: '?', 114: True, -114: False, 115: False, -115: True, 122: True, -122: False}
clause_list = [[111, 112, 113], [-111, 113, 115], [-111, 112, -114], [-111, 122]]
# print(dict)


def dlcs(dict, clause_list):
    # Separate lists for positive and negative literals
    neg_clause_list = []
    pos_clause_list = []
    no_neg_clause_list = []
    for clause in clause_list:
        for clause_var in clause:
            if clause_var < 0 and dict[abs(clause_var)] == '?':
                no_neg_clause_list.append(clause_var * -1)
                neg_clause_list.append(clause_var * -1)
            elif clause_var >= 0 and dict[abs(clause_var)] == '?':
                no_neg_clause_list.append(clause_var * 1)
                pos_clause_list.append(clause_var)

    # Count occurrences of literals in list with only positives and only negatives. Afterwards, merge lists for CP+CN
    from collections import Counter
    count_total = Counter(no_neg_clause_list)

    # Sort lists based on most frequent occurrences
    most_common_tot = count_total.most_common()

    # Highest value
    highest_values = []
    highest_value = most_common_tot[0][1]
    idx = 0
    while most_common_tot[idx][1] == highest_value and idx <= (len(most_common_tot) - 1):
        highest_values.append(most_common_tot[idx][0])
        idx += 1
        if idx > len(most_common_tot) - 1:
            break

    import random
    var_to_change = random.choice(highest_values)

    cp = pos_clause_list.count(var_to_change)
    cn = neg_clause_list.count(var_to_change)

    if cp > cn:
        # dict[var_to_change] = 1
        #dict[(var_to_change * -1)] = False
        return var_to_change, [1, 0]

    # try value 0 first
    else:
        # dict[var_to_change] = 0
        #dict[(var_to_change * -1)] = True
        return var_to_change, [1, 0]

    # Return updated dict
    # return dict

