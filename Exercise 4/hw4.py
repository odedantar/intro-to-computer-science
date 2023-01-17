# Skeleton file for HW4 - Winter 2022 - extended intro to CS

# Add your implementation to this file

# You may add other utility functions to this file,
# but you may NOT change the signature of the existing ones.

# Change the name of the file to include your ID number (hw4_ID.py).

def winnable_mem(board):
    d = {}
    return winnable_mem_rec(board, d)


# 1c
def winnable_mem_rec(board, d):
    key = tuple(board)
    if key in d:
        return d[key]
    
    if sum(board) == 0:
        return True

    m = len(board)
    for i in range(m):
        for j in range(board[i]):
            munched_board = board[0:i] + [min(board[k], j) for k in range(i, m)]
            
            is_win = winnable_mem_rec(munched_board, d)
            d[tuple(munched_board)] = is_win

            if not is_win:
                return True
    
    return False 


# 2a
def H_local(n, i, j):
    if n <= 1:
        return i and j

    power = 2 ** (n - 1)
    is_i, is_j = (i >= power), (j >= power)
    is_inverse = (is_i and is_j)

    normal_i = i - power if is_i else i
    normal_j = j - power if is_j else j

    if is_inverse:
        return 1 - H_local(n - 1, normal_i, normal_j)
    
    return H_local(n - 1, normal_i, normal_j)


# 2c
H_complete = lambda n: [ [ H_local(n, i, j) for j in range(2**n) ] for i in range(2**n) ]


# 3a
def can_create_once(s, L):
    if len(L) == 0:
        return s == 0
    
    element = L.pop()
    is_summable = (can_create_once(s - element, L) or 
                   can_create_once(s + element, L))
    L.append(element)

    return is_summable


# 3b
def can_create_twice(s, L):
    if len(L) == 0:
        return s == 0
    
    element = L.pop()
    is_summable = (can_create_twice(s - element, L) or 
                   can_create_twice(s + element, L) or
                   can_create_twice(s - (2 * element), L) or
                   can_create_twice(s + (2 * element), L))
    L.append(element)

    return is_summable


# 3c
def valid_braces_placement(s, L):
    expression = [str(e) for e in L]

    calc = valid_braces_calc(expression)

    return s in calc


def valid_braces_calc(L):
    calc = set()

    if len(L) <= 3:
        return { eval(''.join(L)) }

    for i in range(1, len(L), 2):
        lhs = valid_braces_calc(L[:i])
        rhs = valid_braces_calc(L[i+1:])
        
        for a in lhs:
            for b in rhs:
                calc.add( eval('%d %s %d' % (a, L[i], b)) )
    
    return calc


# 4a
def grid_escape1(B):
    if len(B) == 0:
        return False
    
    if len(B[0]) == 0:
        return False

    return grid_escape1_rec(B, 0, 0)


def grid_escape1_rec(B, i, j):
    rows = len(B) - 1 
    cols = len(B[0]) - 1

    if i > rows or j > cols:
        return False
    
    if i == rows and j == cols:
        return True
    
    step = B[i][j]

    if step == 0:
        return False
    
    return (grid_escape1_rec(B, i + step, j) or 
            grid_escape1_rec(B, i, j + step))


# 4b
def grid_escape2(B):
    if len(B) == 0:
        return False

    if len(B[0]) == 0:
        return False

    return grid_escape2_rec(B, 0, 0, set())


def grid_escape2_rec(B, i, j, s):
    rows = len(B) - 1 
    cols = len(B[0]) - 1

    if (i,j) in s:
        return False

    if i > rows or j > cols or i < 0 or j < 0:
        return False

    if i == rows and j == cols:
        return True
    
    s.add((i,j))
    step = B[i][j]
    
    if step == 0:
        return False
    
    return (grid_escape2_rec(B, i + step, j, s) or 
            grid_escape2_rec(B, i - step, j, s) or
            grid_escape2_rec(B, i, j + step, s) or
            grid_escape2_rec(B, i, j - step, s))



##########
# Tester #
##########
def test():
    # 1c
    if winnable_mem([5, 5, 3]) or not winnable_mem([5, 5, 5]):
        print("error in winnable_mem")
    # 2a
    if H_local(2,2,2) != 1:
        print("error in H_local")
    # 2c
    if H_complete(1) != [[0,0],[0,1]]:
        print("error in H_complete")
    # 3a
    if not can_create_once(6, [5, 2, 3]) or not can_create_once(-10, [5, 2, 3]) \
            or can_create_once(9, [5, 2, 3]) or can_create_once(7, [5, 2, 3]):
        print("error in can_create_once")
    # 3b
    if not can_create_twice(6, [5, 2, 3]) or not can_create_twice(9, [5, 2, 3]) \
        or not can_create_twice(7, [5, 2, 3]) or can_create_once(19, [5, 2, 3]):
        print("error in can_create_twice")
    # 3c
    L = [6, '-', 4, '*', 2, '+', 3]
    if not valid_braces_placement(10, L) or not valid_braces_placement(1, L) or valid_braces_placement(5, L):
        print("error in valid_braces_placement")

    B1 = [[1, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 1, 2]]
    B2 = [[2, 3, 1, 2], [2, 2, 2, 2], [2, 2, 3, 2], [2, 2, 2, 2]]
    B3 = [[2, 1, 2, 1], [1, 2, 1, 1], [2, 2, 2, 2], [4, 4, 4, 4]]

    # 4a
    if grid_escape1(B1) is False:
        print("error in grid_escape1 - B1")
    if grid_escape1(B2) is True:
        print("error in grid_escape1 - B2")
    if grid_escape1(B3) is True:
        print("error in grid_escape1 - B3")

    # 4b
    if grid_escape2(B1) is False:
        print("error in grid_escape2 - B1")
    if grid_escape2(B2) is False:
        print("error in grid_escape2 - B2")
    if grid_escape2(B3) is True:
        print("error in grid_escape2 - B3")