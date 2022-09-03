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

def encrypt(plaintext: iter, otp_lazy: iter) -> list[str]:
    global otp_offset
    ciphertext: list[str] = list()
    first_line = True
    for line in plaintext:

        if not first_line:
            line = f"\\n {line}"

        for plain_word in line.split():

            if len(plain_word) != 1:
                # This isn't a letter or symbol -- user typed in a word.
                # All our words in the list are lowercase.
                plain_word = plain_word.lower()

            key_index = otp_lazy.__next__()
            otp_offset += 1
            plain_index = wordlist.get_index(plain_word)
            encrypted_index = (plain_index + key_index) % wordlist.count
            encrypted_word = wordlist.get_word(encrypted_index)
            ciphertext.append(encrypted_word)

        first_line = False

    return ciphertext

ciphertext = encrypt(sys.stdin, otp_lazy)
write_otp_offset(otp_offset, OTP_ENCRYPT_OFFSET_FILE)
print(" ".join(ciphertext))
