# Heyhey this script is supposed to loop over first easy, then medium, difficult evil sudokus and put them all
# in nice lil output files. joy for all

from tkinter.filedialog import askdirectory
import tkinter.filedialog
import os
from iterative_dpll import iterative_dpll

d = tkinter.filedialog.askdirectory(initialdir='.')
fancy_output = open("fancy_output", "w")
heuristics = [1, 2, 3]

for subdir, dirs, files in os.walk(d):
    subdirname = subdir.split('/')
    subdirname = subdirname[-1]
    print('subdirrr', subdirname)
    for file in files:
        if file.endswith(".txt"):
            filepath = subdir + os.sep + file
            print(filepath)
            for heuristic in heuristics:
                iterative_dpll(subdirname, heuristic, filepath)

#
# for subdir, dirs, files in os.walk(d):
#     subdirname = os.path.split(subdir)[-1]
#     print('subdirrr', subdirname)
#     for file in files:
#         if not file.endswith(".txt"):
#             continue
#
#         filepath = os.path.join(subdir, file)
#         print(filepath)
#         for heuristic in heuristics:
#             iterative_dpll(subdirname, heuristic, filepath)
