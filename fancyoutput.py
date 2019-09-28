# elaborate output..... aka N-backtracks and cl/v ratio per file

def fancyoutput(difficulty, filename, heuristic, benchmark, cv_ratio):
    fancy_output = open("fancy_output", "a")
    short_filename = filename.split("/")
    short_filename = short_filename[-1]
    fancy_output.write(difficulty + ' ' + short_filename + ' ' + str(heuristic) + ' ' + str(benchmark) + ' ' + str(cv_ratio) + '\n')

