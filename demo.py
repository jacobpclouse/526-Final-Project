# Written by Luna D. and Jacob Clouse for ICSI 526 

# Original Paper -> Alternative N-bit Key Data Encryption for Block Ciphers
# Edited on Windows 10 - may need to be edited if you want to use on Linux/MacOS

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import datetime
import pickle
# import random

from AES import AES
from Alt_N_Bit import generate_key_pair, pad, encrypt_message, decrypt_message
from cryptography.hazmat.primitives.asymmetric import ec  # For generating initial ec key pair

from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify # for web back end
from flask_cors import CORS, cross_origin

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
demo = Flask(__name__)
# demo = Flask(__name__, static_folder='../frontend-alt-n-bit/dist', static_url_path='')
Cors = CORS(demo)
CORS(demo, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
demo.config['CORS_HEADERS'] = 'Content-Type'

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
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



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
'''
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
    MSN = pad(MSN, len(ENCK))
    print('\n')
    print(MSN)

    # GETTING ENCRYPTION DONE:
    encrypted_message_val = encrypt_message(MSN, ENCK)
    # todo why convert to hex from binary
    encrypt_message_hex = encrypted_message_val.hex()

    print('\n')
    print(f"Final result of encryption: {encrypt_message_hex}")

    # write to file: (WILL NOT WORK IF IT IS EMPTY)
    write_out_data_to_pickle("encryption_normal", encrypted_message_val)

    # Now for Decryption
    decryptedBoi = decrypt_message(encrypted_message_val, ENCK)
    # todo again why convert to hex from binary
    decrypted_HEX_Boi = decryptedBoi.hex()
    print('\n')
    print(f"FINAL DECRYPTION: {decryptedBoi}")
    print("\n")
    print(f"FINAL HEX DECRYPTION: {decrypted_HEX_Boi}")
'''

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Route to process encrypted image data
@demo.route('/encrypt-image',methods=['GET', 'POST'])
def encryptedImageFunc():
    title = "Route to process encrypted image data - Alt N Bit Encryption Demo - Luna and Jacob " 


    if request.method == "GET":
    # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status':'success'}
        response_object['message'] ='Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("encryptedImageFunc - Post Request Recieved!")

        message = request.json.get('message')
        number_Blocks = request.json.get('numBlocks')
        sent_text = request.json.get('text')

        # Generate key pairs & Display them
        sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

        # print('\n')
        # print('Sender private key:', sender_private_key.private_numbers().private_value)
        # print('Sender public key:', sender_public_key.public_numbers().x)
        # print('Receiver private key:', receiver_private_key.private_numbers().private_value)
        # print('Receiver public key:', receiver_public_key.public_numbers().x)

        print(message)
        return jsonify(success=True)
    



# Route to process encrypted image data
@demo.route('/encrypt-text',methods=['GET', 'POST'])
def encryptedTextFunc():
    title = "Route to process encrypted text data - Alt N Bit Encryption Demo - Luna and Jacob " 


    if request.method == "GET":
    # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status':'success'}
        response_object['message'] ='Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("encryptedImageFunc - Post Request Recieved!")

        message = request.json.get('message')
        number_Blocks = request.json.get('numBlocks')
        sent_text = request.json.get('text')

        # Generate key pairs & Display them
        sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

        # print('\n')
        # print('Sender private key:', sender_private_key.private_numbers().private_value)
        # print('Sender public key:', sender_public_key.public_numbers().x)
        # print('Receiver private key:', receiver_private_key.private_numbers().private_value)
        # print('Receiver public key:', receiver_public_key.public_numbers().x)

        print(message)
        return jsonify(success=True)





# ********************
# Original route info - DO NOT USE
#*********************
@demo.route('/OLDMAIN',methods=['GET', 'POST'])
def mainIndex():
    dashboardHeader = "Alt N Bit Encryption Demo" # in base temp, basically what this page does
    title = "Alt N Bit Encryption Demo - Luna and Jacob " # in base temp, actual page title in browser
    returned_translated = "Encrypted text will display here"

    if request.method == "GET":
    # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status':'success'}
        response_object['message'] ='Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("Post Request Recieved!")

        message = request.json.get('message')
        number_Blocks = request.json.get('numBlocks')
        sent_text = request.json.get('text')

        # Generate key pairs & Display them
        sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

        print('\n')
        print('Sender private key:', sender_private_key.private_numbers().private_value)
        print('Sender public key:', sender_public_key.public_numbers().x)
        print('Receiver private key:', receiver_private_key.private_numbers().private_value)
        print('Receiver public key:', receiver_public_key.public_numbers().x)


        print(message)
        return jsonify(success=True)
    # return render_template('index.html', html_title = title, dash_head = dashboardHeader, translated = returned_translated)


# Route to test if data was being sent properly
@demo.route('/message1', methods=['POST'])
def receive_message():
    message = request.json.get('message')
    print(message)
    return jsonify(success=True)



# main statement - used to set dev mode
if __name__ == '__main__':
    demo.run(debug=True)


