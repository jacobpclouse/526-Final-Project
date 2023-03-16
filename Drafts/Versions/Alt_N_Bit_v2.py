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

# Debug mode variable
chooseDebugMode = ''

# Array of hashes - encryption (basically we can store all the hashes used for h1 in this for decryption) - NOT IMPLIMENTED YET!!!
encryption_hashes = []

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

''' MAIN LOOP ENCRYPTION'''
# --- Function that kicks of the encryption routine ---
def main_loop_encryption():
    # Debug mode setup - if yes, enable print outs, if no then no print outs should be shown
    chooseDebugMode = input("Debug Mode - Do you want console print outs?: YES or NO? ").upper()
    print(chooseDebugMode)
    print('\n')

    # Catch statement to prevent invalid selections
    while chooseDebugMode == '':
        chooseDebugMode = input("Can't be left blank, please input either YES or NO: ")

    # Generate key pairs & Display them
    sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()
    if chooseDebugMode == 'YES':
        print('Sender private key:', sender_private_key.private_numbers().private_value)
        print('Sender public key:', sender_public_key.public_numbers().x)
        print('Receiver private key:', receiver_private_key.private_numbers().private_value)
        print('Receiver public key:', receiver_public_key.public_numbers().x)

    # Encrypt message defined by the user with ENCK
    # Define if you want this to use sample data or if you want to define input:
    chooseMSN = input("Do you want to use the default MSN test data? : YES or NO? ")
    print(chooseMSN.upper())
    print('\n')

        # Catch statement to prevent invalid selections
    while chooseMSN == '':
        chooseMSN = input("Can't be left blank, please input either YES or NO: ")

        # execute if they don't want to use the default data, user will input the test data and it will be encoded
    if chooseMSN.upper() == 'NO':
        print("User Providing Test Data.")
        UserInput = input("Please give me data to encode: ")
        MSN = UserInput.encode()

        # if they do want to use the default data (or nonsense), then we just will use the default data
    else:
        print("Using Default Test Data.")
        MSN = b'Hello, world!' # This was the original test input - Encrypt message "Hello, world!" with ENCK


    # Grabbing the ENCK
    ENCK = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
    encrypted_message = encrypt_message(MSN, ENCK)

    if chooseDebugMode == 'YES':
        print(f"Final result of encryption: {encrypted_message.hex()}")



# --- Function to Encrypt message using ENCK ---
def encrypt_message(MSN, ENCK):
    # Step 1: Hash message and store in e
    e = hashlib.sha256(MSN).digest()
    if chooseDebugMode == 'YES':
        print(f"MSN: {MSN}")
        print(f"ENCK: {ENCK}")
        print(f"e var: {e}")

    # Step 2: Hash ENCK and store in H1
    H1 = hashlib.sha256(ENCK).digest()
    if chooseDebugMode == 'YES':
        print(f"H1: {H1}") 

    # Step 3: Encrypt e with ENCK and store in BLK[0]
    block_size = len(ENCK)
    if chooseDebugMode == 'YES':
        print(f"Block Size: {block_size}") # looks like block size will be 32... should we adjust this?
    BLK = [e[i:i+block_size] for i in range(0, len(e), block_size)]
    BLK[0] = bytes([BLK[0][i] ^ ENCK[i] for i in range(block_size)])
    if chooseDebugMode == 'YES':
        print(f"BLK: {BLK}")
        print(f"BLK[0]: {BLK[0]}")

    # Step 4: Hash e using H1 as initialization vector and store in H1
    # H1 = hashlib.sha256(e, H1).digest() #ERRORING - how do we hash two variables? ****
    # Concatenate e and H1 before hashing
    data_to_hash = e + H1
    H1 = hashlib.sha256(data_to_hash).digest()
    if chooseDebugMode == 'YES':
        print(f"data_to_hash: {data_to_hash}")
        print(f"NEW H1: {H1}")


    # Step 5: Encrypt n blocks of MSN using different keys -- THIS RETURNS EMPTY VALUES - WHYYY???
    # alright, we need to add some extra text to get it up over the the block size here (maybe add the block data to the end of the message?)
    print(f'Len(MSN): {len(MSN)}')
    print(f'Len(BLK[0]): {len(BLK[0])}')
    n = len(MSN) // len(BLK[0])
    print(f"what is n: {n}") # n is 0, its not hitting the for loop...
    encrypted_blocks = []
    for i in range(n):
        key = H1
        print(f"key: {key}")
        if i > 0:
            key = hashlib.sha256(key).digest()
            print(f"Hashlib key: {key}")
        block = MSN[i*len(BLK[0]):(i+1)*len(BLK[0])]
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_block = encryptor.update(block) + encryptor.finalize()
        encrypted_blocks.append(encrypted_block)
        new_data_to_hash_loop = encrypted_block + H1
        H1 = hashlib.sha256(new_data_to_hash_loop).digest()
        # H1 = hashlib.sha256(encrypted_block, H1).digest()
    print(f"Encrypted Blocks: {encrypted_blocks}")

    return b''.join(encrypted_blocks)


''' MAIN LOOP DECRYPTION'''
# --- Function that kicks of the encryption routine ---
def main_loop_decryption():
    print("decrypt boi")


# --- Function to Generate sender and receiver key pairs ---
def generate_key_pair():
    sender_private_key = ec.generate_private_key(curve)
    sender_public_key = sender_private_key.public_key()
    receiver_private_key = ec.generate_private_key(curve)
    receiver_public_key = receiver_private_key.public_key()
    return sender_private_key, sender_public_key, receiver_private_key, receiver_public_key



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

# Program Startup -- Logo Print Out shows that it is working
our_Logo()

# User decides if we are gonna use encrypt or decrypt
encryptOrDecrypt = input("Do you want to ENCRYPT or DECRYPT? ").upper()

# Catch statement to prevent invalid selections
while encryptOrDecrypt == '':
    encryptOrDecrypt = input("Can't be left blank, please input either ENCRYPT or DECRYPT: ").upper()

# execute Encryption
if encryptOrDecrypt == 'ENCRYPT':
    main_loop_encryption()

# execute Decryption
elif encryptOrDecrypt == 'DECRYPT':
    main_loop_decryption()

# if nonsense, end the script
else:
    print("Response Not Recognized, Ending Program...")

'''
# Debug mode setup - if yes, enable print outs, if no then no print outs should be shown
chooseDebugMode = input("Debug Mode - Do you want console print outs?: YES or NO? ").upper()
print(chooseDebugMode)
print('\n')

    # Catch statement to prevent invalid selections
while chooseDebugMode == '':
    chooseDebugMode = input("Can't be left blank, please input either YES or NO: ")

# Generate key pairs & Display them
sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()
if chooseDebugMode == 'YES':
    print('Sender private key:', sender_private_key.private_numbers().private_value)
    print('Sender public key:', sender_public_key.public_numbers().x)
    print('Receiver private key:', receiver_private_key.private_numbers().private_value)
    print('Receiver public key:', receiver_public_key.public_numbers().x)

# Encrypt message defined by the user with ENCK
# Define if you want this to use sample data or if you want to define input:
chooseMSN = input("Do you want to use the default MSN test data? : YES or NO? ")
print(chooseMSN.upper())
print('\n')

    # Catch statement to prevent invalid selections
while chooseMSN == '':
    chooseMSN = input("Can't be left blank, please input either YES or NO: ")

    # execute if they don't want to use the default data, user will input the test data and it will be encoded
if chooseMSN.upper() == 'NO':
    print("User Providing Test Data.")
    UserInput = input("Please give me data to encode: ")
    MSN = UserInput.encode()

    # if they do want to use the default data (or nonsense), then we just will use the default data
else:
    print("Using Default Test Data.")
    MSN = b'Hello, world!' # This was the original test input - Encrypt message "Hello, world!" with ENCK


# Grabbing the ENCK
ENCK = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
encrypted_message = encrypt_message(MSN, ENCK)

if chooseDebugMode == 'YES':
    print(f"Final result of encryption: {encrypted_message.hex()}")
'''