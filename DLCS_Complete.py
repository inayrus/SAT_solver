"""
File with a function to run the second heuristic in SAT.py: DLCS.

by Sanne van den Berg and Valerie Sawirja
"""
from collections import Counter
import random


def dlcs(dict, clause_list):
    """
    Function that picks one of the most frequent literals in the active clauses.
    Tries the truth value first that corresponds with most frequent polarity of
    the chosen literal.
    Returns a literal and a list with truth values.
    """
    # Separate lists for positive and negative literals
    neg_clause_list = []
    pos_clause_list = []
    no_neg_clause_list = []
    for clause in clause_list:
        for clause_var in clause:
            abs_literal = abs(clause_var)
            if dict[abs_literal] == '?' and abs_literal not in no_neg_clause_list:
                no_neg_clause_list.append(abs_literal)
                if clause_var < 0:
                    neg_clause_list.append(abs_literal)
                else:
                    pos_clause_list.append(abs_literal)

    # Count occurrences of literals
    count_total = Counter(no_neg_clause_list)

    # Sort lists based on most frequent occurrences
    most_common_tot = count_total.most_common()

    # Highest value
    highest_values = []
    highest_value = most_common_tot[0][1]
    idx = 0

    # create a list of literals that appear most often
    while most_common_tot[idx][1] == highest_value and idx <= (len(most_common_tot) - 1):
        highest_values.append(most_common_tot[idx][0])
        idx += 1
        if idx > len(most_common_tot) - 1:
            break

    # randomly choose one of the most common literals
    var_to_change = random.choice(highest_values)

    cp = pos_clause_list.count(var_to_change)
    cn = neg_clause_list.count(var_to_change)

    # try truth value 1 if chosen literal is more often positive than negative
    if cp > cn:
        return abs(var_to_change), [0, 1]

    # try value 0 first
    else:
        return abs(var_to_change), [1, 0]
