import re

solution_number = 1
solutions = []
with open("stroop-3-spur-10000-samples.out", "r") as lines:
    for line in lines:
        matches = re.findall(r"^(\d+),", line)
        if not matches:
            continue

        count = matches[0]
        for n in range(int(count)):
            solutions.append(solution_number)
        solution_number += 1

with open("stroop-3-spur-10000-samples-discrete.out", "w") as out:
    out.write(' '.join(map(str, solutions)))
    out.write('\n')
