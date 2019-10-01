# elaborate output..... aka N-backtracks and cl/v ratio per file

def fancyoutput(difficulty, filename, heuristic, benchmark, cv_ratio, cv2_ratio, cv3_ratio):
    fancy_output = open("fancy_output", "a")
    short_filename = filename.split("\\")
    short_filename = short_filename[-1]
    fancy_output.write(short_filename + ',' + difficulty + ',' + str(heuristic) + ',' + str(benchmark) + ',' + str(cv_ratio) + ',' + str(cv2_ratio) + ',' + str(cv3_ratio) + '\n')

