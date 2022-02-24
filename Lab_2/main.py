from tools import xor_seq, count_letters, decode
from collections import Counter


def crack(ciphertexts):
    
    ciphertexts = sorted(ciphertexts, key=len)
    key_final = []
    max_len = 0
    for ciphertext in ciphertexts:

        if max_len != 0:
            ciphertexts = [c[max_len:] for c in ciphertexts]

        max_len = len(ciphertext)
        min_len = min(len(text) for text in ciphertexts)

        key_iter = [None for _ in range(min_len)]

        for i, ciphertext in enumerate(ciphertexts):
            counter = Counter()

            for j, compare in enumerate(ciphertexts):
                if i != j:
                    xored = xor_seq(ciphertext, compare)
                    iter_counts = count_letters(xored)
                    counter.update(iter_counts)

            for i, count in counter.items():
                if count == len(ciphertexts) - 1:
                    key_iter[i] = ciphertext[i] ^ 32  # 32 is a space in ASCII

        key_final += key_iter
        
    return key_final


if __name__ == '__main__':
    
    with open('input.txt') as file:
        ciphertext = file.readlines()
    
    ciphertexts = [bytes.fromhex(line.rstrip()) for line in ciphertext]
    key = crack(ciphertexts)
    
    for ciphertext in ciphertexts:
        text = decode(ciphertext, key)
        text = ''.join(text)
        print(text)
        