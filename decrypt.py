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

def decrypt(ciphertext: iter, otp_lazy: iter) -> list[str]:
    for line in ciphertext:
        plaintext: list[str] = list()
        for encrypted_word in line.split():
            key_index = otp_lazy.__next__()
            encrypted_index = word_to_index_lookup[encrypted_word]
            plain_index = (encrypted_index - key_index)
            if plain_index < 0:
                plain_index += wordlist_count
            plain_word = index_to_word_lookup[plain_index]

            if plain_word == "\\n":
                plain_word = "\n"

            plaintext.append(plain_word)

    return plaintext

otp_lazy = read_otp_lazy()
plaintext = decrypt(sys.stdin, otp_lazy)
print(" ".join(plaintext))
