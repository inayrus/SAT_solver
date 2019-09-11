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
        """
        # extra var with cleared clauses (pop from old and append to cleared list)


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
    print(len(solver.clauses))
    print(solver.clauses)

    print("mlep")
