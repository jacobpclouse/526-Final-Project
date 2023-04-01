# Written by Luna D. and Jacob Clouse for ICSI 526 

# Original Paper -> Alternative N-bit Key Data Encryption for Block Ciphers
# Edited on Windows 10 - may need to be edited if you want to use on Linux/MacOS

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import datetime # used to grab the datetime in logo printout
import os
import hashlib # Used in Sha256 hashing
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # needed for encryption /decryption modules
from cryptography.hazmat.backends import default_backend # needed for encryption /decryption modules
from cryptography.hazmat.primitives import hashes, serialization # needed for encryption /decryption modules
from cryptography.hazmat.primitives.asymmetric import ec # For generating initial ec key pair
import pickle # this is used to store byte arrays and then get the data back out
import secrets # for padding MSN up to block size
import string # for padding MSN up to block size
import random # adding so we add an arbitrary length to our msg

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

# --- Function to Generate sender and receiver key pairs ---
# This code was sourced from Line 22 of Provable Things encrypted-queries (EC example): https://github.com/provable-things/encrypted-queries/blob/master/tools/encrypted_queries_tools.py 
def generate_key_pair():
    sender_private_key = ec.generate_private_key(curve)
    sender_public_key = sender_private_key.public_key()
    receiver_private_key = ec.generate_private_key(curve)
    receiver_public_key = receiver_private_key.public_key()
    return sender_private_key, sender_public_key, receiver_private_key, receiver_public_key


# --- Function to Encrypt message using ENCK ---
def encrypt_message(MSN, ENCK):
    # Step 1: Hash message and store in e
    # hashlib doc: https://docs.python.org/3/library/hashlib.html
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

    # python bitwise xor: https://favtutor.com/blogs/xor-python
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


    # Step 5: Encrypt n blocks of MSN using different keys 
    # alright, we need to add some extra text to get it up over the the block size here (maybe add the block data to the end of the message?)
    print(f'Len(MSN): {len(MSN)}')
    print(f'Len(BLK[0]): {len(BLK[0])}')
    n = len(MSN) // len(BLK[0])
    print(f"what is n: {n}") # if n is 0, it will not access the loop, we need to make sure that it is equal or greater than the block size
    encrypted_blocks = []
    for i in range(n):
        key = H1
        print(f"key: {key}")
        if i > 0:
            key = hashlib.sha256(key).digest()
            print(f"Hashlib key: {key}")
        # Python: for loops - for i in range(0,len(list) vs for i in list: https://stackoverflow.com/questions/32930246/python-for-loops-for-i-in-range0-lenlist-vs-for-i-in-list
        block = MSN[i*len(BLK[0]):(i+1)*len(BLK[0])]
        # Symmetric encryption: https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_block = encryptor.update(block) + encryptor.finalize()
        encrypted_blocks.append(encrypted_block)
        new_data_to_hash_loop = encrypted_block + H1
        H1 = hashlib.sha256(new_data_to_hash_loop).digest()
        # H1 = hashlib.sha256(encrypted_block, H1).digest()
    print(f"Encrypted Blocks: {encrypted_blocks}")

    return b''.join(encrypted_blocks)


# --- Function to Decrypt message using ENCK --- ## NEED TO TEST!!!! 
# Do we feed in the Same ENCK from before encryption? It shouldn't change here
def decrypt_message(encrypted_message, ENCK):
    # Step 1: Hash ENCK and store in H1
    H1 = hashlib.sha256(ENCK).digest()
    if chooseDebugMode == 'YES':
        print(f"encrypted_message: {encrypted_message}")
        print(f"ENCK: {ENCK}")
        print(f"H1 var: {H1}")
    

    # Step 2: Decrypt the first block of the message
    block_size = len(ENCK)
    first_block = encrypted_message[:block_size]
    decrypted_first_block = bytes([first_block[i] ^ ENCK[i] for i in range(block_size)])
    if chooseDebugMode == 'YES':
        print(f"block_size: {block_size}")
        print(f"first_block: {first_block}")
        print(f"decrypted_first_block: {decrypted_first_block}")

    # Step 3: Hash the decrypted first block using H1 as initialization vector and update H1
    data_to_hash = decrypted_first_block + H1
    H1 = hashlib.sha256(data_to_hash).digest()
    if chooseDebugMode == 'YES':
        print(f"data_to_hash: {data_to_hash}")
        print(f"Updated H1: {H1}")

    # Step 4: Decrypt the remaining blocks of the message using the updated H1 as the key
    decrypted_blocks = []
    for i in range(1, len(encrypted_message) // block_size):
        key = H1
        print(f"key: {key}")
        if i > 1:
            key = hashlib.sha256(key).digest()
            print(f"Hashlib key: {key}")
        block = encrypted_message[i*block_size:(i+1)*block_size]
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_block = decryptor.update(block) + decryptor.finalize()
        decrypted_blocks.append(decrypted_block)
        data_to_hash = decrypted_block + H1
        H1 = hashlib.sha256(data_to_hash).digest()
    
    print(f"[decrypted_first_block] + decrypted_blocks: {[decrypted_first_block] + decrypted_blocks}")

    # Step 5: Concatenate the decrypted blocks and return the original message
    return b''.join([decrypted_first_block] + decrypted_blocks)


# --- Function to add random padding to anemic inputs (if they are less than desired length) ---
def do_we_need_padding(messageToAnalyze,targetBlockSizeInteger):
    # Usually targetBlockSizeInteger will be like 32
    if (len(messageToAnalyze) < targetBlockSizeInteger):
        numberOfCharsLeft = targetBlockSizeInteger - len(messageToAnalyze) # figure out how many chars we are short by
        print(f"We need to pad at least {numberOfCharsLeft} characters!")
        numberOfCharsLeft = numberOfCharsLeft + (random.randint(0,200)) # incriment by a random value, that way it won't be exactly the same as our ENCK
        # using secrets.choices() - generating random strings
        toConcatBoi = ''.join(secrets.choice(string.ascii_letters + string.digits)
            for i in range(numberOfCharsLeft))
        messageToAnalyze = messageToAnalyze + bytes(toConcatBoi,encoding='utf8') # updating orig data by concat
        return messageToAnalyze # return new message with concatonated data
    else:
        print("We don't need padding...")
        return messageToAnalyze # don't need to adjust, we can leave it as it is



# --- Function to print our logo ---
def our_Logo():
    run_at_time = defang_datetime()
    print('Code designed, written & tested by:')
    print('  |                                _ )            |         |          ')
    print('  |      |   |  __ \    _` |       _ \ \          |   _` |  |  /   _ \ ')
    print('  |      |   |  |   |  (   |      ( `  <      \   |  (   |    <    __/ ')
    print(' _____| \__,_| _|  _| \__,_|     \___/\/     \___/  \__,_| _|\_\ \___| ')
    print('Built for ICSI 526 - Spring 2023')
    print(f'Started at: {run_at_time}')

# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime

# --- Function that saves array data to a pickle file - ie encrypted chunks ---
def write_out_data_to_pickle(output_file_name, data_array):
    with open(f'{output_file_name}.pickle', 'wb') as f:
        pickle.dump(data_array, f)

# --- Function that reads array data to a pickle file, prints it ---
def read_data_from_pickle(input_file_name):
    with open(f'{input_file_name}.pickle', 'rb') as f:
        loaded_byte_array = pickle.load(f)
        print(loaded_byte_array)



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Program Startup -- Logo Print Out shows that it is working
our_Logo()



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
    # MSN = b'Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!Hello, world!'
    MSN = b'Hello, world!' # NEEDS TO BE LONGER - USE AUTOKEY This was the original test input - Encrypt message "Hello, world!" with ENCK


# Grabbing the ENCK
ENCK = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
if chooseDebugMode == 'YES':
    print(f'LENGTH OF BLOCK SIZE: {len(ENCK)}')
# If message is shorter than block size, we will adjust it
MSN = do_we_need_padding(MSN,len(ENCK))
print(MSN)
print("\n")


''' GETTING ENCRYPTION DONE '''
encrypted_message_val = encrypt_message(MSN, ENCK)
encrypt_message_hex = encrypted_message_val.hex()

if chooseDebugMode == 'YES':
    print(f"Final result of encryption: {encrypt_message_hex}")

# write to file: (WILL NOT WORK IF IT IS EMPTY)
write_out_data_to_pickle("encryption_normal",encrypted_message_val)

''' Now for Decryption '''
decryptedBoi = decrypt_message(encrypted_message_val,ENCK)
decrypted_HEX_Boi = decryptedBoi.hex()
print(f"FINAL DECRYPTION: {decryptedBoi}")
print("\n")
print(f"FINAL HEX DECRYPTION: {decrypted_HEX_Boi}")

