"""
The main SAT-solver program: an iterative DPLL algorithm with three heuristics.
1) random split
2) DCLS split
3) VSIDS split with clause learning and non-chronological backtracking

by Sanne van den Berg and Valerie Sawirja
"""
from dpll_functions import remove_tautologies, perform_split, print_heuristic, get_extensionless, unit_prop, write_output, output_statements
from Puzzle_State import Puzzle_State
from cVSIDS import CDCL, vsids_split, non_chrono_backtrack
import sys
import copy
import pathlib


def iterative_dpll(input_file, heuristic):
    """
    SAT-solver DPLL algorithm that loops iteratively though the search space
    """
    # initialize start variables
    start_state = Puzzle_State(input_file)
    variable_weights = dict.fromkeys(start_state.values, 0)
    file = get_extensionless(input_file)
    stack = []
    n_backtracks = 0

    # remove tautologies
    remove_tautologies(start_state)

    # put A COPY OF the start states on the stack
    first_state = copy.deepcopy(start_state)
    stack.append(first_state)

    # start while loop (while stack not empty)
    while stack:
        # pop the last from the stack
        current_state = stack.pop()

        # do unit propagation:
        n_backtracks, conflict_lit = unit_prop(current_state, n_backtracks)

        if not conflict_lit and len(current_state.clauses) != 0:
            # perform split
            chosen_literal, truth_assignments = \
                perform_split(heuristic, current_state, variable_weights)

            # if there's a chosen literal (not everything is assigned yet)
            if chosen_literal:
                # make children (all possibilities for the new variable)
                for truth in truth_assignments:
                    child = current_state.get_child(chosen_literal, truth)
                    # add child to stack
                    stack.append(child)

        # perform clause learning and non chrono backtracking
        if heuristic == 3 and conflict_lit:
            # make conflict clause, update literal weights, decide backtrack destination
            current_state, variable_weights, back_to_literal = \
                CDCL(conflict_lit, start_state, current_state, variable_weights)

            # do non chrono backtracking
            stack = non_chrono_backtrack(stack, back_to_literal)

        # no clauses left: SAT, found a solution!
        if len(current_state.clauses) == 0:
            print('Number of backtracks:', n_backtracks)
            output_statements("sat", file)
            write_output(inputfile, current_state)
            exit(0)

        # else, conflict. let the loop backtrack

    # broke out of while loop: UNSAT. write output with START puzzle state
    output_statements("unsat", file)
    write_output(inputfile, start_state)
    exit(0)


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

    # add extension if absent
    inputfile = sys.argv[2]
    if ".txt" not in inputfile:
        inputfile = inputfile + ".txt"

    # ensure the file exist
    path = pathlib.Path(inputfile)
    if not path.exists():
        print("{} does not exist".format(inputfile))
        exit(1)

    # print what algorithm is running
    print_heuristic(n_strategy)

    # run algorithm
    iterative_dpll(inputfile, n_strategy)
