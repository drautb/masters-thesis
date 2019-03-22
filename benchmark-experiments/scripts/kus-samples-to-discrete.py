import hashlib

solution_number = 1
sol_dict = {}
solutions = []
with open("stroop-3-kus-10000-samples.out", "r") as lines:
    for line in lines:
        line = line[line.index(', ') + 2:]
        sig = str(hashlib.md5(line.encode()).digest())

        if sig not in sol_dict:
            sol_dict[sig] = solution_number
            solution_number += 1

        solutions.append(sol_dict[sig])


with open("stroop-3-kus-10000-samples-discrete.out", "w") as out:
    out.write(' '.join(map(str, solutions)))
    out.write('\n')
