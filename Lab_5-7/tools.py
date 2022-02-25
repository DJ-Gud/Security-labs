from string import ascii_letters
from datetime import datetime
import os
import hashlib
import nacl.secret

DATA_PATH = 'data.csv'
LOG_PATH = 'log.csv'

def get_secret_box():
    with open('supersecretkey.txt') as file:
        key = file.readlines()[0]

    key =  bytes(bytearray.fromhex(key))
    return nacl.secret.SecretBox(key)

def load_data():
    data = {}
    with open(DATA_PATH) as file:
        lines = file.readlines()
    
    box = get_secret_box()
    for line in lines:
        if line:
            name, login, password, salt, nonce, hpot = line.split(',')
            name = bytes(bytearray.fromhex(name))
            nonce = bytes(bytearray.fromhex(nonce))
            name = box.decrypt(name, nonce).decode('utf-8')
            salt = bytes(bytearray.fromhex(salt))
            hpot =  int(hpot.replace('\n', ''))
            data[login] = (name, password, salt, hpot) 

    return data

def save_user(name, login, password, salt, hpot=0):
    
    box = get_secret_box()
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    name = box.encrypt(bytes(name, 'utf-8'), nonce).hex()

    with open(DATA_PATH, 'a') as file:
        file.write(f'{name},{login},{password},{bytearray(salt).hex()},{bytearray(nonce).hex()},{hpot}\n')

def weak_password(password):
    if len(password) < 8:
        return True

    for ch in password:
        if ch not in ascii_letters:
            return False

    return True

def honey_pot_activation(login, addr, timestamp=None):
    if not timestamp:
        timestamp = datetime.now()

    with open(LOG_PATH, 'a') as file:
        file.write(f'{login},{addr},{timestamp}\n')

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16)
    else:
        assert isinstance(salt, bytes)
    hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hashlib.pbkdf2_hmac('sha1',hash.encode('utf-8'),salt , 50_000).hex(), salt


