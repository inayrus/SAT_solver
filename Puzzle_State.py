import pathlib

class Puzzle_State(object):
    """
    A class for the state of the puzzle at a certain point in the SAT solver
    """

    def __init__(self, inputfile):
        """
        Initialized the attributes for the Puzzle
        what does the puzzle state needs to know?
            dictionary with all the literals and their values
            a list with the active clauses
            a list with the choices made so far
        """
        self.values = {}
        self.clauses = self.load_clauses(inputfile)
        self.choice_tree = []

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

    def update_clauses(self, literal):
        """
        removes whole clauses that are now true
        removes only literals that are now false
        """
        value = self.get_truth(literal)

        for clause in self.clauses:
            # only get clauses that have a version of the literal
            if literal in clause or -literal in clause:
                # if the literal is true
                if value == 1:
                    # clauses that are now true --> remove whole clause
                    if literal in clause:
                        self.clauses.remove(clause)
                    # negated literals become false --> remove from clause
                    else:
                        clause.remove(-literal)
                # if the literal is false
                else:
                    # false: remove literal from clause
                    if literal in clause:
                        clause.remove(literal)
                    # negated means whole clause is true
                    else:
                        self.clauses.remove(clause)




