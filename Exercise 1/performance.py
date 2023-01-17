import time


def zeros1(num):#1st solution
    m = num
    cnt = 0
    while m > 0:
        if m % 10 == 0:
            cnt = cnt + 1
        m = m // 10
    return cnt


def zeros2(num):#2nd solution
    cnt = 0
    snum = str(num) #num as a string
    for digit in snum:
        if digit == "0":
            cnt = cnt + 1
    return cnt


def zeros3(num):#3rd solution
    cnt = str.count(str(num), "0")
    return cnt


def counter(num):
    cnt = 0
    snum = str(num)
    for digit in snum:
        cnt = cnt + 1


def measure(func, num):
    t0 =  time.perf_counter()
    func(num)
    t1 =  time.perf_counter()
    print(t1-t0)