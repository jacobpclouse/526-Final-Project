# Written by Luna D. and Jacob Clouse for ICSI 526 

# Original Paper -> Alternative N-bit Key Data Encryption for Block Ciphers
# Edited on Windows 10 - may need to be edited if you want to use on Linux/MacOS

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import datetime
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec # For generating initial ec key pair

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables & Setup
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# SECP256K1 elliptic curve
curve = ec.SECP256K1()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function to Generate sender and receiver key pairs ---
def generate_key_pair():
    sender_private_key = ec.generate_private_key(curve)
    sender_public_key = sender_private_key.public_key()
    receiver_private_key = ec.generate_private_key(curve)
    receiver_public_key = receiver_private_key.public_key()
    return sender_private_key, sender_public_key, receiver_private_key, receiver_public_key

# --- Function to Encrypt message using ENCK ---
def encrypt_message(MSN, ENCK):
    print(f"MSN: {MSN}")
    print(f"ENCK: {ENCK}")
    # Step 1: Hash message and store in e
    e = hashlib.sha256(MSN).digest()
    print(f"e var: {e}")

    # Step 2: Hash ENCK and store in H1
    # ENCK_bytes = ENCK.to_bytes(32, 'big') # already looks like the ENCK is in bytes (ie: ascii and hex)
    H1 = hashlib.sha256(ENCK).digest()
    print(f"H1: {H1}") 

    # Step 3: Encrypt e with ENCK and store in BLK[0]
    block_size = len(ENCK)
    print(f"Block Size: {block_size}") # looks like block size will be 32... should we adjust this?



# --- Function to print our logo ---
def our_Logo():
    print('Code designed, written & tested by:')
    print('  |                                _ )            |         |          ')
    print('  |      |   |  __ \    _` |       _ \ \          |   _` |  |  /   _ \ ')
    print('  |      |   |  |   |  (   |      ( `  <      \   |  (   |    <    __/ ')
    print(' _____| \__,_| _|  _| \__,_|     \___/\/     \___/  \__,_| _|\_\ \___| ')
    print('Built for ICSI 526 - Spring 2023')

# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime

# --- Function that saves data to a file ---
def write_out_data_to_file(output_file_name, data):
    text_file = open(f"WriteOut_{output_file_name}.txt", "w")
    yeahBoi = text_file.write(data)
    text_file.close()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Program Startup
our_Logo()
# Generate key pairs & Display them
sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()
print('Sender private key:', sender_private_key.private_numbers().private_value)
print('Sender public key:', sender_public_key.public_numbers().x)
print('Receiver private key:', receiver_private_key.private_numbers().private_value)
print('Receiver public key:', receiver_public_key.public_numbers().x)


# Encrypt message defined by the user with ENCK
UserInput = input("Please give me data to encode: ")
MSN = UserInput.encode()
# MSN = b'Hello, world!' # This was the original test input - Encrypt message "Hello, world!" with ENCK
ENCK = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
encrypted_message = encrypt_message(MSN, ENCK)