from collections import defaultdict


def count_letters(text):
    letters = defaultdict(int)
    for i, ch in enumerate(text):
        if chr(ch) in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.!?\x00':
            letters[i] += 1

    return letters


def xor_seq(first, second):
    res = []
    for pair in zip(first, second):
        res.append(pair[0] ^ pair[1])
    return res


def decode(ciphertext, key):
    result = []
    for pair in zip(key, ciphertext):
        if pair[0]:
            result.append(chr(pair[0] ^ pair[1]))
        else:
            result.append('*')
            
    return result