# different python implementations

def fib1(n: int) -> int:
    """This is a recursive way"""
    if n < 2 : return n

    return fib1(n-1) + fib1(n-2)

from typing import Dict

memo : Dict[int, int] = {0: 0, 1:1}

def fib2(n: int) -> int: 
    """This approach is recursive but uses 
        memoization"""
    if n not in memo:
        memo[n] = fib2(n-1) + fib2(n-2)
    return memo[n]

from functools import lru_cache

@lru_cache(maxsize=None)
def fib3(n: int) -> int:
    """This approach is recursive but uses
        caching mechanisms"""
    if n < 2 : return 
    return fib3(n-1) + fib3(n-2)

def fib4(n: int) -> int:
    """This approach is iterative"""
    if n==0 : return n
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last+next
    return next

def fib5(n: int) -> int: 
    """This approach generates the results
       for each integer before n"""
    yield 0
    if n > 0 : yield 1
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last + next
        yield next

if __name__ == "__main__":
    print(fib1(10))
    print(fib2(15))
    print(fib3(4))
    print(fib4(11)
    print(fib5(23))


