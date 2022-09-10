#!/usr/bin/env python3
import os
import sys
from lib import *

this_dir = os.path.dirname(os.path.abspath(__file__))

OTP_FILE = f"{this_dir}/otp.txt"
OTP_ENCRYPT_OFFSET_FILE = f"{this_dir}/.otp-encrypt-offset"
WORDLIST_FILE = f"{this_dir}/wordlist-numbered.txt"

otp_offset = read_otp_offset(OTP_ENCRYPT_OFFSET_FILE)
otp = OneTimePad(OTP_FILE, otp_offset)
wordlist = read_wordlist(WORDLIST_FILE)

def flatten(nested_list: list) -> list:
    flat_list = []
    for sublist in nested_list:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def encrypt_word(plain_word: str, otp: OneTimePad) -> list[str]:

    if plain_word in symbol_lookup:
        # `plain_word` isn't a word; it's actually a symbol. Convert to an actual word and then encrypt it.
        # For example, "!" converts to [ "exclamation", "point" ]
        symbol_alias: list[str] = symbol_lookup[plain_word]
        return flatten([ encrypt_word(s, otp) for s in symbol_alias ])

    try:
        plain_index = wordlist.get_index(plain_word.lower())
    except KeyError:
        # Not in our word list. Split it up and encrypt each character.
        return flatten([ encrypt_word(ch, otp) for ch in plain_word ])

    key_index = otp.next_word_index()
    encrypted_index = (plain_index + key_index) % wordlist.count
    encrypted_word = wordlist.get_word(encrypted_index)
    return [ encrypted_word ]

def encrypt(plaintext: iter, otp: OneTimePad) -> list[str]:

    # Prepend the current OTP offset to the message so the decrypt script knows where to start reading the OTP
    ciphertext: list[str] = [ str(otp.current_offset) ]

    first_line = True

    for line in plaintext:

        if not first_line:
            line = f"\\n {line}"

        for plain_word in line.split():
            ciphertext += encrypt_word(plain_word, otp)

        first_line = False

    return ciphertext

ciphertext_list = encrypt(sys.stdin, otp)
ciphertext_string = " ".join(ciphertext_list)
write_otp_offset(otp.current_offset, OTP_ENCRYPT_OFFSET_FILE)
print(ciphertext_string)
otp.close()
