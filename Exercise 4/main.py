import time
from hw4 import test, can_create_once


def performance(func, reference):
    inputs = [[5]*2, [5]*4, [5]*8]

    for l in inputs:
        t0 =  time.perf_counter()
        reference(l)
        t1 =  time.perf_counter()
        ref_time = t1 - t0

        t0 =  time.perf_counter()
        func(l)
        t1 =  time.perf_counter()
        func_time = t1 - t0

        print("Input: %s \nMem time: \t%f sec \nRegular time: \t%f sec \n"
            % (str(l),ref_time, func_time))

# performance(min, winnable_mem)

# can_create_once(5, [5, 2, 3])

test()