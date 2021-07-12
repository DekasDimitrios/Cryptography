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


if __name__ == '__main__':
    print("2 ^ 1234567 mod 12345 = " + str(fast(2, 1234567, 12345)))
    print("130 ^ 7654321 mod 567 = " + str(fast(130, 7654321, 567)))

    c = [3203, 909, 3143, 5255, 5343, 3203, 909, 9958, 5278, 5343, 9958, 5278, 4674, 909, 9958, 792, 909, 4132, 3143, 9958, 3203, 5343, 792, 3143, 4443]
    for i in range(len(c)):
        print(chr(fast(c[i], 1179, 11413)), end="")
