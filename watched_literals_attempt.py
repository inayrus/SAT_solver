clause_list = [[False, True, '?', False, True, '?', '?', '?', False, '?'], ['?', False, '?', True, '?', '?']]



# #initial watched_literals (make the initial list) --> actual function form comes later
# watched_literals = []
# for i in range(len(clause_list)):
#     watched_literals.append([None] * 2)
#
# # fills watched literals list
# for clause in clause_list:
#     clause_index = clause_list.index(clause)
#     w_l = 0
#     w_l_c = 0
#     while w_l_c < 2:
#         if clause_list[clause_index][w_l] == '?':
#             watched_literals[clause_index][w_l_c] = w_l
#             w_l_c += 1
#         w_l += 1
#         print(watched_literals)
#
#
#
#

watched_literals = []
for clause_i, clause in enumerate(clause_list):
    wl_clause = []
    for lit_i, literal in enumerate(clause):
        if len(wl_clause) == 2:
            # append the wl_clause to watched_literals list
            watched_literals.append(wl_clause)
            break
        elif literal != False:
            # append the index of the literal in its clause
            wl_clause.append(lit_i)

print(watched_literals)

#Experimental clause list with a few changes, if some '?' got values
clause_list = [[False, True, False, False, True, False, False, False, False, '?'], [False, False, False, True, False, False]]



# update watched literals

# get the index and literals list for every clause in watched literals
for literals_i, wl_literals in enumerate(watched_literals):

    # loop over literals in one watched lit clause
    for wl_literal_i, wl_literal in enumerate(wl_literals):

        # value of literal
        value = clause_list[literals_i][wl_literal]
        print(value)

        # if the value of the watched literal has changed
        # ------>>> DOES OUR CLASS USE FALSE OR 0????
        if value == False:
            # remove it from watched lit list
            del watched_literals[literals_i][wl_literal_i]

            # check if literal is the last element in clause
            if clause_list[literals_i][-1] == value:

                # check if watched lits list for one clause is empty
                if len(watched_literals[literals_i]) == 0:
                    print('backtracking')
            else:
                # else, pick next value in clause that is NOT in watched lit list
                # and whose value is not False
                for new_lit_i, new_lit in enumerate(clause_list[literals_i]):
                    if new_lit_i not in wl_literals and new_lit != False:
                        wl_literals.append(new_lit_i)
                        print(new_lit_i)
                        break

print(watched_literals)

# unit prop if watched lit clause has length 1
# do nothing if it has a watched lit that is true
