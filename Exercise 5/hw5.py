# Skeleton file for HW5 - Spring 2021 - extended intro to CS

# Add your implementation to this file

# you may NOT change the signature of the existing functions.

# Change the name of the file to include your ID number (hw5_ID.py).

import random
import math

from numpy import right_shift

##############
# QUESTION 2 #
##############


def is_sorted(lst):
    """ returns True if lst is sorted, and False otherwise """
    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            return False
    return True


def modpower(a, b, c):
    """ computes a**b modulo c, using iterated squaring """
    result = 1
    while b > 0:  # while b is nonzero
        if b % 2 == 1:  # b is odd
            result = (result * a) % c
        a = (a * a) % c
        b = b // 2
    return result


def is_prime(m):
    """ probabilistic test for m's compositeness """
    for i in range(0, 100):
        a = random.randint(1, m - 1)  # a is a random integer in [1...m-1]
        if modpower(a, m - 1, m) != 1:
            return False
    return True


def merge_sorted(I, J):
    """ merge sorted lists in orderly fashion """
    i, j = 0, 0
    merged = []

    while i < len(I) and j < len(J):
        if I[i] < J[j]:
            merged.append(I[i])
            i += 1
        else:
            merged.append(J[j])
            j += 1

    merged.extend(I[i:])
    merged.extend(J[j:])

    return merged


class FactoredInteger:

    def __init__(self, factors, verify=True):
        """ Represents an integer by its prime factorization """
        if verify:
            assert is_sorted(factors)
        number = 1
        for p in factors:
            if verify:
                assert (is_prime(p))
            number *= p
        self.number = number
        self.factors = factors

    # 2b
    def __repr__(self):
        return ('<%d:%s>' % (self.number ,'*'.join([str(p) for p in self.factors])))

    def __eq__(self, other):
        return self.number == other.number

    def __mul__(self, other):
        return FactoredInteger(
            merge_sorted(self.factors, other.factors),
            verify=False
        )

    def __pow__(self, other):
        factors = []
        for p in self.factors:
            factors.extend([p]*other.number)
        
        return FactoredInteger(
            factors,
            verify=False
        )

    # 2c
    def gcd(self, other):
        i, j = 0, 0
        factors = []
        s_f, o_f = self.factors, other.factors

        while i < len(s_f) and j < len(o_f):
            if s_f[i] < o_f[j]:
                i += 1
            elif s_f[i] > o_f[j]:
                j += 1
            elif s_f[i] == o_f[j]:
                factors.append(s_f[i])
                i, j = i + 1, j + 1
        
        return FactoredInteger(factors, verify=False)

    # 2d
    def lcm(self, others):
        my_set = set()
        lists = [self.factors] + [x.factors for x in others]
        f_i_d = [{f: 0 for f in x} for x in lists]

        for i in range(len(lists)):
            for f in lists[i]:
                my_set.add(f)
                f_i_d[i][f] += 1
        
        f_m_d = {x: 0 for x in my_set}
        
        for f_d in f_i_d:
            for f in f_d.keys():
                if f_d[f] > f_m_d[f]:
                    f_m_d[f] = f_d[f]
        
        result = []
        
        for k, v in f_m_d.items():
            result += [k] * v
        
        return FactoredInteger(result, verify=False)


##############
# QUESTION 3 #
##############

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = math.sqrt(x ** 2 + y ** 2)
        self.theta = math.atan2(y, x)
        if self.theta < 0:
            self.theta += 2 * math.pi

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    # 3a_i
    def angle_between_points(self, other):
        angle = other.theta - self.theta
        if angle < 0:
            angle += 2 * math.pi
        
        return angle


# 3a_ii
def find_optimal_angle(trees, alpha):
    thetas = [(t.theta, i) for i,t in enumerate(trees)]
    thetas = sort_thetas(thetas, 0, len(thetas))
    
    extra_lap = []
    for i in range(len(thetas) - 1):
        extra_lap.append((thetas[i][0] + 2 * math.pi, thetas[i][1]))
    
    thetas.extend(extra_lap)

    max_trees = 0
    max_point = thetas[0]
    length = len(thetas) - len(extra_lap)
    
    for i in range(length):
        value = thetas[i][0] + alpha
        bound_index = find_theta_bound(thetas, value, i, i + length)

        if bound_index - i > max_trees:
            max_trees = bound_index - i
            max_point = thetas[i]
    
    view = Point(0,0)
    return view.angle_between_points(trees[max_point[1]])


def merge_thetas(t1, t2):
    """ merge sorted lists of tuples in orderly fashion """
    i, j = 0, 0
    merged = []

    while i < len(t1) and j < len(t2):
        if t1[i][0] < t2[j][0]:
            merged.append(t1[i])
            i += 1
        else:
            merged.append(t2[j])
            j += 1

    merged.extend(t1[i:])
    merged.extend(t2[j:])
    
    return merged


def sort_thetas(thetas, start, end):
    """ recursive mergesort """
    length = end - start
    
    if length <= 1:
        return [thetas[start]]
    else:
        split = start + length//2
        return merge_thetas(sort_thetas(thetas, start, split) ,
                            sort_thetas(thetas, split, end))


def find_theta_bound(thetas, value, start, end):
    """ recursive binary search """
    length = end - start
    
    if length <= 1:
        return start
    else:
        split = start + length//2
        
        if value < thetas[split][0]:
            return find_theta_bound(thetas, value, start, split)
        else:
            return find_theta_bound(thetas, value, split, end)


class Node:
    def __init__(self, val):
        self.value = val
        self.next = None

    def __repr__(self):
        # return str(self.value)
        # This shows pointers as well for educational purposes:
        return "(" + str(self.value) + ", next: " + str(id(self.next)) + ")"


class Linked_list:
    def __init__(self, seq=None):
        self.head = None
        self.len = 0
        if seq != None:
            for x in seq[::-1]:
                self.add_at_start(x)

    def __repr__(self):
        out = ""
        p = self.head
        while p != None:
            out += str(p) + ", "  # str(p) invokes __repr__ of class Node
            p = p.next
        return "[" + out[:-2] + "]"

    def __len__(self):
        ''' called when using Python's len() '''
        return self.len

    def add_at_start(self, val):
        ''' add node with value val at the list head '''
        tmp = self.head
        self.head = Node(val)
        self.head.next = tmp
        self.len += 1

    def find(self, val):
        ''' find (first) node with value val in list '''
        p = self.head
        # loc = 0     # in case we want to return the location
        while p != None:
            if p.value == val:
                return p
            else:
                p = p.next
                # loc=loc+1   # in case we want to return the location
        return None

    def __getitem__(self, loc):
        ''' called when using L[i] for reading
            return node at location 0<=loc<len '''
        assert 0 <= loc < len(self)
        p = self.head
        for i in range(0, loc):
            p = p.next
        return p

    def __setitem__(self, loc, val):
        ''' called when using L[loc]=val for writing
            assigns val to node at location 0<=loc<len '''
        assert 0 <= loc < len(self)
        p = self.head
        for i in range(0, loc):
            p = p.next
        p.value = val
        return None

    def insert(self, loc, val):
        ''' add node with value val after location 0<=loc<len of the list '''
        assert 0 <= loc <= len(self)
        if loc == 0:
            self.add_at_start(val)
        else:
            p = self.head
            for i in range(0, loc - 1):
                p = p.next
            tmp = p.next
            p.next = Node(val)
            p.next.next = tmp
            self.len += 1

    def delete(self, loc):
        ''' delete element at location 0<=loc<len '''
        assert 0 <= loc < len(self)
        if loc == 0:
            self.head = self.head.next
        else:
            p = self.head
            for i in range(0, loc - 1):
                p = p.next
            # p is the element BEFORE loc
            p.next = p.next.next
        self.len -= 1


class Segment:
    def __init__(self, p1, p2):
        self.point1 = p1
        self.point2 = p2

    def intersecting(self, other):
        if (self.point1.x - self.point2.x) == 0:
            return False
        if (other.point1.x - other.point2.x) == 0:
            return False
        self_incline = (self.point1.y - self.point2.y) / (self.point1.x - self.point2.x)
        other_incline = (other.point1.y - other.point2.y) / (other.point1.x - other.point2.x)
        self_b = self.point1.y - self_incline * self.point1.x
        other_b = other.point1.y - other_incline * other.point1.x
        if (self_incline - other_incline) == 0:
            return False
        intersecting_x = (other_b - self_b) / (self_incline - other_incline)
        if ((intersecting_x <= max(min(self.point1.x, self.point2.x), min(other.point1.x, other.point2.x))) or
                (intersecting_x >= min(max(self.point1.x, self.point2.x), max(other.point1.x, other.point2.x)))):
            return False
        else:
            return True


# for 3b_ii
def calculate_angle(p1, p2, p3):
    ang = math.degrees(math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x))
    return ang + 360 if ang < 0 else ang


class Polygon:
    def __init__(self, llist):
        self.points_list = llist
        self.point_head = llist.head

    # 3b_ii
    def edges(self):
        angles = []
        point_count = 1
        prev = self.point_head

        if prev == None:
            return angles
        
        while prev.next != None:
            point_count += 1
            prev = prev.next
        
        edge = self.point_head

        if edge == prev:
            return angles

        while edge.next != None:
            angles.append(calculate_angle(prev.value, edge.value, edge.next.value))
            prev = edge
            edge = edge.next

        angles.append(calculate_angle(prev.value, edge.value, self.point_head.value))

        total = sum(angles)

        if total != 180 * (point_count - 2):
            angles = [360 - a for a in angles]

        return angles

    # 3b_iii
    def simple(self):
        edge = self.point_head
        
        if edge == None:
            return True
        
        if edge.next == None:
            return True

        while edge.next != None:
            p = self.point_head
            s = Segment(edge.value, edge.next.value)

            while p.next != None:
                is_neighbor = p == edge or p.next == edge.next or \
                              p == edge.next or p.next == edge

                if not is_neighbor:
                    if s.intersecting(Segment(p.value, p.next.value)):
                        return False
                
                p = p.next

            if s.intersecting(Segment(p.value, self.point_head.value)):
                return False
            
            edge = edge.next
        
        p = self.point_head
        s = Segment(edge.value, self.point_head.value)

        while p.next != None:
            is_neighbor = p == edge or p.next == edge.next or \
                          p == edge.next or p.next == edge

            if not is_neighbor:
                if s.intersecting(Segment(p.value, p.next.value)):
                    return False
            p = p.next
        
        return True


##############
# QUESTION 4 #
##############


def printree(t, bykey=True):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    # for row in trepr(t, bykey):
    #        print(row)
    return trepr(t, bykey)


def trepr(t, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if t == None:
        return ["#"]

    thistr = str(t.key) if bykey else str(t.val)

    return conc(trepr(t.left, bykey), thistr, trepr(t.right, bykey))


def conc(left, root, right):
    """Return a concatenation of textual represantations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result


def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1


def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i


class Tree_node():
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return "(" + str(self.key) + ":" + str(self.val) + ")"


class Binary_search_tree():

    def __init__(self):
        self.root = None

    def __repr__(self):  # no need to understand the implementation of this one
        out = ""
        for row in printree(self.root):  # need printree.py file
            out = out + row + "\n"
        return out

    def inorder(self):
        result = []

        def inorder_rec(root):
            if root:
                inorder_rec(root.left)
                result.append((root.key, root.val))
                inorder_rec(root.right)

        inorder_rec(self.root)
        return result

    def lookup(self, key):
        ''' return node with key, uses recursion '''

        def lookup_rec(node, key):
            if node == None:
                return None
            elif key == node.key:
                return node
            elif key < node.key:
                return lookup_rec(node.left, key)
            else:
                return lookup_rec(node.right, key)

        return lookup_rec(self.root, key)

    def insert(self, key, val):
        ''' insert node with key,val into tree, uses recursion '''

        def insert_rec(node, key, val):
            if key == node.key:
                node.val = val  # update the val for this key
            elif key < node.key:
                if node.left == None:
                    node.left = Tree_node(key, val)
                else:
                    insert_rec(node.left, key, val)
            else:  # key > node.key:
                if node.right == None:
                    node.right = Tree_node(key, val)
                else:
                    insert_rec(node.right, key, val)
            return

        if self.root == None:  # empty tree
            self.root = Tree_node(key, val)
        else:
            insert_rec(self.root, key, val)

    # 4a
    def diam(self):
        ''' calculate tree diameter, uses recursion '''

        def depth_rec(t_node, diameter = 0):
            if t_node == None:
                return (0, 0)
            
            left_depth, left_diam = depth_rec(t_node.left, diameter)
            right_depth, right_diam = depth_rec(t_node.right, diameter)

            current_diam = 1 + left_depth + right_depth
            diameter = max(current_diam, left_diam, right_diam)

            return (1 + max(left_depth, right_depth), diameter)

        return depth_rec(self.root)[1]

    # 4b
    def cumsum(self):
        def cumsum_rec(t_node, appendix=''):
            if t_node == None:
                return appendix
            
            key = cumsum_rec(t_node.left, appendix)
            t_node.key = key + t_node.key
            return cumsum_rec(t_node.right, t_node.key)
        
        cumsum_rec(self.root)


############
# QUESTION 5
############

# 5a
def prefix_suffix_overlap(lst, k):
    overlap = []

    for i, si in enumerate(lst):
        for j, sj in enumerate(lst):
            if i != j and si[:k] == sj[-k:]:
                overlap.append((i,j))
    
    return overlap


# 5c
class Dict:
    def __init__(self, m, hash_func=hash):
        """ initial hash table, m empty entries """
        self.table = [[] for i in range(m)]
        self.hash_mod = lambda x: hash_func(x) % m

    def __repr__(self):
        L = [self.table[i] for i in range(len(self.table))]
        return "".join([str(i) + " " + str(L[i]) + "\n" for i in range(len(self.table))])

    def insert(self, key, value):
        """ insert key,value into table
            Allow repetitions of keys """
        i = self.hash_mod(key)  # hash on key only
        item = [key, value]  # pack into one item
        self.table[i].append(item)

    def find(self, key):
        """ returns ALL values of key as a list, empty list if none """
        i = self.hash_mod(key)
        values = [item[1] for item in self.table[i] if key == item[0]]
        return values 


# 5d
def prefix_suffix_overlap_hash1(lst, k):
    overlap = []
    reisha = Dict(2 * len(lst))

    for i, s in enumerate(lst):
        reisha.insert(s[:k], i)
    
    for j, s in enumerate(lst):
        matches = reisha.find(s[-k:])
        for i in matches:
            if i != j and s[-k:] == lst[i][:k]:
                overlap.append((i,j))
    
    return overlap


##########
# TESTER #
##########

def test():
    ##############
    # QUESTION 2 #
    #   TESTER   #
    ##############

    # 2b
    n1 = FactoredInteger([2, 3])  # n1.number = 6
    n2 = FactoredInteger([2, 5])  # n2.number = 10
    n3 = FactoredInteger([2, 2, 3, 5])  # n3.number = 60
    if str(n3) != "<60:2*2*3*5>":
        print("2b - error in __repr__")
    if n1 != FactoredInteger([2, 3]):
        print("2b - error in __eq__")
    if n1 * n2 != n3:
        print("2b - error in __mult__")
    if n1 ** n2 != FactoredInteger([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]):
        print("2b - error in __pow__")

    # 2c
    n4 = FactoredInteger([2, 2, 3])  # n4.number = 12
    n5 = FactoredInteger([2, 2, 2])  # n5.number = 8
    n6 = FactoredInteger([2, 2])  # n6.number = 4
    if n4.gcd(n5) != n6:
        print("2c - error in gcd")

    n7 = FactoredInteger([2, 3])  # n7.number = 6
    n8 = FactoredInteger([5, 7])  # n8.number = 35
    n9 = FactoredInteger([])  # represents 1
    if n7.gcd(n8) != n9:
        print("2c - error in gcd")

    ##############
    # QUESTION 3 #
    #   TESTER   #
    ##############

    # 3a
    p1 = Point(1, 1)  # theta = pi / 4
    p2 = Point(0, 3)  # theta = pi / 2
    if Point.angle_between_points(p1, p2) != 0.25 * math.pi or \
            Point.angle_between_points(p2, p1) != 1.75 * math.pi:
        print("3a_i - error in angle_between_points")

    trees = [Point(2, 1), Point(-1, 1), Point(-1, -1), Point(0, 3), Point(0, -5), Point(-1, 3)]
    if find_optimal_angle(trees, 0.25 * math.pi) != 0.5 * math.pi:
        print("3a_ii - error in find_optimal_angle")

    # 3b
    def test_angles(target, output):
        if len(target) != len(output):
            print("3a_ii - error in Polygon.edges")
        for i in range(len(target)):
            if abs(target[i] - output[i]) >= 0.1:  # dealing with floats
                print("3a_ii - error in Polygon.edges")

    parallelogram = Polygon(Linked_list([Point(1, 1), Point(4, 4), Point(8, 4),Point(5, 1)]))
    test_angles(parallelogram.edges(), [45.0, 135.0, 45.0, 135.0])
    other_poly = Polygon(Linked_list([Point(1, 1), Point(1, 3), Point(2, 3), Point(3, 1)]))
    test_angles(other_poly.edges(), [90.0, 90.0, 116.5, 63.4])
    not_simple = Polygon(Linked_list([Point(1, 1),Point(8, 4),Point(4, 4),Point(5, 1)]))

    if not_simple.simple():
        print("3a_iii - error in Polygon.simple")
    if not parallelogram.simple():
        print("3a_iii - error in Polygon.simple")
    if not other_poly.simple():
        print("3a_iii - error in Polygon.simple")

    ##############
    # QUESTION 4 #
    #   TESTER   #
    ##############

    # 4a
    t2 = Binary_search_tree()
    t2.insert('c', 10)
    t2.insert('a', 10)
    t2.insert('b', 10)
    t2.insert('g', 10)
    t2.insert('e', 10)
    t2.insert('d', 10)
    t2.insert('f', 10)
    t2.insert('h', 10)
    if t2.diam() != 6:
        print("4a - error in diam")

    t3 = Binary_search_tree()
    t3.insert('c', 1)
    t3.insert('g', 3)
    t3.insert('e', 5)
    t3.insert('d', 7)
    t3.insert('f', 8)
    t3.insert('h', 6)
    t3.insert('z', 6)
    if t3.diam() != 5:
        print("4a - error in diam")

    # 4b
    t3.cumsum()
    if str(t3.inorder()) != "[('c', 1), ('cd', 7), ('cde', 5), ('cdef', 8), ('cdefg', 3), ('cdefgh', 6), ('cdefghz', 6)]":
        print("4b - error in cumsum")
    t2.cumsum()
    if str(t2.inorder()) != "[('a', 10), ('ab', 10), ('abc', 10), ('abcd', 10), ('abcde', 10), ('abcdef', 10), ('abcdefg', 10), ('abcdefgh', 10)]":
        print("4b - error in cumsum")

    ##############
    # QUESTION 5 #
    #   TESTER   #
    ##############
    # 5a
    lst = ["abcd", "cdab", "aaaa", "bbbb", "abff"]
    k = 2
    if sorted(prefix_suffix_overlap(lst, k)) != sorted([(0, 1), (1, 0), (4, 1)]):
        print("error in prefix_suffix_overlap")

    # 5c
    d = Dict(3)
    d.insert("a", 56)
    d.insert("a", 34)
    if sorted(d.find("a")) != sorted([56, 34]) or d.find("b") != []:
        print("error in Dict.find")

    # 5d
    lst = ["abcd", "cdab", "aaaa", "bbbb", "abff"]
    k = 2
    if sorted(prefix_suffix_overlap_hash1(lst, k)) != sorted([(0, 1), (1, 0), (4, 1)]):
        print("error in prefix_suffix_overlap_hash1")