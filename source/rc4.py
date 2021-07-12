import numpy as np


def swap(a, b):
    """
    Utility function used to swap the value of a with b and vice versa.

    :param a: the first value to be swapped.
    :param b: the second value to be swapped.
    """

    temp = a
    a = b
    b = temp


def RC4(k, m):
    """
    Function implementing the RC4 encryption algorithm.

    :param k: a string representing the key that is used during the encryption process.
    :param m: a string representing the message that is going to be encrypted.
    :return: a string representing the cipher produced by the encryption process.
    """

    # Encode key as an ASCII valued array.
    K = np.array([ord(c) for c in k])
    # The length of the key array
    keylen = K.shape[0]

    # Encode message as an ASCII valued array.
    M = np.array([ord(c) for c in m])
    # The length of the message array
    messagelen = M.shape[0]

    # The array used to store the permutations
    S = np.empty(256, dtype=int)
    # The array used to store the key repeated as many times as needed.
    T = np.empty(256, dtype=int)

    # Create the key stream array
    KS = np.empty(messagelen, dtype=int)

    # Initialization
    for i in range(256):
        S[i] = i
        T[i] = K[i % keylen]

    # Initial Permutations of S
    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        swap(S[i], S[j])

    # Generate Key Stream
    i = 0
    j = 0
    while i < messagelen:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        swap(S[i], S[j])
        t = (S[i] + S[j]) % 256
        KS[i - 1] = S[t]

    # Decode ASCII valued array as a message referred to as the cypher
    c = ''.join(np.array([chr(num) for num in np.bitwise_xor(M, KS)]))

    return c


if __name__ == "__main__":
    key = 'HOUSE'
    original_message = "WE ALL MAKE MISTAKES AND WE ALL PAY A PRICE".replace(" ", "")
    ciphertext = RC4(key, original_message)

    print("The original message: " + original_message)
    print("The key: " + key)
    print("The cypher given after RC4 encryption: " + ciphertext)
    print("The message given after RC4 decryption: " + RC4(key, ciphertext))
