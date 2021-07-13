import random


def n_bit_rand(n):
    """
    Utility function used to generate a random n-bit integer.

    :param n: an integer representing the length (bitwise) of the integer to be produced.
    :return: an integer of the desired length (bitwise).
    """

    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


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


def get_prime(length, diff=0):
    """
    Utility function that produces a random prime of the desired length that is not equal to the parameter diff.

    :param length: an integer representing the desired length of the prime that will be returned by the function.
    :param diff: a prime number that should not be returned by the function.
    :return: a random prime number
    """

    prime = n_bit_rand(length)
    while not is_prime(prime) or diff == prime:
        prime = n_bit_rand(length)
    return prime


def gcd(a, b):
    """
    A utility function that implements the Euclid's algorithm in order to
    calculate the greatest common divisor between a and b.

    :param a: the first integer
    :param b: the second integer
    :return: the greatest common divisor between the two parameters.
    """

    while b:
        a, b = b, a % b
    return a


def pick_coprime(x):
    """
    Utility function that finds and returns a random co-prime of the number given as parameter.

    :param x: an integer of which a co-prime is to be found by the function.
    :return: a co-prime of the given parameter.
    """

    cp = random.randrange(1, x)
    while gcd(cp, x) != 1:
        cp = random.randrange(1, x)
    return cp


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


def generate(length):
    """
    Utility function that generates the components needed for implementing of CRT-RSA.

    :param length: an integer representing the bit-length of the primes that are going to be produced.
    :return: a list that contains all the elements need to implement the CRT-RSA.
    """

    # Produce two random primes, different from each other.
    p = get_prime(length)
    q = get_prime(length, p)
    N = p * q
    # Find the φ(Ν) value using Euler's formula
    phi_N = (p - 1) * (q - 1)
    # Find e and d such that e*d = 1 mod φ(Ν)
    e = pick_coprime(phi_N)
    d = pow(e, -1, phi_N)
    # d_p = e^-1 mod (p - 1)
    dp = pow(e, -1, p-1)
    # d_q = e^-1 mod (q - 1)
    dq = pow(e, -1, q-1)
    # i_q = q^-1 mod p
    iq = pow(q, -1, p)

    return p, q, e, d, N, dp, dq, iq


def encrypt(m, e, N):
    """
    Function implementing the encryption stage of the CRT-RSA.

    :param m: a string representing the original message before encryption.
    :param e: an integer representing the public key.
    :param N: an integer representing the modulus.
    :return: a list that contains the encryption of the message, letter by letter.
    """

    # Use letter^e mod N for each letter in the message m.
    return [fast(ord(char), e, N) for char in m]


def decrypt(c, p, q, dp, dq, iq):
    """
    Function implementing the decryption stage of the CRT-RSA.

    :param c: a string representing the ciphertext produced by encrypting.
    :param p: the first prime used for key generation.
    :param q: the second prime used for key generation.
    :param dp: an integer representing the modulo of the private key with respect to p.
    :param dq: an integer representing the modulo of the private key with respect to q.
    :param iq: the modular multiplicative inverse of q.
    :return: a string representing the original message produced by the decryption process.
    """

    m = []
    # For each number in the cipher list
    for num in c:
        # S_p = c^{d_p} mod p
        mp = pow(num, dp, p)
        # S_q = c^{d_q} mod q
        mq = pow(num, dq, q)
        # h = (i_q * (S_p - S_q)) mod p
        h = (iq * (mp - mq)) % p
        # S = S_q + q * h
        m.append(mq + q * h)
    return ''.join(chr(i) for i in m)


if __name__ == '__main__':
    message = "Hope that encrypting the message letter by letter is the right way of doing it."
    # Produce the needed parameters for RSA using length-bit primes.
    p, q, e, d, N, dp, dq, iq = generate(length=2048)
    # Encrypt the text into a list of big integers.
    c = encrypt(message, e, N)
    print("Text encrypted into the following list: {}".format(c))
    # Decrypt the array of integers using the CRT.
    m = decrypt(c, p, q, dp, dq, iq)
    print("Original message after decrypting: {}".format(m))
