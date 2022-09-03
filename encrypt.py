#!/usr/bin/env python3
import os
import sys
from lib import *

this_dir = os.path.dirname(os.path.abspath(__file__))

OTP_FILE = f"{this_dir}/otp.txt"
OTP_ENCRYPT_OFFSET_FILE = f"{this_dir}/.otp-encrypt-offset"
WORDLIST_FILE = f"{this_dir}/wordlist-numbered.txt"

otp_offset = read_otp_offset(OTP_ENCRYPT_OFFSET_FILE)
otp_lazy = read_otp_lazy(OTP_FILE, otp_offset)
wordlist = read_wordlist(WORDLIST_FILE)

def encrypt_word(plain_word: str, otp_lazy: iter) -> list[str]:
    global otp_offset

    if len(plain_word) <= 1:
        plain_index = wordlist.get_index(plain_word)
    else:
        # This isn't a letter or symbol -- the user typed in a word.
        try:
            plain_index = wordlist.get_index(plain_word.lower())
        except KeyError:
            # Not in our word list. Split it up and encrypt each character.
            return [encrypt_word(ch, otp_lazy)[0] for ch in plain_word]

    key_index = otp_lazy.__next__()
    otp_offset += 1
    encrypted_index = (plain_index + key_index) % wordlist.count
    encrypted_word = wordlist.get_word(encrypted_index)
    return [ encrypted_word ]

def encrypt(plaintext: iter, otp_lazy: iter) -> list[str]:
    global otp_offset
    ciphertext: list[str] = list()
    first_line = True
    for line in plaintext:

        if not first_line:
            line = f"\\n {line}"

        for plain_word in line.split():
            ciphertext += encrypt_word(plain_word, otp_lazy)

        first_line = False

    return ciphertext

ciphertext_list = encrypt(sys.stdin, otp_lazy)
ciphertext_string = " ".join(ciphertext_list)
write_otp_offset(otp_offset, OTP_ENCRYPT_OFFSET_FILE)
print(ciphertext_string)
