from Puzzle_State import Puzzle_State
from DLCS_Complete import dlcs
from omgconflicts import CDCL
import sys
import random
import copy
import pathlib
from collections import Counter


def iterative_dpll(subdirname, heuristic, inputfile):
    """
    SAT algorithm that loops iteratively though the search space
    """

    # h
    #heuristic = input('Enter heur: ')
    # initialize puzzle start state and stack
    start_state = Puzzle_State(inputfile)
    variable_weights = dict.fromkeys(start_state.values, 0)
    stack = []
    previous_split = []
    N_backtracks = 0
    times_run = 0

    # remove tautologies
    remove_tautologies(start_state)

    # put A COPY OF the start states on the stack (chosen start var & True and False)
    first_state = copy.deepcopy(start_state)
    stack.append(first_state)

    # start while loop (while stack not empty)
    while stack:
        times_run += 1
        print("states in stack: ", len(stack))
        # loop starts without conflict
        conflict = False
        conflict_lit = None

        # pop the last from the stack
        current_state = stack.pop()

        # do unit propagation:
        unit_count = 1
        found_units = set()
        while not conflict and unit_count > 0:
            unit_count = 0
            for clause in current_state.clauses:
                # if clause is length one:
                if len(clause) == 1:
                    unit_count += 1
                    literal = clause[0]
                    found_units.add(literal)
                    # check dict if it has a value that makes this clause False:
                    if current_state.get_truth(literal) == 0:
                        # if yes --> conflict
                        conflict = True
                    else:
                        # set clauses of length 1 on true,
                        current_state.set_truth(literal, 1)
                        # update the clauses
                        conflict_lit, conflict = current_state.update_clauses(literal)
                # stop for loop if conflict
                if conflict:
                    N_backtracks += 1
                    break

            print("unit count:", unit_count)

        # calculate clause to variable rate
        if times_run == 1:
            clause_var = len(current_state.clauses)/81
            print('clause', clause_var)

        # add all found units of unit propagation to the dependency of choice tree
        current_state.choice_tree[-1][-1] = list(found_units)

        # only do the below if there is NO conflict and there are unsolved clauses left (aka not [], when all clauses are removed)
        if not conflict and len(current_state.clauses) != 0:

            #split variables
            if heuristic == 1:
                chosen_literal = random_choice(current_state)
                truth_assignments = [0, 1]
            elif heuristic == 2:
                chosen_literal, truth_assignments = dlcs(current_state.values, current_state.clauses)
            elif heuristic == 3:
                # weights list
                heaviest_weights = Counter(variable_weights).most_common()

                # get literals that are unassigned
                unassigned = get_unassigned(current_state)

                # choose the unassigned literal with the heaviest weight
                for weight in heaviest_weights:
                    if weight[0] in unassigned:
                        chosen_literal = weight[0]
                        break

                truth_assignments = [0,1]

                # print('heavy shit', len(heaviest_weights))
                # if heaviest_weights[0][1] == 0 and heaviest_weights[0][0] not in previous_split and get_truth(heaviest_weights[0][1] == False):
                #     chosen_literal = random_choice(current_state)
                # elif heaviest_weights[0][0] in previous_split:
                #     chosen_literal = heaviest_weights[len(previous_split)][0]
                # else:
                #     chosen_literal = heaviest_weights[0][0]
                # previous_split.append(chosen_literal)
                # truth_assignments = [0,1]
                # print('prev', len(previous_split))

            else:
                chosen_literal = current_state.clauses[0][0]
                truth_assignments = [1, 0]
                # quit()

            print("split literal", chosen_literal)

            # if there's a chosen literal (not everything is assigned yet)
            if chosen_literal:
                # make children (all possibilities for the new variable)
                for truth in truth_assignments:
                    child = copy.deepcopy(current_state)
                    # 1) add chosen var to choice tree
                    child.choice_tree.append([chosen_literal, truth, list()])
                    # 2) change value in dictionary
                    child.set_truth(chosen_literal, truth)
                    # 3) update clauses with new truth assignment
                    child.update_clauses(chosen_literal)

                    # add child to stack
                    stack.append(child)

        if heuristic == 3 and conflict_lit:
            current_state, variable_weights, back_to_level = CDCL(conflict_lit, start_state, current_state, variable_weights)
            print("ye")

            #### non chrono backtrack
            # went to level 0 --> unsat
            if back_to_level == 0:
                stack = []

            else:
                bak_to_literal = current_state.choice_tree[back_to_level][0]
                for state in reversed(stack):
                    if state.choice_tree[-1][0] == bak_to_literal:
                        i = stack.index(state)
                        new_stack = stack[0:i+1]
                        stack = new_stack
                        print(state)


        # no clauses left: SAT, found a solution!
        if len(current_state.clauses) == 0:
            print("SAT. solution saved in {}.out".format(get_extensionless(inputfile)))
            # call write output on the instance.values dict
            write_output(subdirname, inputfile, current_state, heuristic)
            print('N back', N_backtracks)
            #exit(0)
            return

        # else, conflict. let the loop backtrack

    # broke out of while loop: UNSAT. write output with START puzzle state
    print("UNSAT. solution saved in {}.out".format(get_extensionless(inputfile)))
    write_output(subdirname, inputfile, start_state, heuristic)
    print('N back', N_backtracks)
    #exit(0)
    return

def remove_tautologies(puzzle_obj):
    """
    removes tautologies from the list of clauses
    (ex. -111 and 111 in the same clause)
    """
    tautologies = []
    for index, clause in enumerate(puzzle_obj.clauses):
        for literal in clause:
            positive = 0 + abs(literal)
            negative = 0 - abs(literal)
            if positive in clause and negative in clause:
                tautologies.append(index)
                break

    # delete the tautologies from last to first (keeps right order)
    for index in reversed(tautologies):
        del puzzle_obj.clauses[index]

def random_choice(puzzle_obj):
    """
    Returns a random choice from unassigned literals
    Returns None if all literals are assigned
    """
    unassigned = get_unassigned(puzzle_obj)
    if unassigned:
        return random.choice(unassigned)
    else:
        return None

def get_unassigned(puzzle_obj):
    """returns a list with unassigned variables"""
    unassigned = [key for (key, value) in puzzle_obj.values.items() if value == '?']
    return unassigned

def write_output(subdirname, file, puzzle_obj, heuristic):
        """
        Takes a dictionary with values and their truth assignment and writes it
        to a file in DIMACS notation.
        """
        # check if inputfile has the .txt extension, if yes, remove it
        filename = get_extensionless(file)

        # get a list with all literals that are True
        true_literals = filter_true_literals(puzzle_obj)
        n_true_lits = len(true_literals)

        # check if filename.out already exists

        filepath = pathlib.Path(filename + '-' + str(subdirname) + '-' + str(heuristic) + '.out')

        # write to 'filename.out'
        with filepath.open(mode='w') as writer:
            # comment
            writer.write("c Literals with value True based on clauses in {}\n".format(filename))

            # p cnf nvar nclauses
            writer.write("p cnf {} {}\n".format(n_true_lits, n_true_lits))

            # write the literals
            for var in true_literals:
                writer.write("{} 0\n".format(str(var)))

def get_extensionless(filename):
    """returns the filename without extension"""
    if ".txt" in filename:
        filename = filename.split(".")[0]
    if "/" in filename:
        filename = filename.split("/")[-1]

    return filename

def filter_true_literals(puzzle_obj):
        """
        takes self.values,
        returns the variables that have truth assignment '1' in a list
        """
        true_literals = list()

        for var in puzzle_obj.values:
            if puzzle_obj.values[abs(var)] == 1 and var > 0:
                true_literals.append(var)
        return true_literals


if __name__ == "__main__":
    # read the commandline args ("SAT -Sn inputfile")

    # ensure correct usage
    if len(sys.argv) != 3:
        print("usage: python SAT.py -Sn inputfile.txt")
        exit(1)

    # ensure the strategy number is valid
    n_strategy = int(sys.argv[1][-1])
    if n_strategy < 1 or n_strategy > 3:
        print("usage: pick 1, 2, or 3 as strategy number, ex. -S1")
        exit(1)

    inputfile = sys.argv[2]
    # add extension if absent
    if ".txt" not in inputfile:
        inputfile = inputfile + ".txt"
    # ensure the file exist
    path = pathlib.Path(inputfile)
    if not path.exists():
        print("{} does not exist".format(inputfile))
        exit(1)

    # run loop
    iterative_dpll(inputfile)

    # TODO: turn this file into a SAT class, with weights as one of its attributes
