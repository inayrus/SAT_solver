"""
A file with functions to let the DPLL in SAT.py run.

by Sanne van den Berg and Valerie Sawirja
"""
import random
import pathlib
from DLCS_Complete import dlcs
from cVSIDS import vsids_split

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


def unit_prop(current_state, n_backtracks):
    """
    Sets clauses of length 1 to True, then updates the active clauses.
    Adds found units as dependents to a literal.
    Loop continues until no more unit clauses are found or it ran into conflict.
    Returns the number of backtracks (int) and the conflict literal (int).
    """
    # loop starts without conflict
    conflict = False
    conflict_lit = None
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
                    conflict = True
                else:
                    # set clauses of length 1 on true, update clauses
                    current_state.set_truth(literal, 1)
                    conflict_lit, conflict = current_state.update_clauses(literal)
            # stop for loop if conflict
            if conflict:
                n_backtracks += 1
                return n_backtracks, conflict_lit

        # add all found units of unit propagation as dependents of previous split
        current_state.choice_tree[-1][-1] = list(found_units)

    return n_backtracks, conflict_lit


def random_choice(puzzle_obj):
    """
    Returns a random choice from unassigned literals
    Returns None if all literals are assigned
    """
    unassigned = puzzle_obj.get_unassigned()
    if unassigned:
        return random.choice(unassigned)
    else:
        return None


def perform_split(heuristic, current_state, variable_weights):
    """
    Performs one of three split functions: (1) random, (2) dlcs, (3) vsids
    Returns a literal (int),
    Returns a list with truth value orders, where the last value is used first.
    """
    if heuristic == 1:
        chosen_literal = random_choice(current_state)
        truth_assignments = [0, 1]
    elif heuristic == 2:
        chosen_literal, truth_assignments = dlcs(current_state.values, current_state.clauses)
    else:
        chosen_literal = vsids_split(current_state, variable_weights)
        truth_assignments = [0, 1]

    return chosen_literal, truth_assignments


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
    file_path = pathlib.Path(filename + '.out')

    # write to 'filename.out'
    with file_path.open(mode='w') as writer:
        # comment
        writer.write("c A solution for {}:\n".format(filename))

        # p cnf nvar nclauses
        writer.write("p cnf {} {}\n".format(n_true_lits, n_true_lits))

        # write the literals
        for var in true_literals:
            writer.write("{} 0\n".format(str(var)))
    return


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


def print_heuristic(heuristic):
    """
    informs the user what algorithm is running
    """
    if heuristic == 1:
        print("Running DPLL with random split heuristic.")
    elif heuristic == 2:
        print("Running DPLL with DLCS split heuristic.")
    else:
        print("Running DPLL with VSIDS, clause learning, and non_chronological backtracking.")

def output_statements(status, file):
    if status == "sat":
        print("SAT. solution saved in {}.out".format(file))
        # Ascii art retrieved from http://www.patorjk.com
        print('''
                   ___     ___    _____  
                  / __|   /   \  |_   _| 
                  \__ \   | - |    | |   
                  |___/   |_|_|   _|_|_  
                _|"""""|_|"""""|_|"""""| 
                "`-0-0-'"`-0-0-'"`-0-0-' ''')
    else:
        print("UNSAT. solution saved in {}.out".format(file))
        # Ascii art retrieved from http://www.patorjk.com
        print('''
                      ██████  ▄▄▄     ▄▄▄█████▓ ███▄    █ ▓█████   ██████   ██████ 
                    ▒██    ▒ ▒████▄   ▓  ██▒ ▓▒ ██ ▀█   █ ▓█   ▀ ▒██    ▒ ▒██    ▒ 
                    ░ ▓██▄   ▒██  ▀█▄ ▒ ▓██░ ▒░▓██  ▀█ ██▒▒███   ░ ▓██▄   ░ ▓██▄   
                      ▒   ██▒░██▄▄▄▄██░ ▓██▓ ░ ▓██▒  ▐▌██▒▒▓█  ▄   ▒   ██▒  ▒   ██▒
                    ▒██████▒▒ ▓█   ▓██▒ ▒██▒ ░ ▒██░   ▓██░░▒████▒▒██████▒▒▒██████▒▒
                    ▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░ ▒ ░░   ░ ▒░   ▒ ▒ ░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
                    ░ ░▒  ░ ░  ▒   ▒▒ ░   ░    ░ ░░   ░ ▒░ ░ ░  ░░ ░▒  ░ ░░ ░▒  ░ ░
                    ░  ░  ░    ░   ▒    ░         ░   ░ ░    ░   ░  ░  ░  ░  ░  ░  
                          ░        ░  ░                 ░    ░  ░      ░        ░  ''')