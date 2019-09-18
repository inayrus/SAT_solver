" test"

# blub = [1, 2, 6, [2, 5]]
# blubb = []
#
# for i in range(len(blub)):
#     blubb.append([None] * 2)
#
# print(blubb)
#
# blubb[1][0] = blub[2]
# print(blubb)



#item = [1:len(blub)]
#for item in blubb
#    blubb[item] = [None] *2
#print(blubb)


clause_list = [[False, True, '?', False, True, '?', '?', '?', False, '?'], ['?', False, '?', True, '?', '?']]



#initial watched_literals (make the initial list) --> actual function form comes later
watched_literals = []
for i in range(len(clause_list)):
    watched_literals.append([None] * 2)

# fills watched literals list
for clause in clause_list:
    clause_index = clause_list.index(clause)
    w_l = 0
    w_l_c = 0
    while w_l_c < 2:
        if clause_list[clause_index][w_l] == '?':
            watched_literals[clause_index][w_l_c] = w_l
            w_l_c += 1
        w_l += 1
        print(watched_literals)


#Experimental clause list with a few changes, if some '?' got values
clause_list = [[False, True, False, False, True, False, False, False, False, '?'], [False, False, False, True, False, False]]




# #the len thing is working. after literal is too big for len it removes the value from the clause and if clause is empty it says something about satisfiability checks
# #BUTTTTTTTTTTTT. It gets confused about double values.
# #later watched literals
# print('hey') # just so I know in output where it begins
# for literals in watched_literals:
#     literals_index = watched_literals.index(literals)
#     for literal in literals:    #already the actual number itself
#         literal_index = watched_literals[literals_index].index(literal)
#         while clause_list[literals_index][literal] != '?' and len(watched_literals[literals_index]) > 0:
#             print('literal', literal)
#             print('len', len(clause_list[literals_index]))
#             if (literal + 1) > (len(clause_list[literals_index]) - 1):
#                 print('owps')
#                 del watched_literals[literals_index][literal_index]
#                 print(watched_literals)
#                 if len(watched_literals[literals_index]) == 0:
#                     print('Now satisfiability check should be performed') #if it is: great. it'll not loop over this again (bcs len). If it is not? -> call the formula for backtracking or to stop the operation entirely (if no backtracking can be done anymore)
#                     print(watched_literals)
#             elif (literal + 1) not in watched_literals[literals_index]:
#                 literal += 1
#                 watched_literals[literals_index][literal_index] = literal
#                 print(watched_literals)
#             else:
#                 literal += 2
#                 print('updated literal', literal)
#                 if literal not in watched_literals and literal <= (len(clause_list[literals_index]) - 1):
#                     watched_literals[literals_index][literal_index] = literal
#                     print(watched_literals[literals_index])
#                     print('updated lit', literal)
#

# #Experiment with functions here
# def already_in_clause(clause, literal):
#     if literal in clause:
#         return True
#     else:
#         return False
#
#
#
# def check_clause_length(literal, literals_index, list):
#     if literal > (len(list[literals_index]) - 1):
#         print('owps')
#         del watched_literals[literals_index][literal_index]
#         print(watched_literals)
#         if len(watched_literals[literals_index]) == 0:
#             print('Now satisfiability check should be performed')  # if it is: great. it'll not loop over this again (bcs len). If it is not? -> call the formula for backtracking or to stop the operation entirely (if no backtracking can be done anymore)
#             print(watched_literals)
#
#
#
# print('hey') # just so I know in output where it begins
# for literals in watched_literals:
#     literals_index = watched_literals.index(literals)
#     for literal in literals:
#         literal_index = watched_literals[literals_index].index(literal)
#         while clause_list[literals_index][literal] != '?':
#             literal += 1
#             check_clause_length(literal, literals_index, clause_list)
#             if already_in_clause(watched_literals[literals_index], literal):
#                 literal += 1
#                 check_clause_length(literal, literals_index, clause_list)
#             else:
#                 watched_literals[literals_index][literal_index] = literal
#
#Experiment over

            #
            # if (literal + 1) > (len(clause_list[literals_index]) - 1):
            #     print('owps')
            #     del watched_literals[literals_index][literal_index]
            #     print(watched_literals)
            #     if len(watched_literals[literals_index]) == 0:
            #         print('Now satisfiability check should be performed')
            #         print(watched_literals)
            # elif (literal + 1) not in watched_literals[literals_index]:
            #     literal += 1
            #     watched_literals[literals_index][literal_index] = literal
            #     print(watched_literals)
            # else:
            #     literal += 2
            #     print('updated literal', literal)
            #     if literal not in watched_literals and literal <= (len(clause_list[literals_index]) - 1):
            #         watched_literals[literals_index][literal_index] = literal
            #         print(watched_literals[literals_index])
            #         print('updated lit', literal)
            #     elif literal > (len(clause_list[literals_index]) - 1):
            #         print('owps')
            #         del watched_literals[literals_index][literal_index]
            #         print(watched_literals)
            #         if len(watched_literals[literals_index]) == 0:
            #             print('Now satisfiability check should be performed')  # if it is: great. it'll not loop over this again (bcs len). If it is not? -> call the formula for backtracking or to stop the operation entirely (if no backtracking can be done anymore)
            #             print(watched_literals)
            #         elif literal_index == 1:
            #             print('boom')
            #             literals_index = watched_literals.index(literals) + 1
            #             literals = watched_literals[literals_index]
            #             print(literals)
            #
            #

#     else:
#         literal += 1
#         watched_literals[literals_index][literal_index] = literal
#
#
# def check_clause_length(literal, literals_index, list):
#     if (literal + 1) > (len(list[literals_index]) - 1):
#         print('owps')
#         del watched_literals[literals_index][literal_index]
#         print(watched_literals)
#         if len(watched_literals[literals_index]) == 0:
#             print('Now satisfiability check should be performed')  # if it is: great. it'll not loop over this again (bcs len). If it is not? -> call the formula for backtracking or to stop the operation entirely (if no backtracking can be done anymore)
#             print(watched_literals)
#
#
# def

#THIS ONE IS GOOD (well, semi)
#the len thing is working. after literal is too big for len it removes the value from the clause and if clause is empty it says something about satisfiability checks
#BUTTTTTTTTTTTT. It gets confused about double values.
# #later watched literals
print('hey') # just so I know in output where it begins
for literals in watched_literals:
    literals_index = watched_literals.index(literals)

    # loops over literals per watched lit clause
    for literal in literals:    #already the actual number itself
        literal_index = watched_literals[literals_index].index(literal)

        # only enters when an item in watched lits has changed value, no longer '?'
        while clause_list[literals_index][literal] != '?' and len(watched_literals[literals_index]) > 0:
            print('literal', literal)
            print('len', len(clause_list[literals_index]))

            # literal represents the index of a value in clause_list
            if (literal + 1) > (len(clause_list[literals_index]) - 1):
                # if no more literals in clause to watch
                print('owps')
                del watched_literals[literals_index][literal_index]
                print(watched_literals)
                if len(watched_literals[literals_index]) == 0:
                    print('Now satisfiability check should be performed')
                    print(watched_literals)
            # update value to watch --> but also has to check whether the new value is also unassigned
            elif (literal + 1) not in watched_literals[literals_index]:
                literal += 1
                watched_literals[literals_index][literal_index] = literal
                print(watched_literals)
            else:
                literal += 2
                print('updated literal', literal)
                if literal not in watched_literals and literal <= (len(clause_list[literals_index]) - 1):
                    watched_literals[literals_index][literal_index] = literal
                    print(watched_literals[literals_index])
                    print('updated lit', literal)
                elif literal > (len(clause_list[literals_index]) - 1):
                    print('owps')
                    del watched_literals[literals_index][literal_index]
                    print(watched_literals)
                    if len(watched_literals[literals_index]) == 0:
                        print('Now satisfiability check should be performed')  # if it is: great. it'll not loop over this again (bcs len). If it is not? -> call the formula for backtracking or to stop the operation entirely (if no backtracking can be done anymore)
                        print(watched_literals)
                    elif literal_index == 1:
                        print('boom')
                        literals_index = watched_literals.index(literals) + 1
                        literals = watched_literals[literals_index]
                        print(literals)


                        # issue....... this discontinues the loop for some reason. doesn't go to next clause.


#
# #the len thing is working. after literal is too big for len it removes the value from the clause and if clause is empty it says something about satisfiability checks
# #BUTTTTTTTTTTTT. It gets confused about double values.
# #later watched literals
# print('hey') # just so I know in output where it begins
# for literals in watched_literals:
#     literals_index = watched_literals.index(literals)
#     for literal in literals:    #already the actual number itself
#         literal_index = watched_literals[literals_index].index(literal)
#         while clause_list[literals_index][literal] != '?' and len(watched_literals[literals_index]) > 0:
#             print('literal', literal)
#             print('len', len(clause_list[literals_index]))
#             if (literal + 1) > (len(clause_list[literals_index]) - 1):
#                 print('owps')
#                 del watched_literals[literals_index][literal_index]
#                 print(watched_literals)
#                 if len(watched_literals[literals_index]) == 0:
#                     print('Now satisfiability check should be performed')
#                     print(watched_literals)
#             elif (literal + 1) not in watched_literals[literals_index]:
#                 literal += 1
#                 watched_literals[literals_index][literal_index] = literal
#                 print(watched_literals)
#             else:
#                 literal += 2
#                 print('updated literal', literal)
#                 if literal not in watched_literals and literal <= (len(clause_list[literals_index]) - 1):
#                     watched_literals[literals_index][literal_index] = literal
#                     print(watched_literals[literals_index])
#                     print('updated lit', literal)
#                 elif literal > (len(clause_list[literals_index]) - 1):
#                     print('owps')
#                     del watched_literals[literals_index][literal_index]
#                     print(watched_literals)
#                     if len(watched_literals[literals_index]) == 0:
#                         print('Now satisfiability check should be performed')  # if it is: great. it'll not loop over this again (bcs len). If it is not? -> call the formula for backtracking or to stop the operation entirely (if no backtracking can be done anymore)
#                         print(watched_literals)
#                     elif literal_index == 1:
#                         print('boom')
#                         next(watched_literals[literals])
#                         # issue....... this discontinues the loop for some reason. doesn't go to next clause.

print('done', watched_literals)


#THE LINES BELOW WORK, BUT I DO NOT HAVE THE LEN THING IN IT YET.
# #later watched literals
# print('hey')
# for literals in watched_literals:
#     literals_index = watched_literals.index(literals)
#     for literal in literals:    #already the actual number itself
#         literal_index = watched_literals[literals_index].index(literal)
#         if literal < (len(clause_list[literals_index])):
#             while clause_list[literals_index][literal] != '?': #it isn't doing the second part yet #endless while loop at the moment
#                 #if len(clause_list[literals_index])-2 in watched_literals[literals_index]:  # is not working yet
#                  #   print('owps')  # This will become the part where it should eventually maybe start checking for satisfied clauses or not
#                   #  del watched_literals[literals_index][literal-1]
#                    # if len(watched_literals[literals_index]) < 2:
#                     #    print('Now satisfiability check should be performed')
#                 #else:
#                     literal += 1
#                     if clause_list[literals_index][literal] == '?' and literal in watched_literals[literals_index]:
#                         literal += 1
#                     if clause_list[literals_index][literal] == '?' and literal not in watched_literals[literals_index]:
#                         watched_literals[literals_index][literal_index] = literal
#                         print(watched_literals)
# #        if literal == len(clause_list[literals_index]):


#ISSUES
#- de if statements....
#VNM HET LENGTE DING. WANNEER WEET IE DAT HET OP IS
# en daarna aanroepen van functie die bepaalt of clause true of niet is.
# dunno if truth values are already in the clause thingies... Should?




#                clause_list[literals_index][literal].index != watched_literals[literals_index][1]:


#        print(literal)
#        print(watched_literals[literals_index][0])
#        bla = watched_literals[literals_index][literal]
#        print(bla)
#        literal_index = watched_literals[literals_index][literal]
#        print(literal_index)
#literal_index = watched_literals[literals_index].index(literal)
#        print(literal_index)
#       if clause_list[literals_index][literal_index] != '?': #no... that would make it 2 for instance. but value in list could actually be 5 --> go there instead
#            new_index = literal_index + 1
#            watched_literals[literals_index][literal_index] = clause_list[literals_index][new_index]







#
# #I could do this better. Instead of 2 lists with 1 the indices and 2nd the truth values... Do 1 list with indices and check it against the clause list values
#
# clause_list = [['?', True, '?', False, True, '?', '?', '?', False, '?'], ['?', False, '?', True, '?', '?']]
# watched_literals = []
# watched_indices = []
# for i in range(len(clause_list)):
#     watched_literals.append([None] * 2)
#     watched_indices.append([None] * 2)
# #print(watched_literals)
# #print(watched_indices)
#
# #initial watched_literals
# for clause in clause_list:
#     clause_index = clause_list.index(clause)
#     print(clause_index)
#     w_l = 0
#     w_l_c = 0
#     while w_l_c < 2:
#         if clause_list[clause_index][w_l] == '?':
#             watched_literals[clause_index][w_l_c] = clause_list[clause_index][w_l]
#             w_l_c += 1
# #            watched_indices[clause_index][w_l_c] = w_l
#         w_l += 1
#         print(watched_literals)
# #        print(watched_indices)
#
# #later watched_literals
# #for literals in watched_literals:
# #    if False in literals:
#



# for clause in clause_list:
#     clause_index = clause_list.index(clause)
#     print(clause_index)
#     w_l = 0
#     w_l_c = 0
#     if w_l_c == 0:
#         if clause_list[clause_index][w_l] == '?':
#             watched_literals[clause_index] = clause_list[clause_index][w_l]
#         w_l += 1
#         print(watched_literals)
#     elif w_l_c == 1:
#         if clause_list[clause_index][w_l] == '?':
#             watched_literals[clause_index] = clause_list[clause_index][w_l]
#         w_l += 1
#         print(watched_literals)



#print(len(clause_list[0]))
#watched_literals = [None] * len(clause_list)
#print(len(watched_literals[0]))
#print(watched_literals)
#print(len(watched_literals))
#print('yay')
# csize = len(clause_list)
# print(csize)
# len(watched_literals) = csize
# print(len_watched_literals)


    # while w_l_c < 2:
    #     print('yo')
        # if clause_list[clause_index][w_l] == '?':
        #     watched_literals[clause_index].append(clause_list[clause_index][w_l])
        #     w_l_c += 1
        # w_l += 1
        # print(watched_literals)


    # if watched_literals[clause_index] == None:
    #     print('yo')
    #     if clause_list[clause_index][w_l] == '?':
    #         watched_literals[clause_index] = clause_list[clause_index][w_l]
    #     w_l += 1
    #     print(watched_literals)


    # while len(watched_literals[clause_index]) < 2:
    #     print('yo')
    #     if clause_list[clause_index][w_l] == '?':      # Don't know if this part will work.
    #         watched_literals[clause_index][0] = clause_list[clause_index][w_l]         # This won't... the append is inappropriate
    #     w_l += 1




#
# blub = []
# blubb = [1, 2, [2, 3], 5]
# blubbb = [1, 5, 5]
#
# blubbb.insert(4, blubb[1])
# print(blubbb)
# #blubbb.replace(4, blubb[0])
# #print(blubbb)
# blubbb[3] = blubb[2]
# print(blubbb)
# #blubbb[1][0] = blubbb[0]
# blubbb.insert(1[1], blubbb[0])
# print(blubbb)

# thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
# print(thislist[2:5])
#
#
#
# my_list = ['p','r','o','b','e']
# # Output: p
# print(my_list[0:2])
#
# blub = ['1', '2', '5']
# blubb = [1, 2, [2, 3], 5]
# #print(blubb(1:2))
#
# ref = blubb[2][1]
# print(ref)
# refff = blubb[2][0]
# bla = []
# bla.append(blubb[1])
# print(bla)
# remove(bla[2])
# bla[2].append(blubb[1])
# print(bla)
# #print(refff)
#
# #ref = blub[2]
# #print(ref)
