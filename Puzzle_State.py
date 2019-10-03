"""
Puzzle class for the SAT solver project.

by Sanne van den Berg and Valerie Sawirja
"""
import pathlib
import copy


class Puzzle_State(object):
    """
    A class for the state of the puzzle at a certain point in the SAT solver
    """

    def __init__(self, inputfile):
        """
        Initializes the attributes for the Puzzle. Contains:
        a dictionary with all the absolute literals and their values,
        a list with active clauses,
        a list with variable splits [chosen_variable, truth_value, [dependents]]
        """
        self.values = {}
        self.clauses = self.load_clauses(inputfile)
        self.choice_tree = [[None, None, [None]]]

    def load_clauses(self, clauses_file):
        """
        Reads in the clauses from a file and fills self.values with literals.
        Returns a list of lists
        """
        # https://stackoverflow.com/questions/28890268/parse-dimacs-cnf-file-python
        filepath = pathlib.Path(clauses_file)

        # create a list for all the clause
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
        Initializes all absolute literals in self.values dict with '?' as value.
        """
        if abs(literal) not in self.values:
            self.values[abs(literal)] = '?'

    def get_truth(self, literal):
        """
        Checks truth value of a literal and accounts for negation.
        Returns 1 if the literal is true, 0 if it's false, and '?' if unassigned.
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
        Changes the value of a literal in self.values and accounts for negation.
        """
        # check if literal is negated
        negated = self.is_negated(literal)

        if not negated or value == '?':
            self.values[literal] = value
        else:
            # if literal is negated assign the opposite values
            if value == 1:
                self.values[abs(literal)] = 0
            else:
                self.values[abs(literal)] = 1

    def is_negated(self, literal):
        """
        Checks if a literal is negated.
        Returns a boolean.
        """
        if literal < 0:
            return True
        else:
            return False

    def update_clauses(self, literal):
        """
        Removes clauses from self.clauses if they turned true.
        Removes literals that turned false from their clauses.
        """
        value = self.get_truth(literal)
        conflict_lit = None
        conflict = False

        for clause in [*self.clauses]:
            # only get clauses that have a version of the literal
            if literal in clause or -literal in clause:
                if value == 1:
                    # clauses that are now true --> remove whole clause
                    if literal in clause:
                        self.clauses.remove(clause)
                    # negated literals become false --> remove from clause
                    else:
                        if len(clause) == 1:
                            # conflict
                            conflict_lit = -literal
                        clause.remove(-literal)

                # if the literal is false
                else:
                    # false: remove literal from clause
                    if literal in clause:
                        if len(clause) == 1:
                            # conflict
                            conflict_lit = literal
                        clause.remove(literal)
                    # whole clause is true
                    else:
                        self.clauses.remove(clause)

        if conflict_lit:
            conflict = True

        return conflict_lit, conflict

    def get_unassigned(self):
        """returns a list with unassigned variables"""
        unassigned = [key for (key, value) in self.values.items() if value == '?']
        return unassigned

    def get_child(self, chosen_literal, truth):
        child = copy.deepcopy(self)
        # 1) add chosen var to choice tree
        child.choice_tree.append([chosen_literal, truth, list()])
        # 2) change value in dictionary
        child.set_truth(chosen_literal, truth)
        # 3) update clauses with new truth assignment
        child.update_clauses(chosen_literal)

        return child
