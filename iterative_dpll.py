# what does the puzzle state needs to know?
    # dictionary with all the literals and their values
    # a list with the active clauses
    # a list with the choices made so far

# dude's unresolved stands for the literals that should be yeeted from the clauses/ clause lists

def iterative_dpll():
    """
    SAT algorithm that loops iteratively though the search space
    """
    # initialize puzzle start state

    # remove tautologies

    # put A COPY OF the start states on the stack (chosen start var & True and False)

    # start while loop (while stack not empty)

        # pop the last from the stack

        # fill in the value for the chosen var
            # add chosen var to choice tree
            # add to dictionary
            # remove whole clauses that are now true
            # remove only literals that are now false

        # do unit propegation:
            # (false literals worden er uit geyeet)
            # at start, look for clauses with length 0 --> conflict
            # if clause is length one:
                # check in dict if it already had a value:
                    # if yes --> conflict
                    # else: zet clauses of length 1 op true,
                    #       then remove whole clause &
                    #       remove the literal from clauses where its value is now False

        # only do the below if there is NO conflict and there are unsolved clauses left (aka not [], when all clauses are removed)

            # get next random variable to assign
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
