#!/usr/bin/env python3
import os
import sys
from lib import *

this_dir = os.path.dirname(os.path.abspath(__file__))

OTP_FILE = f"{this_dir}/otp.txt"
OTP_DECRYPT_OFFSET_FILE = f"{this_dir}/.otp-decrypt-offset"
WORDLIST_FILE = f"{this_dir}/wordlist-numbered.txt"

otp_offset = read_otp_offset(OTP_DECRYPT_OFFSET_FILE)
otp = OneTimePad(OTP_FILE, otp_offset)
wordlist = read_wordlist(WORDLIST_FILE)

class OTPSyncError(Exception):
    pass

def decrypt(ciphertext: iter, otp: OneTimePad) -> list[str]:
    starting_otp_word: Optional[str] = None
    for line in ciphertext:
        plaintext: list[str] = list()
        for encrypted_word in line.split():

            if starting_otp_word == None:
                starting_otp_word = otp.next_word()
                if starting_otp_word == encrypted_word:
                    # To help us stay in sync with the message sender, the first word should always be the current word
                    # in the One Time Pad. This is the case; go back to the beginning of the loop and continue with
                    # normal decryption.
                    continue
                else:
                    raise OTPSyncError("This message starts at a different location from where we are in the one-time pad.")

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
write_otp_offset(otp.current_offset, OTP_DECRYPT_OFFSET_FILE)
print(plaintext_string)
otp.close()
