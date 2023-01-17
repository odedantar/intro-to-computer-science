from hw2 import test
from hw2 import semi_perfect_3
import time

def add(bin1, bin2):
    bitwise = {
        ('0','0'): ('0', '0'), ('1','0'): ('1', '0'),
        ('1','1'): ('0', '1'), ('0','1'): ('1', '0')
    }
    
    length = max(len(bin1), len(bin2))
    binary1 = '0' * (length - len(bin1)) + bin1
    binary2 = '0' * (length - len(bin2)) + bin2
    result = ""
    remainder = ""

    for i in range(length):
        b, r = bitwise[(binary1[-i-1], binary2[-i-1])]
        remainder += r
        result += b
    
    result = result[::-1]
    remainder = remainder[::-1] + '0'
    remainder = remainder[1:] if remainder[0] == '0' else remainder
    
    if '1' in remainder:
        return add(result, remainder)
    else:
        return result

# t0 =  time.perf_counter()
# perfect_numbers(3)
# t1 =  time.perf_counter()
# print ('time elapsed: %f seconds' % (t1 - t0))

# t0 =  time.perf_counter()
# perfect_numbers(4)
# t1 =  time.perf_counter()
# print ('time elapsed: %f seconds' % (t1 - t0))

# intervals = [50, 500, 5000]
# for n in intervals:
#     density = abundant_density(n)
#     print('Density in [0, %d]:\t%f %% ' % (n, density * 100))

print(semi_perfect_3(0))

test()