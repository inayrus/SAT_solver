from Puzzle_State import Puzzle_State
from DLCS_Complete2 import dlcs
from omgconflicts import CDCL
import sys
import random
import copy
import pathlib


def iterative_dpll(inputfile):
    """
    SAT algorithm that loops iteratively though the search space
    """
    # Choose the heuristic
    heuristic = int(input('Please enter 1, 2 or 3 for basic DPLL, the first heuristic or second heuristic, respectively: '))

    # initialize puzzle start state and stack
    start_state = Puzzle_State(inputfile)
    stack = []

    # remove tautologies
    remove_tautologies(start_state)

    # put A COPY OF the start states on the stack (chosen start var & True and False)
    first_state = copy.deepcopy(start_state)
    stack.append(first_state)

    # TODO: what do if there are no more literals to assign randomly choose? how to just skip code and let it backtrack

    # start while loop (while stack not empty)
    while stack:
        print("states in stack: ", len(stack))
        # loop starts without conflict
        conflict = False

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
                        conflict_lit = current_state.update_clauses(literal)
                # if a clause is empty
                elif len(clause) == 0:
                    conflict = True

            print("unit count:", unit_count)

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
            else:
                print('Second heuristic is to be continued. Please enter another.')
                quit()

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

        # if conflict_lit:
        #     current_state = CDCL(conflict_lit, start_state, current_state)

        # no clauses left: SAT, found a solution!
        if len(current_state.clauses) == 0:
            print("SAT. solution saved in {}.out".format(get_extensionless(inputfile)))
            # call write output on the instance.values dict
            write_output(file, current_state)
            exit(0)

        # else, conflict. let the loop backtrack

    # broke out of while loop: UNSAT. write output with START puzzle state
    print("UNSAT. solution saved in {}.out".format(get_extensionless(inputfile)))
    write_output(file, start_state)
    exit(0)


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
    unassigned = [key for (key, value) in puzzle_obj.values.items() if value == '?']
    if unassigned:
        return random.choice(unassigned)
    else:
        return None

def write_output(file, puzzle_obj):
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
        filepath = pathlib.Path(filename + '.out')

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
        return filename.split(".")[0]
    else:
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
    # NEED TO ADD ALL CONTROLS OF SAT FILE
    file = sys.argv[2]

    iterative_dpll(file)
