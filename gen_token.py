import time
import math
import random
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from base64 import b64encode


def Ax(a):
    curr_time = int(time.time() * 1000)
    pie = (curr_time % 1000 + a) / 999 * math.pi
    pie -= math.pi / 2
    return (curr_time, math.sin(pie) * 1000)


def _encrypt_text(plain_text: str):
    public_key_base64 = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoa1QCkVvFAfv+fgFpjfq
    9/YrtGzDYull6V0oiy1XPuTCQeb4uptHEmCepnZPmKaP/akp5wS7UTGYw+or//gd
    IER2Cs58q7tVvqxTe68mx901oSw61VOt7mqDVhIsnJlH6yo2Kd9a5rClU/xr618K
    Ry0wuoD2i6mq4fE3uKZZBNrxJ57Jg0EXEsMIvYHxk0kKO8i0YIxEVP84tUuZiq9T
    dcponzr4ny6lqn0YlOSu67kRVL8O0ryHvRJomNN4OcUgq/rUfzJxonqvvmHd75n4
    4r8n4Y7I8/DmVe9cpDWDgv6vk2djRkAQDiLfDEMfq8C7S+/8RPyLTCxXUrR2ouUG
    6QIDAQAB
    -----END PUBLIC KEY-----
    """

    public_key = RSA.import_key(public_key_base64)

    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)

    encrypted = cipher.encrypt(plain_text.encode())

    return b64encode(encrypted).decode()


def generate_token():
    c = Ax(min(random.random() * 0.3, 1))
    return _encrypt_text(json.dumps(c))
