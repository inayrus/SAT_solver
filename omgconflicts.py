

def CDCL(conflict_lit, start_obj, current_state):
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
        current_state.weights[literal] += 1

    # decay all weights with decay_factor
    for keys in current_state.weights:
        current_state.weights[keys] *= decay_factor


    # backtrack to correct state
    #back_to_level = 0
    i = 0
    while i < len(current_state.choice_tree):
        for conflicting in conflict_list:
            if abs(conflicting) in current_state.choice_tree[i][2]:
                back_to_level = i
        i += 1
        #for choice_i, choice in enumerate(reversed(current_state.choice_tree)):
            # for conflicting in conflict_list:
            #     if abs(conflicting) in choice[2]:
            #         back_to_level = choice_i
            #         break

    print('check level', back_to_level)

    # return stuff
    return current_state
