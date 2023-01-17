import time
import random
from hw3 import test, sort_strings1, int_to_string

# k = 6
# inputs = [
#     [int_to_string(k, random.choice(range((5 ** k) - 1))) for i in range(10000)],
#     [int_to_string(k, random.choice(range((5 ** k) - 1))) for i in range(20000)],
#     [int_to_string(k, random.choice(range((5 ** k) - 1))) for i in range(30000)],
#     [int_to_string(k, random.choice(range((5 ** k) - 1))) for i in range(40000)],
# ]

# for l in inputs:
#     t0 =  time.perf_counter()
#     sort_lst = sort_strings1(l, k)
#     t1 =  time.perf_counter()

#     print("N: %d, runtime: %f seconds" % (len(l), t1 - t0))

test()


def sort_strings1_rec(lst, k):
    if len(lst) < 2 or k == 0:
        return lst
    
    digits = { 'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4 }
    lexico = [[] for i in range(len(digits))]
    sorted_list = []

    for w in lst:
        lexico[digits[w[-k]]].append(w)
    
    for i, l in enumerate(lexico):
        lexico[i] = sort_strings1(l, k-1)

    for l in lexico:
        sorted_list.extend(l)
    
    return sorted_list


# Q5 - E
def sort_strings2_loop(lst, k):
    if len(lst) < 2 or k == 0:
        return lst
    
    sorted_list = []
    lexico = [lst]
        
    for i in range(k):
        sub_lexico = []
        for words in lexico:
            if len(words) == 1:
                sub_lexico.append(words)

            else:
                lex_sort = [[] for i in range(5)]
                for w in words:
                    lex_sort[string_to_int(w[i])].append(w)

                for l in lex_sort:
                    if len(l) > 0:
                        sub_lexico.append(l)

        lexico = sub_lexico
    
    for l in lexico:
        sorted_list.extend(l)
    
    return sorted_list
