import numpy as np

# Constants
NUM_OF_ENG_CHARS = 26
ENG_LETTER_FREQ_ORDER = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U',
                         'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']


def find_key_length(ciphertext):
    """
    Implements the Friedman test in order to determine the key length that was used during encryption.

    :param ciphertext: a string representing the given ciphertext.
    :return: an integer representing the length of the key used to produce the given ciphertext.
    """

    # k <- 2
    k = 2
    # found = false
    # While found = false do
    while True:
        # Create an [n/k] x k matrix
        num_of_rows = len(ciphertext) / k
        if num_of_rows.is_integer():
            num_of_cols = k
            cols = int(num_of_cols) * [""]
            # which columns are the vectors
            # Col[1] = (c[1], c[1+k], ...)
            # Col[2] = (c[2], c[2+k], ...)
            # ............................
            # Col[k] = (c[k], c[2*k], ...)
            for i in range(int(num_of_cols)):
                col_string = ""
                for j in range(int(num_of_rows)):
                    col_string += ciphertext[i + (j * int(num_of_cols))]
                cols[i] = col_string

            # For i = 1 to k do
            for i in range(k):
                # if IC(Col[i]) is close to 0.067 then
                if 0.065 < IC(cols[i]) < 0.070:
                    # found = true
                    # return k
                    return k
        # k <- k + 1
        k += 1


def IC(string):
    """
    Utility function that is used in order to calculate the Index of Coincidence for a given string.

    :param string: the string of which the Index of Coincidence is going to be calculated.
    :return: a float representing the Index of Coincidence for the given string.
    """
    length = len(string)
    # Counts string's letter frequency.
    letter_freq = letter_freq_analysis(string)
    summation = 0
    for i in range(NUM_OF_ENG_CHARS):
        summation += letter_freq[i] * (letter_freq[i] - 1)
    # Return (m_a / k) * ((m_a - 1) / (k - 1))
    return summation / (length * (length - 1))


def find_key(ciphertext, key_length):
    """
    Function used to determine the key used during encryption by matching the most frequent letter in
    the ciphertext with the most frequent letter in the English alphabet.

    :param ciphertext: a string representing the ciphertext to be decrypted.
    :param key_length: an integer representing the length of the key used for encryption.
    :return: a string representing the key used for encryption.
    """

    k = ""
    string = key_length * [""]
    for i in range(key_length):
        for j in range(len(ciphertext) // key_length):
            string[i] += ciphertext[i + j * key_length]
        max_char_ascii = ord('A') + np.argmax(letter_freq_analysis(string[i]))
        key_char = chr(ord('A') + ((max_char_ascii - (ord(ENG_LETTER_FREQ_ORDER[0]))) % 26))
        k += key_char
    return k


def letter_freq_analysis(string):
    """
    Utility function that calculates the letter frequency in a given string.

    :param string: the string of which the letter frequencies are going to be calculated.
    :return: a list that stores the letter frequency that was found in the string parameter.
    """

    # Frequency of each letter in the string
    letter_freq = NUM_OF_ENG_CHARS * [0]
    for i in range(len(string)):
        letter_freq[ord(string[i]) - ord('A')] += 1
    return letter_freq


def decipher(ciphertext, key):
    """
    Utility function used to produce the original message.

    :param ciphertext: a string representing the ciphertext produced by the Vigenere cipher.
    :param key: a string representing the key that was used to encrypt the original message.
    :return: a string representing the original message that was produced by decrypting the ciphertext.
    """

    key_stream = ""

    # Produce key stream.
    for i in range(len(ciphertext) // len(key)):
        key_stream += key
    message = ""

    # Decipher the ciphertext letter by letter.
    for i in range(len(ciphertext)):
        message += chr(ord('A') + ((ord(ciphertext[i]) - ord(key_stream[i])) % 26))

    return message


if __name__ == '__main__':
    ciphertext = "MYHSIFPFGIMUCEXIPRKHFFQPRVAGIDDVKVRXECSKAPFGHMESJWUSSEHNEZIXFFLPQDVTCEUGTEEMFRQXWYCLPPAMBSKSTTPGSMIDNSES" \
             "ZJBDWJWSPQYINUVRFXPVPCEOZQRBNLUIINSRPXLEEHKSTTPGCEIMCSKVVVTJQRBSIUCKJOIIXXOVHYEFLINOEXFDPZJVFKTETVFXTTVJ" \
             "VRTBXRVGJRAIFPSRGTDXYSIWYXWVFPAQSSEHNEZIXFVRXQPRURVWBXWVCEIMCSKVVVUCXYWJAAGPUHYIDTMJFFSYUSISMIDNSESRRPIL" \
             "VUFSPTEIHYMEGMTVRRPREEDISHXHVTFVQKIIMFRQILVKRCAUPZTVGMCFVTIIQPRUPVEGIMWICFGIAVVRZQASJHKLQLEPUIIQSLRGGSUH" \
             "SESUQQCWJCLPEWEJPRVDXGRRVHFWINCIPPLMKVYEFTLRGXSAHIJHVTBTHLGZRFDQZGVVKPRUPCSASWYSUAQWEMSUIHTPFDVHEEIVRSYI" \
             "TLRJVWTJXFIIWQAZVGZRYPGYWEIDNXYOKKUKIJOSYZSEEQVLMHPVTKYEXRNOEXAJVBBFAXTHXSYEEBEUSLWONRZQRPAJVTZVZQGRVGJL" \
             "MGHRBUYZZMERNIFWMEYKSABYTVRRPUIVZKSAAMKHCIYDVVHYEZBETVZRQGCNSEIQSLLARRUICDCIIFWEEQCIHTVESJWITRVSUOUCHESJ" \
             "WMCHXSEXXTRVGJAUILFIKXTTWVELEXXXZSJPUUINWCPNTZZCCIZIEERRPXLMCZSIXDWKHYIMTVFDCEZTEERKLQGEUWFLMKISFFYSWXLG" \
             "TPAHIIHFKQILVFKLQKIIMEEFJVVCWXTTWVWEZQCXZCEWOGMVGFYFUSIHYISDSUBVWEXRDSEGDXIJCLXRDVLBZZQGWRZSVAILVFYSASJF" \
             "FKLQJRZHPSRJWRZCIHTRECNQKKSZQVMEGIRQYMZVQZZCMACWKVISGVLFIKXTTAFFCHYXPCWFREDJUSJTMXVZBXQQCAFAVRMCHCWKXXTG" \
             "YWCHDTRMWTXUBWFTRWKHXVAKLMIQRYVWYTRKCIXGGIRBUMYEVZGFRUCRFQVRFEIFDCIFDXYCJIIWSTOELQPVDSZWMNHFBFXPTWGOZVFW" \
             "IDWJIDNXYOKMECSNIGSZJWZGSYFILVDRWEXRXCWKDTIUHYINXXKSIRQHWFTDIZLLFTVEDILVKRCAULLARRBGSXFVWEILVVRXQDJDSEAU" \
             "APGOJWMCHUWTXMISIGUMQPRUHYIBDAVFKLQNXFCBJDDQKVVTQDTCSNMXAVVHLVZISKVVTQDTCSRRPHSCCEKMHQVBUMQAMSSIXKLMCZEI" \
             "HTVGSIMEWWFZUMQGWUCEXSXZVMFYDHICJVWFDFIIKIEBIEKYSPTWGWJIKDYVBJPMKIPCLATDVVUZQQCXPCLVXXZVGKIXACFINLMIXFRF" \
             "ATPXKCKLUCORBUATPXKCWIQAAYCUVUAPPCLHUTXPCLXDTEKMFYXXOVQRXFAILGVCAJEJQRRZDRWCUHQGHFBKKUKIPCLVETPMSJXAILVG" \
             "VYZCEKIIEXBIEARGTXRVAVRIXXYARGTXRVAZRPHEERDEOWMESYIMGXJMFYMGIECKQMRLZBVWKDYRFVRAIGRHKPQNSLOIIYTRPCLLMKIK" \
             "VVPAKIFTYYYPRZHPMZNSLFYIMGXJMFYPDRKVRXQDRCMKLQJRCCMIPWEKSKLQJRCCMIPPRUHYIGCRRHLVMAWFZUMQGWUCEXRXKYHWSDHP" \
             "RJVVKUMXVKJAGPZPVVFNMEHYIETZVBKLOWEGHVVAUWKZLOQXXZGNVUIXVBKLQZMEUUSYDJXCUMELMKVZRYPRECKSZTQRBESDPKICLTAU" \
             "QVBSYFXRRZCQQCMEMFYKDYKVVTQDTCSYEHTXYSGSITVKVVTALIIHFGDTEKSDEOWMESJXTTTFKVVFDGISRXQWEGDZRQHWPCLXTTTVCGPQ" \
             "WEMSKLQESNSIXABEBSKLUHPZTVJDTIRBUFQPYKWWYXISDOBIFWMJZZJQPAFBUIDUYCOUZQCXLFVXTTRZBKLQCEDSFJPTQFQIEONPVHLW" \
             "GHIKVRXBDAVFCIFJWRZCYZXXVZVXGHJZUYXRDVRBVAIDVCRRHQRIEHNSDAHKVRXIXPCUZZQBIEOTLMCGVHFAAGOKVRXIXPCUZZQNSLHY" \
             "ERJXLFVEZSSCRRKQPWVQLVUICSMKLQEVFAZWQDJKVVWQILZBXWNGYKSJLMKIIWJIZISGCNIDQYKHYIKAMVHYIKSSECKJGAJZZKLMITIC" \
             "DMETXYSPRQKIIKZPXSMTHRXAGWWFVIFWIDGVPHTWSIKXTTCVBJPMKIKVVTQDTCSESIAIKIJJUVLKHFJGAJZZKLMITICDMETPVHLWRXKY" \
             "HKSRGIVHYIIDVCRKSPDENOPAUILEOKMACECPRVDXIIGKSPDENOPAUILXFVIPLMKVYEFTEERZRFDPVFRROTPVHLWRXKYHWSDPAFFCHAUV" \
             "VOJSZPAFFCHIWIISJGUTRTSRRPEVFUIIEHAZZCPQPHKCRPXBIEGYEBEMESJWEDPUWVVEXRKVVRMBIFTUIYDGIOTCXTXLGRPXJRZHV"
    print("The ciphertext is as following: {}".format(ciphertext))

    key_length = find_key_length(ciphertext)
    print("The length of the key was found to be equal to {}".format(key_length))

    key = find_key(ciphertext, key_length)
    print("The key used for encrypting was found to be the word {}".format(key))

    message = decipher(ciphertext, key)
    print("The original message is found to be: {}".format(message))
