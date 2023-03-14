import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

# SECP256K1 elliptic curve
curve = ec.SECP256K1()

def generate_key_pair():
    """Generate sender and receiver key pairs"""
    sender_private_key = ec.generate_private_key(curve)
    sender_public_key = sender_private_key.public_key()
    receiver_private_key = ec.generate_private_key(curve)
    receiver_public_key = receiver_private_key.public_key()
    return sender_private_key, sender_public_key, receiver_private_key, receiver_public_key

def encrypt_message(MSN, ENCK):
    """Encrypt message using ENCK"""
    # Step 1: Hash message and store in e
    e = hashlib.sha256(MSN).digest()

    # Step 2: Hash ENCK and store in H1
    # H1 = hashlib.sha256(ENCK.to_bytes(32, 'big')).digest()
    ENCK_bytes = ENCK.to_bytes(32, 'big')
    H1 = hashlib.sha256(ENCK_bytes).digest()


    # Step 3: Encrypt e with ENCK and store in BLK[0]
    block_size = len(ENCK.to_bytes(32, 'big'))
    BLK = [e[i:i+block_size] for i in range(0, len(e), block_size)]
    BLK[0] = bytes([BLK[0][i] ^ ENCK.to_bytes(32, 'big')[i] for i in range(block_size)])

    # Step 4: Hash e using H1 as initialization vector and store in H1
    H1 = hashlib.sha256(e, H1).digest()

    # Step 5: Encrypt n blocks of MSN using different keys
    n = len(MSN) // len(BLK[0])
    encrypted_blocks = []
    for i in range(n):
        key = H1
        if i > 0:
            key = hashlib.sha256(key).digest()
        block = MSN[i*len(BLK[0]):(i+1)*len(BLK[0])]
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_block = encryptor.update(block) + encryptor.finalize()
        encrypted_blocks.append(encrypted_block)
        H1 = hashlib.sha256(encrypted_block, H1).digest()

    return b''.join(encrypted_blocks)

# Example usage
if __name__ == '__main__':
    # Generate key pairs
    sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()
    print('Sender private key:', sender_private_key.private_numbers().private_value)
    print('Sender public key:', sender_public_key.public_numbers().x)
    print('Receiver private key:', receiver_private_key.private_numbers().private_value)
    print('Receiver public key:', receiver_public_key.public_numbers().x)

    # Encrypt message "Hello, world!" with ENCK
    MSN = b'Hello, world!'
    ENCK = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
    encrypted_message = encrypt_message(MSN, ENCK)

    # Print encrypted message
    print('Encrypted message:', encrypted_message.hex())
