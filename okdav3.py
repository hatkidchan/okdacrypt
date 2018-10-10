#!/usr/bin/env python3
# Github: https://github.com/undefinedvalue0103/okdacrypt
from tkinter import Tk, Text, Button
from base64 import decodestring, encodestring
from string import ascii_lowercase, ascii_uppercase, digits

base64alphabet = bytes(ascii_uppercase + ascii_lowercase + digits + '+/', 'utf-8')
default_key = b'OKDA'

_clone_array = lambda array, length: [array[i % len(array)] for i in range(length)]

_shift64 = lambda o: (lambda c: base64alphabet[(base64alphabet.index(c) + o ) % 64] if c in base64alphabet else c)
shift64 = lambda s, o: bytes(list(map(_shift64(o), s)))

def encode(message, key=default_key):
    if not isinstance(message, bytes):
        raise ValueError('message must be bytes')
    if not isinstance(key, bytes):
        raise ValueError('key must be bytes')
    keysum = sum(list(key))
    key = _clone_array(key, len(message))
    data = list(map(lambda d: d[0] ^ d[1], zip(message, key)))
    data = encodestring(bytes(data)).replace(b'\n', b'')
    data = shift64(data, keysum)
    data = ' '.join('%.2X'%v for v in data)
    return '0K DA %s 0K DA'%data

def decode(message, key=default_key):
    if not isinstance(key, bytes):
        raise ValueError('key must be bytes')
    message = bytes.fromhex(message.replace('0K DA', '').replace(' ', '').lower())
    keysum = sum(list(key))
    message = decodestring(shift64(message, -keysum))
    key = _clone_array(key, len(message))
    message = bytes(map(lambda d: d[0] ^ d[1], zip(message, key)))
    return message

def test():
    text = b'Hello, world!'
    key = b'magic'
    print('Input:', text)
    print('Key  :', key)
    encoded = encode(text, key)
    print('Encoded:', encoded)
    decoded = decode(encoded, key)
    print('Decoded:', decoded)
    print('>>>', 'OK' if decoded == text else 'FAIL')

if __name__ == '__main__':
    test()
