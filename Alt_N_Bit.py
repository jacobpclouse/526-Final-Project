"""
@authors Luna Dagci and Jacob Clouse
ICSI 526 Project: Alternative N-bit Key Data Encryption for Block Ciphers

Typically, block ciphers operate on data blocks of fixed size (e.g., 64 or 128 bits), and the key used to encrypt
the data must also be of a fixed size (e.g., 128 or 256 bits). This means that if a user wants to encrypt data
with a key size that is not a multiple of the block size, they would have to pad the data, which can be
inefficient and can weaken the security of the encryption.

The proposed approach in this paper overcomes this limitation by first hashing the key to produce a longer key,
which is then split into multiple subkeys. Each subkey is used to encrypt a block of data, and the resulting ciphertext
is concatenated to form the final encrypted message.

The authors demonstrate that this approach can provide secure encryption for arbitrary key sizes without
sacrificing performance or security. They also show that the approach can be easily integrated with
existing block ciphers, making it a practical solution for real-world encryption applications.

We are using AES block cipher (OFB operation) to integrate the innovative approach in our solution

"""
import hashlib

from PIL import Image

from AES import *
import io

"""Importing Libraries / Modules"""
from cryptography.hazmat.primitives.asymmetric import ec  # For generating initial ec key pair

# write a value to a file
def write_to_file(value,filename):
    with open(filename, "w") as file:
        file.write(str(value))
    file.close()

def generate_key_pair():
    """
    Function to Generate sender and receiver key pairs --- This code was sourced from Line 22 of Provable Things
    encrypted-queries (EC example): https://github.com/provable-things/encrypted-queries/blob/master/tools/encrypted_queries_tools.py
    """
    # SECP256K1 elliptic curve
    curve = ec.SECP256K1()

    sender_private_key = ec.generate_private_key(curve)
    sender_public_key = sender_private_key.public_key()
    receiver_private_key = ec.generate_private_key(curve)
    receiver_public_key = receiver_private_key.public_key()
    return sender_private_key, sender_public_key, receiver_private_key, receiver_public_key


def split_blocks(msn, n_bits, n_blocks):
    # n blocks needs to be an integer for this to work
    n_blocks = int(n_blocks)
    return [msn[i:i + n_bits] for i in range(0, len(msn), n_blocks)]


# todo initialize AES appropriately
aes = AES(b'\x00' * 16)
h0 = b'\x01' * 16  # iv
# print(f"h0: {h0}")

def create_image_from_bytes(image_bytes):
    # create an in-memory stream of the image bytes
    stream = io.BytesIO(image_bytes)

    # open the image using Pillow
    image = Image.open(stream)

    # do something with the image here, such as resizing or applying filters
    # for example, to resize the image to 500x500 pixels:
    # image = image.resize((500, 500))

    # save the modified image to a new in-memory stream
    output_stream = io.BytesIO()
    image.save(output_stream, format='PNG')

    # get the bytes from the output stream
    output_bytes = output_stream.getvalue()

    # return the bytes of the new image
    return output_bytes

def read_image_bytes(filename):
    with open(filename, 'rb') as f:
        image_bytes = f.read()
    return image_bytes

# todo integrate approach from paper: review encrypt. Status incomplete
def encrypt(msn, n, enck, name_e_File_encrypted):
    """
    msn: message
    n: number of blocks
    enck: key
    name_e_File_encrypted: name of file of stored e value
    """

    """"""

    blocks = []

    # Step 1: e = HASH(MSN, H0);
    print("msn type of: ",type(msn))
    print("h0 type of: ",type(h0))
    print("enck type of: ",type(enck))

    '''MAKE IT SO THAT WE CAN CUT THE SIZE OF THE ENCK SO IF N IS LESS THAN THE LENGHT OF IT, WE CUT IT DOWN TO THE LENGTH OF N'''

    # split the msn into the number of n blocks here ***
    msn_chunks = []
    for i in range(0, len(msn), len(enck)):
        chunk = msn[i:i+len(enck)]
        msn_chunks.append(chunk)
    # print(msn_chunks)

    # h0 is a public constant, needs to be provided
    # e = hashlib.sha256(msn + h0).hexdigest()
    e = hashlib.sha256(msn_chunks[0].encode()).hexdigest() # temporarily removing h0 for testing
    # write_to_file(e,'e_in_encryption.txt')
    write_to_file(e,name_e_File_encrypted)

    # Step 2: H1 = HASH(ENCK, H0);
    h1 = hashlib.sha256(enck).hexdigest() # temporarily removing h0 for testing
    # print(f"h1 origin = {h1}")
    # print(f"h1 string = {str(h1)}")

    # print("Length of e: ", len(e))
    # print("Length of enck: ", len(enck))
    # print("Length of h1: ", len(h1))

    # Step 3: BLK[0] = e XOR ENCK;
    ''' YOU MIGHT HAVE TO USE H1 HERE INSTEAD OF ENCK'''
    xored = ""
    for i in range(len(e)):
        intial_xor = ord(e[i]) ^ ord(h1[i])
        xored += chr(intial_xor)
    blocks.append(xored)


    # Step 4: H1 = HASH(e, H1);
    # print(f'type of e: {type(e)}')
    # print(f'type of h1: {type(h1)}')
    concat_e_h1 = (e + h1).encode()
    h1 = hashlib.sha256(concat_e_h1).hexdigest()


    # Step 5: encrypt each block
    for msn_block_no in range(0,len(msn_chunks),1):
        
        # BLK[x] = blk[x] XOR H1;
        current_block = msn_chunks[msn_block_no]
        # print(f"MSN block: {current_block}")
        # print(f"MSN block length: {len(current_block)}")
        cipher_block = ""
        for i in range(len(current_block)):
            cipher_block += chr(ord(current_block[i]) ^ ord(h1[i]))
        blocks.append(cipher_block)

        # H1 = HASH(H1, H1);
        h1 = hashlib.sha256((h1+h1).encode()).hexdigest()

    print(len(blocks) == len(msn))
    return blocks


# todo integrate approach from paper and review decrypt, convert back to utf-8. Status incomplete
# encoding strings with utf8 might be needed to combine bytes and strings
def decrypt(blk, n, enck, name_e_File_decrypted):
    """
    blk: encrypted blocks of size n
    n: blocks size
    enck: key

    """
    
    print("blk type of: ",type(blk))
    print("h0 type of: ",type(h0))
    print("enck type of: ",type(enck))
    blocks = []

    # Step 1: H1 = HASH(ENCK, H0)
    # h1 = hashlib.sha256(enck + h0).hexdigest()
    h1 = hashlib.sha256(enck).hexdigest() # temp not using h0
    
    # print(f'Length of blk[0]: {len(blk[0])}')
    # print(f'Length of enck: {len(enck)}')
    # print(f'ENCK: {enck}')

    # print(f"blk: {blk}")
    # print(len(blk))


    # Step 2: e = BLK[0] XOR ENCK;
    initial_block = blk[0]
    print(initial_block)
    e = ""
    for i in range(len(blk[0])):
        initial_xor = ord(initial_block[i]) ^ ord(h1[i])
        e += chr(initial_xor)
    # e = xor_bytes(blk[0], enck)
    # write_to_file(e,'e_in_decryption.txt')
    write_to_file(e,name_e_File_decrypted)

    # Step 3: H1 = HASH(e, H1);
    # print("* e type of: ",type(e))
    # print("* h1 type of: ",type(h1))
    h1 = hashlib.sha256((e + h1).encode()).hexdigest()
    # print(e)



    # Step 4:
    
    for ciphertext_block in range(1,len(blk),1):
        # blk[x] = BLK[x] XOR H1;
# --
        current_block = blk[ciphertext_block]
        # print(f"MSN block: {current_block}")
        # print(f"MSN block length: {len(current_block)}")
        plaintext_block = ""
        for i in range(len(current_block)):
            plaintext_block += chr(ord(current_block[i]) ^ ord(h1[i]))
        blocks.append(plaintext_block)

        # H1 = HASH(H1, H1);
        h1 = hashlib.sha256((h1+h1).encode()).hexdigest()


    

    # return b''.join(blocks)
    # print(f"Finally: {str(blocks)}")
    return str(blocks)