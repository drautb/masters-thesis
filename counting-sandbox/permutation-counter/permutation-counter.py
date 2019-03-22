from itertools import permutations

def is_sublist(l, s):
    sub_set = False
    if s == []:
        sub_set = True
    elif s == l:
        sub_set = True
    elif len(s) > len(l):
        sub_set = False

    else:
        for i in range(len(l)):
            if l[i] == s[0]:
                n = 1
                while (i+n < len(l) and n < len(s)) and (l[i+n] == s[n]):
                    n += 1

                if n == len(s):
                    sub_set = True

    return sub_set


l = 6
k = 2
v = 3

sequence = v * '1' + ((l - v) * '0')

unique_permutations = set(permutations(sequence))
print("Unique Perms: " + str(len(unique_permutations)))

permutations_with_at_least_k = []
for p in unique_permutations:
    if is_sublist(list(p), list(k * '1')):
        permutations_with_at_least_k.append(p)

print(len(permutations_with_at_least_k))
for p in permutations_with_at_least_k:
    print(str(p))