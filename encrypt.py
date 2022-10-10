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
symbol_set = set("!#%&'\"()*+,-./\\:;<=>?@[]^_`{|}~$0123456789")

def flatten(nested_list: list) -> list:
    flat_list = []
    for sublist in nested_list:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def characterize_if_needed(word: str) -> list[str]:
    if wordlist.exists(word.lower()):
        return [word]
    else:
        return [ch for ch in word]

def partition_word(word: str) -> list[str]:
    partitions: list[str] = [""]
    for ch in word:
        if ch in symbol_set:
            partitions.append(ch)
            partitions.append("")
        else:
            current_word = partitions[-1]
            partitions[-1] = current_word + ch

    return flatten([
        characterize_if_needed(w)
        for w in partitions if w != ""
    ])

def encrypt_word(plain_word: str, otp: OneTimePad) -> list[str]:

    if len(plain_word) == 1:
        plain_index = wordlist.get_index(plain_word)
    else:
        try:
            plain_index = wordlist.get_index(plain_word.lower())
        except KeyError:
            # Not in our word list. Split it up and encrypt each piece.
            return flatten([
                encrypt_word(w, otp)
                for w in partition_word(plain_word)
            ])

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
