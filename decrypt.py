#!/usr/bin/env python3
import os
import sys
from lib import *

this_dir = os.path.dirname(os.path.abspath(__file__))

OTP_FILE = f"{this_dir}/otp.txt"
OTP_DECRYPT_OFFSET_FILE = f"{this_dir}/.otp-decrypt-offset"
WORDLIST_FILE = f"{this_dir}/wordlist-numbered.txt"

otp_offset = read_otp_offset(OTP_DECRYPT_OFFSET_FILE)
otp_lazy = read_otp_lazy(OTP_FILE, otp_offset)
wordlist = read_wordlist(WORDLIST_FILE)

def decrypt(ciphertext: iter, otp_lazy: iter) -> list[str]:
    global otp_offset
    for line in ciphertext:
        plaintext: list[str] = list()
        for encrypted_word in line.split():
            key_index = otp_lazy.__next__()
            otp_offset += 1
            encrypted_index = wordlist.get_index(encrypted_word)
            plain_index = (encrypted_index - key_index)
            if plain_index <= 0:
                plain_index += wordlist.count
            plain_word = wordlist.get_word(plain_index)

            if plain_word == "\\n":
                plain_word = "\n"

            plaintext.append(plain_word)

    return plaintext

plaintext_list = decrypt(sys.stdin, otp_lazy)
plaintext_string = " ".join(plaintext_list)
write_otp_offset(otp_offset, OTP_DECRYPT_OFFSET_FILE)
print(plaintext_string)
