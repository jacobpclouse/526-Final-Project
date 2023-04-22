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
from cryptography.hazmat.primitives.asymmetric import ec

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
print(f"h0: {h0}")

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
def encrypt(msn, n, enck):
    """
    msn: message
    n: number of blocks
    enck: key
    """

    """"""

    blocks = []

    # Step 1: e = HASH(MSN, H0);
    print("msn type of: ",type(msn))
    print("h0 type of: ",type(h0))
    print("enck type of: ",type(enck))


    
    # h0 is a public constant, needs to be provided
    e = hashlib.sha256(msn.encode() + h0).digest()
    #e = hashlib.sha256(msn.encode() + h0).hexdigest()
    write_to_file(e,'e_in_encryption.txt')

    # Step 2: H1 = HASH(ENCK, H0);
    h1 = hashlib.sha256(enck + h0).digest()
    # h1 = hashlib.sha256(enck + h0).hexdigest()



    # Step 3: BLK[0] = e XOR ENCK;
    blocks.append(xor_bytes(e, enck))


    # Step 4: H1 = HASH(e, H1);
    # print(f'type of e: {type(e)}')
    # print(f'type of h1: {type(h1)}')
    h1 = hashlib.sha256(e + h1).digest()
    # h1 = hashlib.sha256((e + h1).encode()).hexdigest()


    # Step 5: encrypt each block
    for msn_block in split_blocks(msn, len(enck), n):
        # BLK[x] = blk[x] XOR H1;
        cipher_block = xor_bytes(msn_block, h1)
        blocks.append(cipher_block)

        # H1 = HASH(H1, H1);
        h1 = hashlib.sha256(h1+h1).digest()
        # h1 = hashlib.sha256((h1+h1).encode()).hexdigest()

    print(len(blocks) == len(msn))
    return blocks


# todo integrate approach from paper and review decrypt, convert back to utf-8. Status incomplete
# encoding strings with utf8 might be needed to combine bytes and strings
def decrypt(blk, enck):
    """
    blk: encrypted blocks of size n
    enck: key
    """
    # h0 = ''
    # h0_decoded = h0.decode()
    # inputForH1 = enck + h0
    # Step 1: H1 = HASH(ENCK, H0)
    print("blk type of: ",type(blk))
    print("h0 type of: ",type(h0))
    print("enck type of: ",type(enck))
    
    h1 = hashlib.sha256(enck.encode() + h0).digest()
    # h1 = hashlib.sha256(enck.encode() + h0).hexdigest()
    

    # Step 2: e = BLK[0] XOR ENCK;
    e = xor_bytes(blk[0], enck)
    write_to_file(e,'e_in_decryption.txt')

    # Step 3: H1 = HASH(e, H1);
    # print("* e type of: ",type(e))
    # print("* h1 type of: ",type(h1))
    h1 = hashlib.sha256(e + h1).digest()
    # h1 = hashlib.sha256(e + h1.encode()).hexdigest()

    # Step 4:
    blocks = []
    for ciphertext_block in blk:
        # blk[x] = BLK[x] XOR H1;
        plaintext_block = xor_bytes(ciphertext_block, h1)
        blocks.append(plaintext_block)

        # H1 = HASH(H1, H1);
        h1 = hashlib.sha256(h1+h1).digest()
        # h1 = hashlib.sha256((h1+h1).encode()).hexdigest()
    
    # revert from hex
    # from_hex_blocks = []
    # for hexVal in blocks:
    #     de_hexed = bytes.fromhex(hexVal)
    #     # de_hexed = hexVal.decode()
    #     from_hex_blocks.append(de_hexed)
    #     # print(de_hexed)
    

    return b''.join(blocks)
    # return from_hex_blocks