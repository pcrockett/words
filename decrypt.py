#!/usr/bin/env python3
import os
import sys
from lib import *

this_dir = os.path.dirname(os.path.abspath(__file__))

OTP_FILE = f"{this_dir}/otp.txt"
OTP_DECRYPT_OFFSET_FILE = f"{this_dir}/.otp-decrypt-offset"
WORDLIST_FILE = f"{this_dir}/wordlist-numbered.txt"

previous_otp_offset = read_otp_offset(OTP_DECRYPT_OFFSET_FILE)
wordlist = read_wordlist(WORDLIST_FILE)

def read_otp_offset_from_stdin() -> int:
    valid_chars = set("0123456789")
    first_word = ""
    while (ch := sys.stdin.read(1)) in valid_chars:
        first_word += ch
    return int(first_word)

otp_offset = read_otp_offset_from_stdin()

if otp_offset < previous_otp_offset:
    sys.stderr.write(
        "WARNING: Either this message is reusing part of the one-time pad, or it is an old message.\n" +
        "       : It is TRIVIAL to defeat encryption if any part of the one-time pad is reused!\n" +
        "       : If this is just an old message, then you have nothing to worry about.\n"
    )

otp = OneTimePad(OTP_FILE, otp_offset)

def decrypt(ciphertext: iter, otp: OneTimePad) -> list[str]:
    plaintext: list[str] = list()
    for line in ciphertext:
        for encrypted_word in line.split():
            key_index = otp.next_word_index()
            encrypted_index = wordlist.get_index(encrypted_word)
            plain_index = (encrypted_index - key_index)
            if plain_index <= 0:
                plain_index += wordlist.count
            plain_word = wordlist.get_word(plain_index)
            if plain_word == "\\n":
                plain_word = "\n"
            plaintext.append(plain_word)
    return plaintext

plaintext_list = decrypt(sys.stdin, otp)
plaintext_string = " ".join(plaintext_list)

if otp.current_offset > previous_otp_offset:
    write_otp_offset(otp.current_offset, OTP_DECRYPT_OFFSET_FILE)

print(plaintext_string)
otp.close()
