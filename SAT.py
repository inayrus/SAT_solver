import sys
import pathlib
import random


class SAT(object):
    """Representation of a SAT solver"""

    def __init__(self, clauses_file):
        """
        Initializes clauses and start values of SAT solver
        """
        self.values = {}
        self.clauses = self.load_clauses(clauses_file)
        self.choice_tree = []
        # can check [-1] in choice list to remember where dependency should be added
        self.dependencies = {}

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

    def davis_putnam(self):
        """
        runs the davis putnam algorithm.
        recursively???
        :return: an DIMACS output file with the true variables

        --> after first simplification, calculate l/n ratio
        """
        # remove tautologies
        self.remove_tautologies()

        # BEGIN loop met stop wanneer wannEER??????????
        # --> check for unit clauses in a while loop
        self.unit_propagation()
        # --> branching
        self.split_S1()
        # ^^ loop continues until conflict: watched literals done / clause == False
            # if conflict: backtracking
            # bijhouden stappen --> lijst in lijst met chosen var en its assignment
                # [[x1, True], [x2, False]]
            # bijhouden dependency: what choice led to what simplification assignment
                # {x2: [x4]}
            # wanneer backtracken, [-1] index poppen en veranderen van True --> False.
            # als value al False, pop the next [-1] index in stappen list

        # set of clauses is 'sat' when all of them are true
        # --> call output function
        # the set is 'unsat' when there is an empty clause: all literals false
        # --> is unsat when stuff has backtracked to step 0 and wants apply [-1] again

        # split:

    def unit_propagation(self):
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

    def split_S1(self):
        """
        branching strategy 1: basic davis putnam.
        a random unassigned variable will be chosen
        """
        # choose random unassigned variable
        unassigned = [key for (key, value) in self.values.items() if value == '?']
        chosen = random.choice(unassigned)

        # set the variable to true
        self.set_truth(chosen, 1)

        # document choice
        self.choice_tree.append([chosen, True])

        # create dependency var
        self.dependencies[chosen] = set()
        print(self.dependencies)

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
            if assigned == 1:
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

        if not negated:
            self.values[literal] = value
        else:
            # if literal is negated assign the opposite values
            if value == 1:
                self.values[abs(literal)] = 0
            else:
                self.values[abs(literal)] = 1

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

        # create new file if 'filename.out' doesn't exist yet
        if not filepath.exists():
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
            if self.values[var] == 1:
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
    test_dict = {111: '?', 112: '?', 113: '?', 114: '?', 221: '?'}
    test_clause = [[-111, -114], [116, 298], [160, 196, -160]]
    # print(test_dict)
    # solver.values = test_dict
    # solver.write_output(inputfile)
    solver.davis_putnam()

    # MAYBE ISSUE -225 IS FIRST RUNTHOUGH FOT GETTING VARS IN DICT??? MUST ALL ME POSITIVE

    print("mlep")
