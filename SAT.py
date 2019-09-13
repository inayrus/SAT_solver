import sys
import pathlib


class SAT(object):
    """Representation of a SAT solver"""

    def __init__(self, clauses_file):
        """
        Initializes clauses and start values of SAT solver
        """
        # values should be a dict, only absolute values
        self.values = {}
        self.clauses = self.load_clauses(clauses_file)

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
            self.values[literal] = '?'

    def davis_putnam(self):
        """
        runs the davis putnam algorithm.
        recursively???
        :return: an DIMACS output file with the true variables

        --> after first simplification, calculate l/n ratio
        """
        # extra var with cleared clauses (pop from old and append to cleared list)

        # set of clauses is 'sat' when all of them are true
        # the set is 'unsat' when there is an empty clause: all literals false

        # at beginning of loop, remove tautologies
        # simplify:
            # unit clauses
                # loop though clauses once
                    # when unit clause found (clause of len 1), adjust truth value
                    # loop through clauses again to filter
                        # copy all clauses that are now True into self.cleared_clauses + remember their index in the OG list
                        # when filter loop finished, remove cleared clauses from attribute
                        # Q: how does removing values from a list impact the for look over the list?
                            # meh you probably need to call the function again with new parameters
                            # Q: would it be possible to use self.clauses then?
                            # Q: do class attr in low depth recursiom change along when high depth changes?
                                # else, make indiv var
            # pure literals
            # --> for every unit
        # split:

    def unit_propagation(self):
        """
        look through all the clauses for unit clauses,
        stores the unit clauses in a list to set to True/False
        throws the unit clauses out of the list with all clauses
        SHOULD IT RETURN SOMETHING?
        """
        # a temporary list to prevent the clauses list from changing
        found_units = list()

        # filter for unit clauses
        for clause in self.clauses:
            # clauses that are length one
            if len(clause) == 1:
                found_units.append(clause[0])
            # check for clauses where all literals except for one are False
            # else:
            #     for literal in clause:

        # turn literals in list to true
        for literal in found_units:
            self.values[literal] = 1

        # add unit clauses to cleared_clauses list


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
    test_dict = {111: '?', 112: 0, 113: '?', 114: 1, 221: 1}
    test_dict[111] = 0
    # print(test_dict)
    # solver.values = test_dict
    # solver.write_output(inputfile)
    solver.unit_propagation()

    print("mlep")
