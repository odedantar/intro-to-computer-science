# Skeleton file for HW3 - Winter 2022 - extended intro to CS

# Add your implementation to this file

# You may add other utility functions to this file,
# but you may NOT change the signature of the existing ones.

# Change the name of the file to include your ID number (hw3_ID.py).
import math
import random

# Q2 - C
def bin_to_fraction(binary):
    fraction = 0

    for p, b in enumerate(binary): 
        fraction += 2**(-p - 1) if b == '1' else 0

    return fraction


# Q2 - D
bin_to_float = lambda binary: ((-1)**int(binary[0]) * 2**(int('0b' + binary[1:9], 2) - 127) * 
                                (1 + bin_to_fraction(binary[9:])))


# Q2 - E
def is_greater_equal(bin1, bin2):
    if bin1[0] != bin2[0]:
        return bin1[0] == '0'
    
    for i in range(1,32):
        if bin1[i] != bin2[i]:
            return bin1[i] == '1'
    
    return True


# Q3 - A
def approx_root(x, e):
    index = 1
    approx = 0
    product = 1
    naturals = []
    is_approximated = False
    
    if x == 0:
        return ([], 0)

    while not is_approximated:
        calculation = (approx + (1 / (product * index))) ** 2

        if calculation <= x:
            naturals.append(index)
            product *= index
            approx += 1 / product
        
        else:
            index += 1
        
        # Squaring this inquality holds becasue everything is positive:
        # sqrt(x) - approx <= e <--> sqrt(x) <= approx + e <--> x <= (approx + e) ** 2 
        is_approximated = x <= (approx + e) ** 2
    
    return (naturals, approx)


# Q3 - B
def approx_e(N):
    s = 0

    for i in range(N):
        s += one_sum_game()
    
    return s / N


def one_sum_game():
    s = 0
    n = 0
    
    while s < 1:
        s += random.random()
        n += 1
    
    return n


# Q4 - A
def find(lst, s):
    i = len(lst) // 2
    
    if len(lst) < 3:
        for k in range(len(lst)):
            if s == lst[k]:
                return k
        return None

    for k in range (-1,2):
        if s == lst[i+k]:
            return i+k
    
    median = get_median(lst[i-1], lst[i], lst[i+1])

    if s < median:
        return find(lst[:i], s)
    if s > median:
        loc = find(lst[i+1:], s)
        return loc + (i + 1) if loc != None else None
    
    return None


def get_median(a, b, c):
    r = b
    mn = min([a, b, c])
    mx = max([a, b, c])
    
    if mn < a and a < mx:
        r = a
    if mn < c and c < mx:
        r = c
    
    return r


# Q4 - B
def sort_from_almost(lst):
    if len(lst) < 2 :
        return lst
    
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1]:
            lst[i], lst[i+1] = lst[i+1], lst[i]
    
    return lst
    

# Q4 - C
def find_local_min(lst):
    if len(lst) < 2:
        return 0 if len(lst) == 1 else None
    
    if lst[0] <= lst[1]:
        return 0
    if lst[-2] >= lst[-1]:
        return len(lst) - 1

    for i in range(1, len(lst) - 1):
        if lst[i-1] >= lst[i] and lst[i] <= lst[i+1]:
            return i


# Q5 - A
def string_to_int(s):
    digits = { 'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4 }
    decimal = 0

    for p, d in enumerate(s[::-1]):
        decimal += digits[d] * (5 ** p)
    
    return decimal


# Q5 - B
def int_to_string(k, n):
    chars = ['a', 'b', 'c', 'd', 'e']
    s = ""

    for p in range(k-1, -1, -1):
        s += chars[n // (5 ** p)]
        n -= (n // (5 ** p)) * (5 ** p)
    
    return s


# Q5 - C
def sort_strings1(lst, k):
    indexes = [0] * (5 ** k)
    ordered = []

    for s in lst:
        indexes[string_to_int(s)] += 1
    
    for i, n in enumerate(indexes):
        if i > 0:
            ordered.extend([int_to_string(k, i)] * n)

    return ordered


# Q5 - E
def sort_strings2(lst, k):
    ordered = []

    for i in range(5 ** k):
        for s in lst:
            if string_to_int(s) == i:
                ordered.append(s)
    
    return ordered


##########
# Tester #
##########
def test():
    # Q2 - C
    if bin_to_fraction('01101') != 0.40625 or bin_to_fraction('1010000') != 0.625:
        print('error in bin_to_fraction')
    # Q2 - D
    if bin_to_float('00111110001000000000000000000000') != 0.15625:
        print("error in bin_to_float")
    # Q2 - E
    if is_greater_equal('00111110001000000000000000000000', '00111111001000000000000000000000') == True or \
       is_greater_equal('00111110001000000000000000000000', '00111110001000000000000000000000') == False:
        print("error in is_greater_equal")
    # Q3 - A
    if approx_root(2, 0.1) != ([1, 3], 1 + 1/3):
        print("error in approx_root (1)")
    if approx_root(2, 0.02) != ([1, 3, 5], 1 + 1/3 + 1/15):
        print("error in approx_root (2)")
    if approx_root(2, 0.001) != ([1, 3, 5, 5], 1 + 1/3 + 1/15 + 1/75):
        print("error in approx_root (3)")
    # Q3 - B
    if abs(approx_e(1000000) - math.e) > 0.01:
        print("MOST LIKELY there's an error in approx_e (this is a probabilistic test)")

    # Q4 - A
    almost_sorted_lst = [2, 1, 3, 5, 4, 7, 6, 8, 9]
    if find(almost_sorted_lst, 5) != 3:
        print("error in find")
    if find(almost_sorted_lst, 6) != 6:
        print("error in find")
    if find(almost_sorted_lst, 50) != None:
        print("error in find")
    # Q4 - B
    if sort_from_almost(almost_sorted_lst) != sorted(almost_sorted_lst):
        print("error in sort_from_almost")
    # Q4 - C
    lst = [5, 6, 7, 5, 1, 1, 99, 100]
    pos = find_local_min(lst)
    if pos not in (0, 4, 5):
        print("error in find_local_min")

    # Q5
    lst_num = [random.choice(range(5 ** 4)) for i in range(15)]
    for i in lst_num:
        s = int_to_string(4, i)
        if s is None or len(s) != 4:
            print("error in int_to_string")
        if string_to_int(s) != i:
            print("error in int_to_string and/or in string_to_int")

    lst1 = ['aede', 'adae', 'dded', 'deea', 'cccc', 'aacc', 'edea', 'becb', 'daea', 'ccea']
    if sort_strings1(lst1, 4) \
            != ['aacc', 'adae', 'aede', 'becb', 'cccc', 'ccea', 'daea', 'dded', 'deea', 'edea']:
        print("error in sort_strings1")

    if sort_strings2(lst1, 4) \
            != ['aacc', 'adae', 'aede', 'becb', 'cccc', 'ccea', 'daea', 'dded', 'deea', 'edea']:
        print("error in sort_strings2")