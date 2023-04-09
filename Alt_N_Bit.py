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
from AES import *

"""Importing Libraries / Modules"""
from cryptography.hazmat.primitives.asymmetric import ec


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


# todo initialize AES appropriately
aes = AES(b'\x00' * 16)
h0 = b'\x01' * 16  # iv


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
    e = hash(msn, h0)

    # Step 2: H1 = HASH(ENCK, H0);
    h1 = hash(enck, h0)

    # Step 3: BLK[0] = e XOR ENCK;
    blocks[0] = xor_bytes(e, enck)

    # Step 4: H1 = HASH(e, H1);
    h1 = hash(e, h1)

    """add padding by n-bits"""
    # # Calculate the number of bytes of padding necessary for the plaintext making it a multiple of the block size
    # padding_len = n - len(msn) % n
    # # Duplicate 16 length to create the padding and convert it to bytes to operate on it in bytes
    # padding = bytes([padding_len] * padding_len)
    # # Add the padding to the plaintext
    # padded_plaintext = msn + padding

    msn_blocks = [padded_plaintext[i:i + n] for i in range(0, len(padded_plaintext), n)]

    # make each ciphertext block dependent on the previous one
    # previous_block = enck

    # Step 5: encrypt each block
    for msn_block in msn_blocks:
        # BLK[x] = blk[x] XOR H1;
        cipher_block = xor_bytes(msn_block, h1)
        blocks.append(cipher_block)

        # H1 = HASH(H1, H1);
        previous_block = h1
        h1 = aes.encrypt_block(previous_block)
    return b''.join(blocks)


# todo integrate approach from paper and review decrypt, convert back to utf-8. Status incomplete
def decrypt(blk, enck, initialization_vector):
    """
    Decrypts `ciphertext` using OFB mode initialization vector (iv).
    blk: encrypted blocks of size n
    enck: key
    """
    blocks = []
    previous = initialization_vector
    for ciphertext_block in blk:
        # OFB mode decrypt: ciphertext XOR encrypt(previous)
        block = aes.encrypt_block(previous)
        plaintext_block = xor_bytes(ciphertext_block, block)
        blocks.append(plaintext_block)
        previous = block

    return b''.join(blocks)
