#!/usr/bin/env python3
import os
import sys

this_dir = os.path.dirname(os.path.abspath(__file__))

word_to_index_lookup: dict[str, int] = dict()
index_to_word_lookup: dict[int, str] = dict()

def read_word_to_index_lookup():
    with open(f"{this_dir}/wordlist-numbered.txt") as file:
        for line in file:
            split = line.split("\t")
            index = int(split[0].strip())
            word = split[1].strip()
            word_to_index_lookup[word] = index
            index_to_word_lookup[index] = word

read_word_to_index_lookup()
wordlist_count = len(word_to_index_lookup)

def read_otp_lazy() -> iter:
    with open(f"{this_dir}/otp.txt") as file:
        for line in file:
            word_index = int(line.split("\t")[0].strip())
            yield word_index

def encrypt(plaintext: iter, otp_lazy: iter) -> list[str]:
    ciphertext: list[str] = list()
    for line in plaintext:
        line = f"{line}\\n"
        for plain_word in line.split():

            if len(plain_word) != 1:
                # This isn't a letter or symbol -- user typed in a word.
                # All our words in the list are lowercase.
                plain_word = plain_word.lower()

            key_index = otp_lazy.__next__()
            plain_index = word_to_index_lookup[plain_word]
            encrypted_index = (plain_index + key_index) % wordlist_count
            encrypted_word = index_to_word_lookup[encrypted_index]
            ciphertext.append(encrypted_word)
    return ciphertext

otp_lazy = read_otp_lazy()
ciphertext = encrypt(sys.stdin, otp_lazy)
print(" ".join(ciphertext))
