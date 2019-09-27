from collections import Counter

def CDCL(conflict_lit, start_obj, current_state, variable_weights):
    # fix rest of weights --> decay factor 0.95. Decays after every conflict
    decay_factor = 0.95
    conflict_list = []

    # select all literals in which conlf lit appears
    for clause in start_obj.clauses:
        if conflict_lit in clause or -conflict_lit in clause:
            for literal in clause:
                if literal != conflict_lit:
                    conflict_list.append(literal)

    # to remove double literals
    conflict_list = list(set(conflict_list))
    print('conflict lsit', conflict_list)
    current_state.clauses.append(conflict_list)

    # # UPDATE WEIGHTS
    # update weights. bump weights for conflict contributing literals
    no_negconflicts = list(set([abs(literal) for literal in conflict_list]))
    for literal in no_negconflicts:
        variable_weights[literal] += 1

    # decay all weights with decay_factor
    for literal in current_state.weights:
        variable_weights[literal] *= decay_factor

    heaviest_weights = Counter(variable_weights).most_common()
    print('current state weights', current_state.weights)
    print('heaviest_weights', heaviest_weights)
    print('heaviest', heaviest_weights[0][0])
    print('heaviest', heaviest_weights[1][1])

    # backtrack to correct state
    # back_to_level = 0
    # i = len(current_state.choice_tree) -1
    # while i > 0:
    #     for conflicting in conflict_list:
    #         if abs(conflicting) in current_state.choice_tree[i][2]:
    #             back_to_level = i
    #             #print('back', back_to_level)
    #     i -= 1

    back_to_level = 0
    for c_state in reversed(current_state.choice_tree):
        c_index = current_state.choice_tree.index(c_state)
        print('len choice tree', len(current_state.choice_tree))
        print('c index', c_index)
        for conflicting in conflict_list:
            if ((abs(conflicting) == current_state.choice_tree[c_index][0]) or (abs(conflicting) in current_state.choice_tree[c_index][2]) or (conflicting == current_state.choice_tree[c_index][0]) or (conflicting in current_state.choice_tree[c_index][2])) and not current_state.choice_tree[len(current_state.choice_tree) -1]:
                back_to_level = c_index

    print('back to level', back_to_level)


    # back_to_level -= 2

    #currrent_state.choice_tree(back_to_level)

    # print('len choice', len(current_state.choice_tree))
    # print('back', back_to_level)
    # print("btl literal", current_state.choice_tree[back_to_level][0])
    # print("btl value", current_state.choice_tree[back_to_level][1])
    #current_state(back_to_level)

        # for choice_i, choice in enumerate(reversed(current_state.choice_tree)):
        #     for conflicting in conflict_list:
        #         if abs(conflicting) in choice[2]:
        #             back_to_level = choice_i
        #             break

    # return stuff
    return current_state, variable_weights, back_to_level, current_state.choice_tree[back_to_level][0]
