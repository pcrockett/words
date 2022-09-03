#!/usr/bin/env python3
import os
from lib import read_otp_offset
from shutil import copy2 as copy

this_dir = os.path.dirname(os.path.abspath(__file__))

OTP_ENCRYPT_OFFSET_FILE = f"{this_dir}/.otp-encrypt-offset"
OTP_DECRYPT_OFFSET_FILE = f"{this_dir}/.otp-decrypt-offset"

encrypt_offset = read_otp_offset(OTP_ENCRYPT_OFFSET_FILE)
decrypt_offset = read_otp_offset(OTP_DECRYPT_OFFSET_FILE)

if encrypt_offset > decrypt_offset:
    copy(OTP_ENCRYPT_OFFSET_FILE, OTP_DECRYPT_OFFSET_FILE)
else:
    copy(OTP_DECRYPT_OFFSET_FILE, OTP_ENCRYPT_OFFSET_FILE)
