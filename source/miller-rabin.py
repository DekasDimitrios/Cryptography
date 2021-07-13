import random


def n_bit_rand(n):
    """
    Utility function used to generate a random n-bit integer.

    :param n: an integer representing the length (bitwise) of the integer to be produced.
    :return: an integer of the desired length (bitwise).
    """

    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def fast(a, g, N):
    """
    Implements a fast algorithm that calculates the modular exponentiation
    of the parameters gives such as: Result = a^g mod N.

    :param a: an integer representing the base factor of the calculation.
    :param g: an integer representing the exponent factor of the calculation.
    :param N: an integer representing the modulus factor of the calculation.
    :return: an integer representing the modular exponentiation result equal to a^g mod N.
    """

    # g = (g_n g_n-1 ... g_0)_2
    g = bin(g).replace("0b", "")[::-1]
    # x <- a, d <- 1
    x, d = a, 1
    # for i=0 to n do
    for i in range(len(g)):
        # if g_1 = 1 then
        if g[i] == '1':
            # d <- d*x mod N
            d = (d * x) % N
        # x <- x^2 mod N
        x = (x * x) % N
    # return d
    return d


def miller_rabin(n):
    """
    Implements the Miller-Rabin primality test.

    :param n: an integer that is going to be tested for primality.
    :return: True if the given number is find to be prime, False otherwise.
    """

    # Find integers k, q, where k > 0, q odd, such that n - 1 = 2^k * q
    k, q = 0, n - 1
    while q % 2 == 0:
        k += 1
        q //= 2

    # Pick a random integer a in the range (1, n-1) or [2, n-2]
    a = random.randint(2, n - 2)

    # if a^q mod n = 1 or n - 1 then return "inconclusive"
    x = fast(int(a), int(q), int(n))
    if x == 1 or x == n - 1:
        return True

    # for j = 0 to k - 1 do
    for _ in range(k):
        # if a^2jq mod n = n - 1 then return "inconclusive"
        x = fast(int(x), 2, int(n))
        if x == n - 1:
            return True

    # return "composite"
    return False


def is_prime(n):
    """
    Utility function that determines whether a given number is prime or not.

    :param n: an integer that is going to be tested for primality.
    :return: True if the given number is find to be prime, False otherwise.
    """

    # 1 is not considered a prime number
    if n <= 1:
        return False

    # 2 and 3 are prime numbers
    if n <= 3:
        return True

    # Every even number is composite
    if n % 2 == 0:
        return False

    # Run the Miller-Rabin test 40 times for each number
    # Q: Why 40?
    # A: https://stackoverflow.com/a/6330138
    for _ in range(40):
        if not miller_rabin(n):
            return False

    # If it passes the test for all 40 iterations, then its a prime number, hopefully.
    return True


if __name__ == '__main__':
    rand_num = n_bit_rand(800)
    while True:
        if is_prime(rand_num):
            print("Prime number found: {}". format(rand_num))
            break
        rand_num = n_bit_rand(800)
