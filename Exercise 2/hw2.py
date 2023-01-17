# Skeleton file for HW2 - Winter 2022 - extended intro to CS

# Add your implementation to this file

# you may NOT change the signature of the existing functions.

# Change the name of the file to include your ID number (hw2_ID.py).

import random  # loads python's random module in order to use random.random() in question 2

##############
# QUESTION 1 #
##############


# 1a
def print_rectangle(length, width):
    rectangle = "*" * width + "\n"
    rectangle += ("*" + " " * (width-2) + "*\n") * (length-2)
    rectangle += "*" * width

    return rectangle


# 1b
def x_o_winner(board):
    sequences = [
        # Columns
        board[0][0] + board[1][0] + board[2][0],
        board[0][1] + board[1][1] + board[2][1],
        board[0][2] + board[1][2] + board[2][2],
        # Diagonals
        board[0][0] + board[1][1] + board[2][2],
        board[0][2] + board[1][1] + board[2][0]
    ]
    # Rows
    sequences.extend(board)

    if "xxx" in sequences:
        return "x"
    elif "ooo" in sequences:
        return "o"
    else:
        return "no winner"


# 1c
def valid_braces(s):
    opened = "([{"
    closed = ")]}"
    braces_type = {")": "(", "]": "[", "}": "{"}
    registry = ""

    for brace in s:
        if brace in opened:
            registry += brace

        elif brace in closed:
            if registry == "":
                return False
            if braces_type[brace] != registry[-1]:
                return False
            else:
                registry = registry[:-1]
                
    if registry != "":
        return False
    
    return True



##############
# QUESTION 2 #
##############


# 2a
def coin():
    toss = random.random()
    return True if toss < 0.5 else False


# 2b
def roll_dice(d):
    toss = random.random()
    return int(toss//(1/d) + 1)


# 2c
def roulette(bet_size, parity):
    roulette = roll_dice(37) - 1

    if roulette == 0:
        return 0
    
    elif roulette % 2 == 0 and parity == "even":
        return 2 * bet_size
    
    elif roulette % 2 == 1 and parity == "odd":
        return 2 * bet_size

    return 0


# 2d
def roulette_repeat(bet_size, n):
    balance = 0
    
    for i in range(n):
        parity = "even" if coin() else "odd"
        balance += (roulette(bet_size, parity) - bet_size)

    return balance


# 2e
def shuffle_list(lst):
    copy = lst[:]
    iterations = len(lst)
    permutation = []
    shuffled = []

    for i in range(iterations):
        location = roll_dice(iterations - i) - 1
        permutation.append(location)
        shuffled.append(copy[location])
        del copy[location]

    if iterations >= 2 and sum(permutation) == 0:
        return shuffle_list(lst)
    else:
        return shuffled


# 2f
def count_steps(d):
    steps = 0
    distance = 0
    is_distant = False

    if d == 0:
        return 0

    while not is_distant:
        steps += 1
        distance += 1 if coin() else (-1)
        is_distant = abs(distance) >= abs(d)
    
    return steps


def avg_count_steps(d):
    iterations = 2**12
    total_steps = 0

    for i in range(iterations):
        total_steps += count_steps(d)
    
    return total_steps / iterations

#2g
def count_steps_2dim(d):
    steps = 0
    location = 0 + 0j
    is_distant = False
    direction = {1: 1, 2: -1, 3: 1j, 4: -1j}

    if d == 0:
        return 0

    while not is_distant:
        steps += 1
        location += direction[roll_dice(4)]
        is_distant = abs(location) >= abs(d)
    
    return steps


##############
# QUESTION 3 #
##############


# 3a
def inc(binary):
    result = ""
    remainder = 1

    for b in binary[::-1]:
        if remainder == 1:
            result += '0' if b == '1' else '1'
            remainder = 0 if b == '0' else 1
        else:
            result += b
    
    result += '1' if remainder == 1 else ''
    
    return result[::-1]


# 3b
def add(bin1, bin2):
    result = ""
    remainder = 0
    overlap = min(len(bin1), len(bin2))
    bitwise = {
        ('0','0'): ('0', 0), ('1','0'): ('1', 0),
        ('1','1'): ('0', 1), ('0','1'): ('1', 0)
    }
    
    for i in range(overlap):
        bit, r1 = bitwise[(bin1[-i-1], bin2[-i-1])]
        bit, r2 = bitwise[(bit, str(remainder))]
        remainder = 0 if r1 == 0 and r2 == 0 else 1
        result += bit
    
    if len(bin1) > len(bin2):
        binary = bin1[:-overlap]
    else:
        binary = bin2[:-overlap]
    
    for b in binary[::-1]:
        if remainder == 1:
            result += '0' if b == '1' else '1'
            remainder = 0 if b == '0' else 1
        else:
            result += b

    result += '1' if remainder == 1 else ''

    return result[::-1]
    

# 3c
def pow_two(binary, power):
    if binary == '0':
        return '0'
    else:
        return binary + '0' * power


# 3d
def div_two(binary, power):
    if binary == '0':
        return '0'
    elif power > len(binary):
        return '0'
    else:
        return binary[0:-power]


# 3e
def leq(bin1, bin2):
    if len(bin1) != len(bin2):
        return True if len(bin1) < len(bin2) else False
    
    for i in range(len(bin1)):
        if bin1[i] != bin2[i]:
            return True if bin1[i] == '0' else False
    
    return True


# 3f
def to_decimal(binary):
    decimal = 0
    for p,b in enumerate(binary[::-1]):
        decimal += 2**p if b == '1' else 0
    
    return decimal


##############
# QUESTION 5 #
##############


# 5a
def divisors(n):
    return [d for d in range(1, n) if n % d == 0]


# 5b
def perfect_numbers(n):
    number = 1
    perfect = []

    while len(perfect) < n:
        if sum(divisors(number)) == number:
            perfect.append(number)
        number += 1
    
    return perfect


# 5c
def abundant_density(n):
    abundant_numbers = 0
    for number in range(1, n+1):
        if sum(divisors(number)) > number:
            abundant_numbers += 1
    
    return abundant_numbers/n


# 5e
def semi_perfect_3(n):
    numbers = divisors(n)
    options = len(numbers)

    if options < 3:
        return None
    
    for i in range(options-2):
        for j in range(i + 1, options-1):
            for k in range(j + 1, options):
                if (numbers[i] + numbers[j] + numbers[k]) == n:
                    return [numbers[i], numbers[j], numbers[k]]
    
    return None


##########
# Tester #
##########

def test():
    if print_rectangle(4, 5) != "*****\n*   *\n*   *\n*****" or \
       print_rectangle(3, 3) != "***\n* *\n***" or \
       print_rectangle(5, 4) != '****\n*  *\n*  *\n*  *\n****':
        print("#1a - error in print_rectangle")

    if x_o_winner(["eee", "xxx", "eoo"]) != "x" or \
       x_o_winner(["xee", "oxo", "eex"]) != "x" or \
       x_o_winner(["eex", "oxe", "xoe"]) != "x" or \
       x_o_winner(["oee", "oxx", "oeo"]) != "o" or \
       x_o_winner(["eee", "eee", "eeo"]) != "no winner":
        print("#1b - error in x_o_winner")

    if valid_braces("(ab{cd}ef)") is not True or \
       valid_braces("{this(is]wrong") is not False or \
       valid_braces("{1:(a,b),2:[c,d)}") is not False:
        print("#1c - error in valid_braces")

    for i in range(10):
        if coin() not in {True, False}:
            print("#2a - error in coin")
            break

    for i in range(10):
        if roll_dice(6) not in {1, 2, 3, 4, 5, 6}:
            print("2b - error in roll_dice")
            break

    for i in range(10):
        if (roulette(100, "even") not in {0, 200}) or (roulette(100, "odd") not in {0, 200}):
            print("2c - error in roulette")
            break

    if shuffle_list([1, 2, 3, 4]) == [1, 2, 3, 4] or \
       shuffle_list(["a", "b", "c", "d", "e"]) == ["a", "b", "c", "d", "e"] or \
       shuffle_list([(1, 2), (3, 4), ("a", "b")]) == [(1, 2), (3, 4), ("a", "b")]:
        print("2e - error in shuffle_list")

    if not 24 < avg_count_steps(5) < 26:  # very low probability that a good implementation will be out of this range
        print("2f - error in avg_count_steps")

    if count_steps_2dim(5) < 5:  # can't reach d in less than d steps
        print("2g - error in count_steps_2dim")

    if inc("0") != "1" or \
       inc("1") != "10" or \
       inc("101") != "110" or \
       inc("111") != "1000" or \
       inc(inc("111")) != "1001":
        print("3a - error in inc")

    if add("0", "1") != "1" or \
       add("1", "1") != "10" or \
       add("110", "11") != "1001" or \
       add("111", "111") != "1110":
        print("3b - error in add")

    if pow_two("10", 2) != "1000" or \
       pow_two("111", 3) != "111000" or \
       pow_two("101", 1) != "1010":
        print("3c - error in pow_two")

    if div_two("10", 1) != "1" or \
       div_two("101", 1) != "10" or \
       div_two("1010", 2) != "10" or \
       div_two("101010", 3) != "101":
        print("3c - error in div_two")

    if not leq("1010", "1010") or \
           leq("1010", "0") or \
           leq("1011", "1010"):
        print("3d - error in leq")

    if divisors(6) != [1, 2, 3] or divisors(7) != [1]:
        print("5a - error in divisors")

    if perfect_numbers(2) != [6, 28]:
        print("5b - error in perfect_numbers")

    if abundant_density(20) != 0.15:
        print("5c - error in adundant_density")

    if semi_perfect_3(18) != [3, 6, 9] or semi_perfect_3(20) is not None:
        print("5e - error in semi_perfect_3")