from collections import Counter


def CDCL(conflict_lit, start_obj, current_state, variable_weights):
    """
    A function that:
    1) creates a conflict clause
    2) adds the clause to the list of remaining propositional clauses
    3) updates the weights of all literals
    4) determines how much should be backtracked
    """
    # decay factor 0.95. Decays after every conflict
    decay_factor = 0.95

    # 1)
    conflict_list = []

    # select all literals in which conflict lit appears
    for clause in start_obj.clauses:
        if conflict_lit in clause or -conflict_lit in clause:
            for literal in clause:
                if literal != conflict_lit and literal != -conflict_lit:
                    conflict_list.append(abs(literal))

    # return list with removed double literals
    conflict_list = list(set(conflict_list))

    # 2)
    # add conflict clause to current state
    current_state.clauses.insert(0, conflict_list)

    # 3)
    # update weights. bump weights for conflict contributing literals
    no_negconflicts = list(set([abs(literal) for literal in conflict_list]))
    for literal in no_negconflicts:
        variable_weights[literal] += 1

    # decay all weights with decay_factor
    for literal in current_state.weights:
        variable_weights[literal] *= decay_factor

    # 4)
    back_to_literal = None
    cut_tree = current_state.choice_tree[1::]

    # backtrack to last split where a literal from conflict clause appears
    for c_state in reversed(cut_tree):
        c_index = current_state.choice_tree.index(c_state)
        variable_tree = current_state.choice_tree[c_index][0]
        dependencies_tree = current_state.choice_tree[c_index][2]

        # check split variable and its dependents for conflict clause literal
        for conflicting in conflict_list:
            if (-conflicting == variable_tree) or (-conflicting in dependencies_tree) or \
            conflicting == variable_tree or conflicting in dependencies_tree:
                back_to_level = c_index
                back_to_literal = current_state.choice_tree[back_to_level][0]

                return current_state, variable_weights, back_to_literal

    return current_state, variable_weights, back_to_literal

def vsids(current_state, variable_weights):
    # weights list
    heaviest_weights = Counter(variable_weights).most_common()

    # get literals that are unassigned
    unassigned = current_state.get_unassigned()

    # choose the unassigned literal with the heaviest weight
    for weight in heaviest_weights:
        if weight[0] in unassigned:
            chosen_literal = weight[0]
            return chosen_literal
