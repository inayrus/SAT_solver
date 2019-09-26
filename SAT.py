import sys
import pathlib
import random
import DLCS_Complete

class SAT(object):
    """Representation of a SAT solver"""

    def __init__(self, clauses_file):
        """
        Initializes clauses and start values of SAT solver
        """
        self.values = {}
        self.clauses = self.load_clauses(clauses_file)
        # self.values = {111: '?', 114: '?', 116: '?', 298: '?', 160: '?', 196: '?', 161: '?', 138: '?', 489: '?', 982: '?', 274: '?'}
        # self.clauses = [[-111, -114], [116, 298], [160, 196, 161, -138, 489, 982, 274]]
        self.choice_tree = []
        # can check [-1] in choice list to remember where dependency should be added
        self.dependencies = {}
        self.watched_literals = self.set_watched_literals()
        self.sat_or_unsat = False
        self.backs = 0

    def load_clauses(self, clauses_file):
        """
        reads in the clauses from a file and fills self.values with literals
        returns a list of lists
        """
        # https://stackoverflow.com/questions/28890268/parse-dimacs-cnf-file-python
        filepath = pathlib.Path(clauses_file)

        # create a list for all the clauses
        clauses = list()

        # read in the file
        with filepath.open('r') as f:
            for line in f:
                symbols = line.split()

                # skip empty lines and lines with comments
                if len(symbols) != 0 and symbols[0] not in ("p", "c"):
                    clause = list()

                    for symbol in symbols:
                        literal = int(symbol)
                        # add clause to clauses list if line terminated with 0
                        if literal == 0:
                            clauses.append(clause)
                        else:
                            # add literal to clause
                            clause.append(literal)
                            # add literal to self.values
                            self.init_values(literal)
        return clauses

    def init_values(self, literal):
        """
        checks if the literal is already in the self.values dict,
        if it's not, it creates a new key-value pair (only absolute values)
        ex. 'literal': '?'
        """
        if abs(literal) not in self.values:
            self.values[abs(literal)] = '?'

    def set_watched_literals(self):
        """
        stores two literals for every clause, where the value of the literal
        is not false
        """
        watched_literals = []
        for clause in self.clauses:
            # store watched literals for clauses longer than 1
            if len(clause) > 1:
                wl_clause = []
                for lit_i, literal in enumerate(clause):
                    if len(wl_clause) == 2:
                        break
                    elif self.get_truth(literal) != 0:
                        # if value not false, append index of the literal in its clause
                        wl_clause.append(literal)
                # append the wl_clause to watched_literals list
                watched_literals.append(wl_clause)
        return watched_literals

    def davis_putnam(self, file):
        """
        runs the davis putnam algorithm.
        recursively???
        :return: an DIMACS output file with the true variables

        --> after first simplification, calculate l/n ratio
        """
        # remove tautologies
        self.remove_tautologies()

        while self.sat_or_unsat == False:
            # check for unit clauses
            self.unit_propagation_loop()

            # update watched literals
            conflict = self.update_watched_literals()
            if conflict:
                # if conflict: backtracking
                self.chron_backtrack()

            if self.sat_or_unsat == False:
                # branching
                self.split_s1()
                # DLCS_Complete2.dlcs(self.values, self.clauses)

            # # update watched literals
            # conflict = self.update_watched_literals()
            # if conflict:
            #     # if conflict: backtracking
            #     self.chron_backtrack()

        # call output function if SAT or UNSAT
        self.write_output(file)

    def unit_propagation_loop(self):
        """
        looks through all the clauses for unit clauses,
        stores the unit clauses in a list to set to True/False
        keeps looping until no more unit clause is found
        """
        # value to start the loop
        unit_count = 1

        while unit_count > 0:
            # a temporary list to prevent the clauses list from changing
            found_units = set()
            unit_count = 0
            print("entered unit loop again")

            # filter for unit clauses
            for clause in self.clauses:
                # clauses that are length one and not already True
                if len(clause) == 1 and self.get_truth(clause[0]) != 1:
                    found_units.add(clause[0])
                    unit_count += 1
                else:
                    # check for clauses with False literals and only one unassigned
                    false_count = 0
                    hidden_unit = []
                    for index, literal in enumerate(clause):
                        # break if two literals are not False and the clause is true
                        if false_count < index - 1 or self.get_truth(literal) == 1:
                            hidden_unit = []
                            break
                        elif self.get_truth(literal) == 0:
                            false_count += 1
                        # remember only unassigned
                        else:
                            hidden_unit.append(literal)
                    # only add to found units if one unassigned
                    if len(hidden_unit) == 1:
                        found_units.add(hidden_unit[0])
                        unit_count += 1

            # turn literals in list to true
            for literal in found_units:
                self.set_truth(literal, 1)
                print(abs(literal), self.values[abs(literal)])
            print(unit_count)

            # if units are found bc of split choice, add them as dependencies
            if len(self.choice_tree) != 0:
                chosen = self.choice_tree[-1][0]
                self.dependencies[chosen].update(found_units)

    def split_s1(self):
        """
        branching strategy 1: basic davis putnam.
        a random unassigned variable will be chosen
        """
        print("split variable")
        # choose random unassigned variable
        unassigned = [key for (key, value) in self.values.items() if value == '?']
        if unassigned != []:
            random.seed(9)
            chosen = random.choice(unassigned)

            # set the variable to true
            self.set_truth(chosen, 1)

            # document choice
            self.choice_tree.append([chosen, True])

            # create dependency var
            self.dependencies[chosen] = set()
            print("new split: {}".format(self.choice_tree))
        elif self.sat_or_unsat == True:
            return
        else:
            print("no more literals to split")
            print("backtrack numbers: {}".format(self.backs))
            # print the truth value of the things in the watched literals
            print("number empty clauses: {}".format(len([clause for clause in self.watched_literals if len(clause) == 0])))
            self.sat_or_unsat = True
            exit(1)

    def update_watched_literals(self):
        """
        updates the watched literals list
        counts how many clauses are true and updates self.sat_or_unsat if all clauses are true
        returns True if an empty clause is found, else it returns False
        """
        print("updating watched lits")
        true_count = 0

        # loop over all the watched literals
        for clause_i, watched_clause in enumerate(self.watched_literals):
            to_remove= list()

            # for clauses longer than 1
            if len(watched_clause) > 1:
                for literal in watched_clause:

                    # if the value of the literal is False
                    value = self.get_truth(literal)
                    if value == 0:
                        # add literal to to_remove list
                        to_remove.append(literal)
                    elif value == 1:
                        # count how many clauses are true
                        true_count += 1
                        break

                # remove here to prevent items being skipped
                for literal in to_remove:
                    watched_clause.remove(literal)

                # add other literals that are True or '?' to watched list
                if len(watched_clause) < 2:
                    for new_lit in self.clauses[clause_i]:
                        if new_lit not in watched_clause and self.get_truth(new_lit) != 0:
                            watched_clause.append(new_lit)
                            #
                            # if self.get_truth(new_lit) == 1:
                            #     true_count += 1
                            #     break

                        # break out of loop if 2 literals in watched list
                        if len(watched_clause) == 2:
                            break

            # return if watched list is empty (all literals are False)
            if len(watched_clause) == 0:
                return True

        # update attribute if all clauses are true
        if true_count >= len(self.watched_literals):
            self.sat_or_unsat = True
            print("THING IS SAT")
            print("backs: ", self.backs)

        print("{} out of {} clauses are true".format(true_count, len(self.watched_literals)))
        return False

    def chron_backtrack(self):
        """
        chronological backtracking:
        - goes to the previous made split in the choice tree
        - turns the literal from True to False
        - unassigns all values that depended on that literal
        - if the value was already False, backtrack to the next upper level of
        the choice tree and do the same as above

        if len(choice_tree) == 0, unsat is set to True
        - after backtrack, unit prop and split need to be called again
        """

        self.backs += 1

        # var to start the loop off
        assigned_truth = False
        # keep track of the literals that might have dependent variables
        chosen_literals = list()

        # keep backtracking if the truth value of literal is flipped before
        while assigned_truth == False:
            # if backtracked to first choice in choice_tree twice, return unsat
            if len(self.choice_tree) == 0:
                self.sat_or_unsat = True
                print("THING IS UNSAT")
                print("number of backtracks: {}".format(self.backs))
                return

            # remove the previous made split in choice tree
            last_choice, assigned_truth = self.choice_tree.pop(-1)
            chosen_literals.append(last_choice)

        # undo truth values
        for literal in chosen_literals:
            # undo literals
            self.set_truth(literal, '?')
            # undo dependencies
            lit_dependencies = self.dependencies[literal]
            for dependent in lit_dependencies:
                self.set_truth(dependent, '?')
            # empty dependency set
            self.dependencies[literal] = set()

        # change value literal from True to False (last item always value True)
        flip_lit = chosen_literals[-1]
        self.set_truth(flip_lit, 0)
        self.choice_tree.append([flip_lit, False])

        print("BACKTRACK: {}".format(self.choice_tree))
        # print("choice tree: {}".format(self.choice_tree))
        # print("values: {}".format(self.values))

    def get_truth(self, literal):
        """
        checks the truth value of a variable and takes negation into account
        returns 1 if the literal is true, 0 if it's false, and '?' if unassigned
        """
        # check if the literal is negated
        negated = self.is_negated(literal)

        # get value from the truth value dictionary
        assigned = self.values[abs(literal)]

        if negated == False or assigned == '?':
            return assigned
        # if literal is negated: return the opposite values
        else:
            if int(assigned) == 1:
                return 0
            else:
                return 1

    def set_truth(self, literal, value):
        """
        changes the value of a literal in self.values and takes negation of the
        literal into account
        """
        # check if literal is negated
        negated = self.is_negated(literal)

        if not negated or value == '?':
            self.values[literal] = value
        else:
            # if literal is negated assign the opposite values
            if value == 1:
                self.values[abs(literal)] = 0
            elif value == 0:
                self.values[abs(literal)] = 1
            else:
                print("something went wrong")

    def is_negated(self, literal):
        """
        checks if a literal is negated
        returns a boolean
        """
        if literal < 0:
            return True
        else:
            return False


    def remove_tautologies(self):
        """
        removes tautologies from the list of clauses
        (ex. -111 and 111 in the same clause)
        """
        tautologies = []
        for index, clause in enumerate(self.clauses):
            for literal in clause:
                positive = 0 + abs(literal)
                negative = 0 - abs(literal)
                if positive in clause and negative in clause:
                    tautologies.append(index)
                    break

        # delete the tautologies from last to first (keeps right order)
        for index in reversed(tautologies):
            del self.clauses[index]


    def write_output(self, filename):
        """
        Takes a dictionary with values and their truth assignment and writes it
        to a file in DIMACS notation.
        """
        # check if inputfile has the .txt extension, if yes, remove it
        if ".txt" in filename:
            filename = filename.split(".")[0]

        # get a list with all literals that are True
        true_literals = self.filter_true_literals()
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

        # what to do if the file already exists? append?? create filename+1??

    def filter_true_literals(self):
        """
        takes self.values,
        returns the variables that have truth assignment '1' in a list
        """
        true_literals = list()

        for var in self.values:
            if self.values[abs(var)] == 1 and var > 0:
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

    # create a SAT object and read in the files
    solver = SAT(inputfile)

    # test lineeeesss
    test_dict = {111: '?', 114: '?', 116: '?', 298: '?', 160: '?', 196: '?', 161: '?', 138: '?', 489: '?', 982: '?', 274: '?'}
    test_clause = [[-111, -114], [116, 298], [160, 196, 161, -138, 489, 982, 274]]

    solver.davis_putnam(inputfile)

    print("mlep")
