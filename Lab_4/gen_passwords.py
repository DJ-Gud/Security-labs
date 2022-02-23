import random
import string
from nltk.util import ngrams
from collections import defaultdict
import os
import hashlib


def get_top25_passwords(n_passwords):
    with open('data/top25.txt') as file:
        passwords = file.readlines()
    
    passwords = list(map(lambda x: x.strip(), passwords))
    
    return [random.choice(passwords) for _ in range(n_passwords)]


def get_top100k_passwords(n_passwords):
    with open('data/10-million-password-list-top-100000.txt') as file:
        passwords = file.readlines()
    
    passwords = list(map(lambda x: x.strip(), passwords))
    
    return [random.choice(passwords) for _ in range(n_passwords)]


def get_random_passwords(n_passwords, length=8):
    letter_space = string.printable[:63]
    passwords = [''.join(random.choice(letter_space) for i in range(length))
                 for _ in range(n_passwords)]
    return passwords


def _get_ngrams_distr(fname, N=4):
    with open(fname) as file:
        passwords_raw = file.readlines()
    
    all_ngrams = []
    for i, password in enumerate(passwords_raw):
        all_ngrams += list(map(lambda x: ''.join(x), ngrams(password.strip().lower(), N)))
        
    n_grams_distr = defaultdict(list)
    for i, token in enumerate(all_ngrams[:-1]):
        n_grams_distr[token].append(all_ngrams[i+1])
        
    return n_grams_distr


def get_human_like_passwords(n_passwords, pass_length=8, n_grams_distr=None):
    
    if not n_grams_distr:
        n_grams_distr = _get_ngrams_distr('data/10-million-password-list-top-100000.txt')
    
    passwords = []
    keys = list(n_grams_distr.keys())
    N = len(keys[0])
    
    for _ in range(n_passwords):
        n_gram = random.choice(keys)
        password = n_gram
        for i in range(int(pass_length / N) - 1):
            n_gram = random.choice(n_grams_distr[n_gram])
            password += n_gram
        passwords.append(password)
        
    return passwords

def gen_passwords(distr, n):
    passwords = []
    for percentage, func in passwords_distribution.values():
        n_passwords = int(n*percentage)
        passwords += func(n_passwords)
        
    return passwords


if __name__ == "__main__":
    
    NUM_PASSWORDS = 100_000
    passwords_distribution = {
        "top25":   (0.05, get_top25_passwords),
        "top100k": (0.8, get_top100k_passwords),
        "random":  (0.05, get_random_passwords),
        "human":   (0.1, get_human_like_passwords)
    }
    
    hashing_schemas = {
        "md5": lambda x: hashlib.md5(x.encode('utf-8')).hexdigest(),
        "pbkdf2 sha1": lambda x: hashlib.pbkdf2_hmac('sha1', x.encode('utf-8'), os.urandom(16), 50_000).hex()
    }
    
    for i, schema in enumerate(hashing_schemas.values()):
        passwords = gen_passwords(passwords_distribution, NUM_PASSWORDS)
        hashes = map(schema, passwords)

        with open(f'schema{i}.txt', "w") as file:
            for hash in hashes:
                 file.write(hash + "\n")
