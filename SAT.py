import sys
import os.path


if __name__ == "__main__":

    # read the commandline args ("SAT -Sn clausefile+puzzlefile")

    # ensure correct usage
    if len(sys.argv) != 3:
        print("usage: SAT.py -Sn clause_file+start_values_file")
        exit(1)

    # ensure the strategy number is valid
    n_strategy = int(sys.argv[1][-1])
    if n_strategy < 1 or n_strategy > 3:
        print("usage: pick 1, 2, or 3 as strategy number, ex. -S1")
        exit(1)

    # parse the concatenation and ensure the files exist
    files = sys.argv[2].split("+")

    for file in files:
        if not os.path.isfile(file):
            # does the below also filter out empty files?
            print("{} does not exist".format(file))
            exit(1)

    clauses_file = files[0]
    start_values_file = files[1]

    print("mlep")

    # create a sat object and read in the files

