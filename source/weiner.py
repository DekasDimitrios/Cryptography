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


def get_pq(x, y):
    """
    Utility function used to produce the partial quotients for a continuous fraction.

    :param x: an integer representing the numerator of the fraction.
    :param y: an integer representing the denominator of the fraction.
    :return: a list filled with the produced partial quotients.
    """

    list = []
    quotient = x // y
    remainder = x % y
    list.append(quotient)
    while remainder > 0:
        x = y
        y = remainder
        quotient = x // y
        remainder = x % y
        list.append(quotient)
    return list


def get_denominators(pq):
    """
    Utility function used to extract the denominators of the partial quotients given as parameter.

    :param pq: a list filled with the partial quotient which the denominators are to be extracted.
    :return: a list filled with the denominators found for the partial quotient given as parameter.
    """

    # The denominator of the first partial quotient is equal to 1.
    # The denominator of the second partial quotient is equal to itself.
    d = [1, pq[1]]
    for i in range(2, len(pq)):
        # The denominator of the i-th partial quotient is equal to the i-th partial quotient times the last
        # denominator plus the penultimate denominator.
        d_i = pq[i] * d[i - 1] + d[i - 2]
        d.append(d_i)
    return d


def weiner(N, e):
    """
    Implements the Weiner attack.

    :param N: an integer representing the RSA modulus.
    :param e: an integer representing the encryption exponent.
    :return: None if the attack fails, the secret key if the attack succeeds.
    """

    # Find the partial quotients of e / N.
    partial_quotients = get_pq(e, N)
    # Find the denominators of the found partial quotients.
    c = get_denominators(partial_quotients)
    # Find D such that (2^e)^D = 2modN, and return it.
    for i in range(1, len(c)):
        if fast(2, (e*c[i]), N) == 2:
            return c[i]
    # Return None if the attack fails
    return None


if __name__ == '__main__':
    N = 194749497518847283
    e = 50736902528669041
    C = [47406263192693509, 51065178201172223, 30260565235128704, 82385963334404268,
         8169156663927929, 47406263192693509, 178275977336696442, 134434295894803806,
         112111571835512307, 119391151761050882, 30260565235128704, 82385963334404268,
         134434295894803806, 47406263192693509, 45815320972560202, 174632229312041248,
         30260565235128704, 47406263192693509, 119391151761050882, 57208077766585306,
         134434295894803806, 47406263192693509, 119391151761050882, 47406263192693509,
         112111571835512307, 52882851026072507, 119391151761050882, 57208077766585306,
         119391151761050882, 112111571835512307, 8169156663927929, 134434295894803806,
         57208077766585306, 47406263192693509, 185582105275050932, 174632229312041248,
         134434295894803806, 82385963334404268, 172565386393443624, 106356501893546401,
         8169156663927929, 47406263192693509, 10361059720610816, 134434295894803806,
         119391151761050882, 172565386393443624, 47406263192693509, 8169156663927929,
         52882851026072507, 119391151761050882, 8169156663927929, 47406263192693509,
         45815320972560202, 174632229312041248, 30260565235128704, 47406263192693509,
         52882851026072507, 119391151761050882, 111523408212481879, 134434295894803806,
         47406263192693509, 112111571835512307, 52882851026072507, 119391151761050882,
         57208077766585306, 119391151761050882, 112111571835512307, 8169156663927929,
         134434295894803806, 57208077766585306]

    D = weiner(N, e)

    if D is None:
        print("The attack has failed!")
    else:
        for i in range(len(C)):
            print(chr(fast(C[i], D, N)), end="")
