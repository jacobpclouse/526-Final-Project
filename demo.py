import datetime
import pickle

from AES import AES
from Alt_N_Bit import generate_key_pair, encrypt, decrypt
from cryptography.hazmat.primitives.asymmetric import ec  # For generating initial ec key pair


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

    current_datetime = current_datetime.replace(":", "_")
    current_datetime = current_datetime.replace(".", "-")
    current_datetime = current_datetime.replace(" ", "_")

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


if __name__ == '__main__':
    # Program Startup -- Logo Print Out shows that it is working
    our_Logo()

    # Generate key pairs & Display them
    sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

    print('\n')
    print('Sender private key:', sender_private_key.private_numbers().private_value)
    print('Sender public key:', sender_public_key.public_numbers().x)
    print('Receiver private key:', receiver_private_key.private_numbers().private_value)
    print('Receiver public key:', receiver_public_key.public_numbers().x)

    # todo NEEDS TO BE LONGER - USE AUTOKEY This was the original test input - Encrypt message "Hello, world!" with ENCK
    MSN = b'Hello, world!'

    # Grabbing the ENCK
    ENCK = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
    # MSN = pad(MSN, len(ENCK))
    print('\n')
    print(MSN)

    # iv = b'\x01' * 16
    # message = bytes(aes.read_from_file(INPUT_DIRECTORY + filename), encoding='utf-8')
    n_blocks = 16

    ''' GETTING ENCRYPTION DONE: '''
    encrypted_blk = encrypt(MSN, n_blocks, ENCK)
    # todo why convert to hex from binary
    encrypted_hex = b''.join(encrypted_blk).hex()

    print('\n')
    print(f"Final result of encryption: {encrypted_hex}")

    # write to file: (WILL NOT WORK IF IT IS EMPTY)
    write_out_data_to_pickle("encryption_normal", encrypted_blk)

    ''' Now for Decryption '''
    decryptedBoi = decrypt(encrypted_blk, ENCK)
    # # todo again why convert to hex from binary
    decrypted_HEX_Boi = decryptedBoi.hex()
    print('\n')
    print(f"FINAL DECRYPTION: {decryptedBoi}")
    print("\n")
    print(f"FINAL HEX DECRYPTION: {decrypted_HEX_Boi}")