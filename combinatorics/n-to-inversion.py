
# Appears to work!
def compute_jth_inversion(n, j):
    inversion = []
    for k in range(n, 1, -1):
        result = j % k
        inversion.append(result)
        j //= k

    inversion.append(0)
    return inversion


# l is the sequence length
# n is the number of choices for each trial
# j is the combination index to generate
def compute_jth_combination(l, n, j):
    combination = [None] * l
    for k in range(l - 1, -1, -1):
        combination[k] = j % n
        j //= n

    return combination


# Given a number, extract the permutation and combination elements
# Not working yet
def extract_constituents(total, sizes, n):
    constituents = []
    for s in sizes:
        constituents.append(n % s)
        n //= s

    return constituents

