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


image_bytes = b'this is the end my friend i wish it would bend but we mush make amends because we know ken'
number_Blocks = '16'


''' ENCRYPT '''
# Generate key pairs & Display them
sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()
# Grabbing the ENCK
the_enck = sender_private_key.exchange(ec.ECDH(), receiver_public_key)

# pass data to encryption function
encrypted_blocks = encrypt(str(image_bytes), number_Blocks, the_enck)


print(f"Image Sent: {image_bytes} \n Number Of Blocks: {number_Blocks}")

print('\n')
print(f"Final result of encryption: {encrypted_blocks}")



''' DECRYPT '''
print('\n\n\n')
decrypted_blocks = decrypt(str(encrypted_blocks), number_Blocks)

print(f"Final result of decryption: {decrypted_blocks}")