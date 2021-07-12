import random

# Substitution matrix used to transform a given message to a corresponding binary representation.
MATRIX = {"A": "00000", "B": "00001", "C": "00010", "D": "00011", "E": "00100", "F": "00101", "G": "00110",
          "H": "00111", "I": "01000", "J": "01001", "K": "01010", "L": "01011", "M": "01100", "N": "01101",
          "O": "01110", "P": "01111", "Q": "10000", "R": "10001", "S": "10010", "T": "10011", "U": "10100",
          "V": "10101", "W": "10110", "X": "10111", "Y": "11000", "Z": "11001", ".": "11010", "!": "11011",
          "?": "11100", "(": "11101", ")": "11110", "-": "11111"}


def toBitString(m):
    """
    Utility function used to convert a string to its corresponding binary representation.

    :param m: a string representing a given message.
    :return: a string representing the binary equivalent to the message given to the function.
    """

    for k, v in MATRIX.items():
        if k in m:
            m = m.replace(k, v)
    return m


def toString(b):
    """
    Utility function used to convert a binary representation to its corresponding message.

    :param b: a string representing a given binary.
    :return: a string representing the message equivalent to the binary given to the function.
    """

    # Isolate each character as a group of 5 bits.
    b_s = ' '.join([b[i:i+5] for i in range(0, len(b), 5)])
    for k, v in MATRIX.items():
        if v in b_s:
            b_s = b_s.replace(v, k)
    return b_s


def bitwise_xor(a, b):
    """
    A utility function that is used to calculate the XOR between two binary strings.

    :param a: a string representing the first binary.
    :param b: a string representing the second binary.
    :return: the result produced by XORing the two strings given as parameters.
    """

    result = ""
    for i in range(0, len(a)):
        result += str(int(a[i]) ^ int(b[i]))
    return result


def OTP(k, m):
    """
    Function implementing the OTP encryption algorithm.

    :param k: a string representing the key that is used during the encryption process.
    :param m: a string representing the message that is going to be encrypted.
    :return: a string representing the cipher produced by the encryption process.
    """

    # Use XOR after the conversion to bit strings.
    c = bitwise_xor(toBitString(m), toBitString(k))
    return toString(c).replace(" ", "")


if __name__ == '__main__':
    original_message = "WE ALL MAKE MISTAKES AND WE ALL PAY A PRICE".replace(" ", "")

    # Encryption and decryption done using a randomly generated key
    key = ""
    keys = list(MATRIX)
    for i in range(len(original_message)):
        key += keys[random.randint(0, len(keys) - 1)]

    ciphertext = OTP(key, original_message)

    print("The original message: {}".format(original_message))
    print("The key: {}".format(key))
    print("The cypher given after OTP encryption: {}".format(ciphertext))
    print("The message given after OTP decryption: {}".format(OTP(key, ciphertext)))

