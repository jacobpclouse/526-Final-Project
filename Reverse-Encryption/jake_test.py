# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import datetime
import pickle
# import random

# encryption imports
from AES import AES
from Alt_N_Bit import generate_key_pair, encrypt, decrypt, split_blocks, create_image_from_bytes
# from Alt_N_Bit import generate_key_pair, pad, encrypt_message, decrypt_message
from cryptography.hazmat.primitives.asymmetric import ec  # For generating initial ec key pair

import numpy as np



# # --- function to store data into a list file for later retrival ---
# def store_list_to_text(inputList,textName):
#     with open(f'{textName}.txt', 'w') as f:
#         for item in inputList:
#             f.write("%s\n" % item)


# # --- function to read data into variable from list, new lines equal new entries in list ---
# def read_list_to_variable(textName):
#     with open(f'{textName}.txt', 'r') as f:
#         my_list = f.read().split(',')

#     print(my_list)
#     return my_list



test_output_name_encryption = 'test_encryption_e.txt'
test_output_name_decryption = 'test_decryption_e.txt'
test_list_name_encryption = 'test_encryption_numpy_array.npy'

image_bytes = 'windows into the soul 111this is the end my friend i wish it would bend but we mush make amends because we know ken this is the end my friend i wish it would bend but we mush make amends because we know ken'
number_Blocks = '16'


''' ENCRYPT '''
print(f"Text Sent: {image_bytes} \n Number Of Blocks: {number_Blocks}")
# Generate key pairs & Display them
sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()
# Grabbing the ENCK
the_enck = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
# print("the_enck: ", the_enck)
# print(f"the_enck length: {len(the_enck)}") # this will be 32

# pass data to encryption function
encrypted_blocks = encrypt(str(image_bytes), number_Blocks, the_enck, test_output_name_encryption)

print('\n')
print(f"Final result of encryption: {encrypted_blocks}")
# print(f"TYPE OF ENCRYPTED RESULT: {type(encrypted_blocks)}")


# Save the array to a file
np.save(test_list_name_encryption, encrypted_blocks)

print('\n')


''' DECRYPT '''
# orig decryption:
# decrypted_blocks = decrypt(encrypted_blocks, number_Blocks, the_enck,test_output_name_decryption)
# enck_from_user = input("enter enck: ").encode()

from_text_encrypted_blocks = np.load(test_list_name_encryption)
decrypted_blocks = decrypt(from_text_encrypted_blocks, number_Blocks, the_enck, test_output_name_decryption)

print(f"** Final result of decryption: {str(decrypted_blocks)}")

