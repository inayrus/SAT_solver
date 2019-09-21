# what does the puzzle state needs to know?
    # dictionary with all the literals and their values
    # a list with the active clauses
    # a list with the choices made so far

# dude's unresolved stands for the literals that should be yeeted from the clauses/ clause lists
from Puzzle_State import Puzzle_State
import sys
import random
import copy


def iterative_dpll(inputfile):
    """
    SAT algorithm that loops iteratively though the search space
    """
    # initialize puzzle start state and stack
    start_state = Puzzle_State(inputfile)
    stack = []

    # remove tautologies
    remove_tautologies(start_state)

    # put A COPY OF the start states on the stack (chosen start var & True and False)
    first_state = copy.deepcopy(start_state)

    # TODO ---> IPV RANDOM CHOICE KAN JE HIER BETER EERST BEGINNEN MET EEN ENKELE UNIT PROP
    chosen = random_choice(first_state)
    stack.append([first_state, chosen, 1])
    stack.append([first_state, chosen, 0])

    # start while loop (while stack not empty)
    while stack:

        # loop starts without conflict
        conflict = False

        # pop the last from the stack
        state_obj, chosen_literal, value = stack.pop()

        # fill in the value for the chosen var
        # 1) add chosen var to choice tree
        state_obj.choice_tree.append(chosen_literal)
        # 2) change value in dictionary
        state_obj.set_truth(chosen_literal, value)
        # 3) update clauses with new truth assignment
        state_obj.update_clauses(chosen_literal)

        # look for clauses with length 0 --> conflict
        if [] in state_obj.clauses:
            conflict = True

        # do unit propagation:
        for clause in state_obj.clauses:
            if conflict:
                break
            else:
                # if clause is length one:
                if len(clause) == 1:
                    literal = clause[0]
                    # check dict if it has a value that makes this clause False:
                    if state_obj.get_truth(literal) == 0:
                        # if yes --> conflict
                        conflict = True
                    else:
                        # set clauses of length 1 on true,
                        state_obj.set_truth(literal, 1)
                        # update the clauses
                        state_obj.update_clauses(literal)
                        # --> TODO: DO THE ABOVE ALL AT ONCE, SAVE IN LIST, SEE SAT
                        # TODO: IS DEPENDENCY LIST NECESSARY?

        # only do the below if there is NO conflict and there are unsolved clauses left (aka not [], when all clauses are removed)
        if not conflict and len(state_obj.clauses) != 0:

            # get next random variable to assign
            chosen = random_choice(state_obj)
            child_obj
            stack.append([state_obj, chosen, 1])
            stack.append([state_obj, chosen, 0])
                # (if it exists, else allow to backtrack --> var reached_end = True)
                # (though reaching the end should not be an issue. bc by then it should have a solution or conflict)
                # HHHH HOW DO YOU KNOW IF THERE ARE VARS TO CHOOSE LEFT

            # create all possibilities for the new variable

            # put all children on the stack
                # --> [instance, split_var, boolean_for_split_var]

        # elif (len clauses == 0) : SAT, found a solution!
            # return the class of the current puzzle state/ call write output on the instance.values dict

        # else, conflict. let the loop continue with [-1] state

    # broke out of while loop: UNSAT
        # return the class of the START puzzle state/ call write output on the START instance.values dict

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
    random.seed(9)
    unassigned = [key for (key, value) in puzzle_obj.values.items() if value == '?']
    return random.choice(unassigned)


if __name__ == "__main__":
    # NEED TO ADD ALL CONTROLS OF SAT FILE
    file = sys.argv[2]

    iterative_dpll(file)
