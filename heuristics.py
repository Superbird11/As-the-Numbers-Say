"""
file: heuristics.py
author: Louis Jacobowitz (ljacobo@ncsu.edu)

This file contains many standalone methods for determining various properties of numbers.
"""
primes = [2, 3]
fibonacci_numbers = [0, 1]


def ones_in_binary_repr(num):
    """ Returns the number of ones in this number's binary representation """
    return bin(num).count('1')


def zeroes_in_binary_repr(num):
    """ Returns the number of zeroes in this number's binary representation """
    return bin(num).count('0') - 1


def _base(decimal, base):
    """
    Converts a number to the given base, returning a string.
    Taken from https://stackoverflow.com/a/26188870/2648811
    :param decimal: The base-10 representation of an integer
    :param base: The base to which to convert it
    :return: A string containing the base-base representation of the given number
    """
    li = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    other_base = ""
    while decimal != 0:
        other_base = li[decimal % base] + other_base
        decimal = decimal // base
    if other_base == "":
        other_base = "0"
    return other_base


def digital_sum(num, base=10):
    """ Returns the sum of the digits in the base-base representation of the given number. """
    return sum(int(d, base) for d in _base(num, base))


def digital_root(num, base=10):
    """ Returns the digital root of the base-base representation of the given number. """
    root = digital_sum(num, base)
    while root >= base:
        root = digital_sum(root, base)
    return root


def palindromes(num, bases=range(10, 1, -1)):
    """
    Checks if the given number is a palindrome in every given base, in order. Returns the sublist of bases for which
    the given number is a palindrome, or an empty list if it is not a palindrome in any base checked.
    """
    r = []
    for i in bases:
        b = _base(num, i)
        if b == b[::-1]:
            r.append(i)
    return r


def is_palindrome(num, bases=range(10, 1, -1)):
    """
    Checks if the given number is a palindrome in every given base, in order, and returns the first base for which
    it is. Returns 0 if the number isn't a palindrome in any given base.
    """
    r = palindromes(num, bases)
    return r[-1] if r else 0


def last_nonzero_digit(num, base=10):
    """ Returns the last nonzero digit of the number. """
    if num == 0:
        return 0
    without_zeros = [int(i, base) for i in _base(num, base) if i != '0']
    return without_zeros[-1]


def is_prime(num):
    """ Returns True if the given number is prime, False otherwise. Updates list of primes as number grows. """
    global primes
    while num > primes[-1]:
        n = primes[-1] + 2
        y = [bool(n % p) for p in primes]
        while not all(n % p for p in primes):
            n += 2
        primes.append(n)
    return num in primes


def highest_digit(num, base=10):
    """ Returns the highest digit in the given number, in the given base """
    return max(int(c, base) for c in _base(num, base))


def lowest_digit(num, base=10):
    """ Returns the lowest digit in the given number, in the given base """
    return min(int(c, base) for c in _base(num, base))


def prime_factors(num):
    """ Returns a list of the prime factors of the given number, excluding 1 """
    if is_prime(num):
        return [num]
    n = num
    factors = []
    for p in primes:
        while n % p == 0:
            factors.append(p)
            n /= p
        if n == 1:
            break
    return factors


def sum_of_prime_factors(num):
    """ Returns the sum of the prime factors of the given number """
    return sum(prime_factors(num))


def divisors(num):
    """ Returns a list of all integers that divide this number, including 1 but not including this number """
    return [i for i in range(1, num//2+1) if num % i == 0]


def sum_of_divisors(num):
    """ Returns the sum of all integers that divide this number, including 1 but not including this number """
    return sum(divisors(num))


def is_fibonacci_number(num):
    """
    Returns True if the given number is in the Fibonacci sequence, False otherwise. Computes Fibonacci sequence
    iteratively as needed.
    """
    global fibonacci_numbers
    while num > fibonacci_numbers[-1]:
        fibonacci_numbers.append(fibonacci_numbers[-1] + fibonacci_numbers[-2])
    return num in fibonacci_numbers


def is_happy_number(num, base=10):
    """
    Returns True if the given number is a Happy Number in the given base, False otherwise.
    https://en.wikipedia.org/wiki/Happy_number
    """
    visited = []
    while num not in visited:
        visited.append(num)
        num = sum(int(i, base)**2 for i in _base(num, base))
    return num == 1
