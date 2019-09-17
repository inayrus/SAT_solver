# This is example input
dict = {111: False, -111: True, 112: '?', -112: '?', 113: '?', -113: '?', 114: True, -114: False, 115: False, -115: True, 122: True, -122: False}
clause_list = [[111, 112, 113], [-111, 115], [-111, 112, -114], [-111, 122]]
print(dict)


def dlcs(dict, clause_list):
    # Separate lists for positive and negative literals
    neg_clause_list = []
    pos_clause_list = []
    for clause in clause_list:
        for clause_var in clause:
            if clause_var < 0:
                neg_clause_list.append(clause_var * -1)
            else:
                pos_clause_list.append(clause_var)

    # Count occurrences of literals in list with only positives and only negatives. Afterwards, merge lists for CP+CN
    from collections import Counter
    count_pos = Counter(pos_clause_list)
    count_neg = Counter(neg_clause_list)
    merged_counts = count_pos + count_neg

    # Sort lists based on most frequent occurrences
    most_common_pos = count_pos.most_common()
    most_common_neg = count_neg.most_common()
    most_common_merge = merged_counts.most_common()

    # Find highest CP+CN that is still unknown
    var_to_change = '?'
    idx = 0
    while var_to_change == '?':
        if dict[most_common_merge[idx][0]] is '?':
            var_to_change = most_common_merge[idx][0]
        else:
            idx += 1

    # Calculate CP and CN
    cp = 0
    cn = 0
    for list_i in most_common_pos:
        if var_to_change in list_i:
            idx = most_common_pos.index(list_i)
            cp = most_common_pos[idx][1]
    for list_i in most_common_neg:
        if var_to_change in list_i:
            idx = most_common_neg.index(list_i)
            cn = most_common_neg[idx][1]

    # Reassign truth value in dict based on whether CP or CN is bigger
    if cp > cn:
        dict[var_to_change] = True
        dict[(var_to_change * -1)] = False
    else:
        dict[var_to_change] = False
        dict[(var_to_change * -1)] = True

    # Return updated dict
    return dict

