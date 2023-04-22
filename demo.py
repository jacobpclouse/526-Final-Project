# Written by Luna D. and Jacob Clouse for ICSI 526 

# Original Paper -> Alternative N-bit Key Data Encryption for Block Ciphers
# Edited on Windows 10 - may need to be edited if you want to use on Linux/MacOS

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

# Backend imports 
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, \
    jsonify  # for web back end
from flask_cors import CORS, cross_origin

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
demo = Flask(__name__)
# without cors, app will refuse the requests from the frontend
Cors = CORS(demo)
CORS(demo, resources={r'/*': {'origins': '*'}}, CORS_SUPPORTS_CREDENTIALS=True)
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
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

''' ENCRYPTION '''


# Route to process encrypted image data ** NEED TO STORE AS BLOB IN UPLOADS
@demo.route('/encrypt-image', methods=['GET', 'POST'])
def encryptedImageFunc():
    # todo do image encryption
    global image_bytes
    title = "Route to process encrypted image data - Alt N Bit Encryption Demo - Luna and Jacob "

    # do something with the image bytes here
    if request.method == "GET":
        # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status': 'success'}
        response_object['message'] = 'Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("encryptedImageFunc - Post Request Recieved!")

        # number_Blocks = request.json.get('numBlocks')
        # sent_image = request.json.get('image')  # NEED TO ADJUST FOR THE BLOB

        number_Blocks = request.json.get('numBlocks')

        # check if the post request has the file part
        if 'image' not in request.files:
            return 'No image uploaded', 400

        # get the file object from the request
        file = request.files['image']

        # read the bytes from the file object
        image_bytes = file.read()

        # Generate key pairs & Display them
        sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()
        # Grabbing the ENCK
        the_enck = sender_private_key.exchange(ec.ECDH(), receiver_public_key)

        # pass data to encryption function
        encrypted_blocks = encrypt(str(image_bytes), number_Blocks, the_enck)

        # print('\n')
        # print('Sender private key:', sender_private_key.private_numbers().private_value)
        # print('Sender public key:', sender_public_key.public_numbers().x)
        # print('Receiver private key:', receiver_private_key.private_numbers().private_value)
        # print('Receiver public key:', receiver_public_key.public_numbers().x)

        print(f"Image Sent: {image_bytes} \n Number Of Blocks: {number_Blocks}")

        print('\n')
        print(f"Final result of encryption: {encrypted_blocks}")

        # write to file: (WILL NOT WORK IF IT IS EMPTY)
        write_out_data_to_pickle("encryption_normal", encrypted_blocks)

        return create_image_from_bytes(image_bytes), 200

        # return jsonify(success=True)

# Route to process encrypted image data
@demo.route('/encrypt-text', methods=['GET', 'POST'])
def encryptedTextFunc():
    title = "Route to process encrypted text data - Alt N Bit Encryption Demo - Luna and Jacob "

    if request.method == "GET":
        # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status': 'success'}
        response_object['message'] = 'Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("encryptedImageFunc - Post Request Recieved!")

        number_Blocks = request.json.get('numBlocks')
        msn_text = request.json.get('text')

        # Generate key pairs & get ENK
        sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()
        # Grabbing the ENCK
        the_enck = sender_private_key.exchange(ec.ECDH(), receiver_public_key)

        # pass data to encryption function
        encrypted_blocks = encrypt(str(msn_text), number_Blocks, the_enck)

        print('\n')
        print(f"Final result of encryption: {encrypted_blocks}")

        # write to file: (WILL NOT WORK IF IT IS EMPTY)
        write_out_data_to_pickle("encryption_normal", encrypted_blocks)

        print(f"Text Sent: {msn_text} \n Number Of Blocks: {number_Blocks}")
        return b''.join(encrypted_blocks).hex(), 200

        # return data to the frontend - add just returning a blob or a file
        # encrypted_blocks_for_Frontend = [b.decode('utf-8') for b in encrypted_blocks]
        # return encrypted_blocks_for_Frontend


''' DECRYPTION '''


# Route to decrypt image data ** NEED TO STORE AS BLOB IN UPLOADS
@demo.route('/decrypt-image', methods=['GET', 'POST'])
def decryptedImageFunc():
    title = "Route to decrypt image data - Alt N Bit Encryption Demo - Luna and Jacob "

    if request.method == "GET":
        # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status': 'success'}
        response_object['message'] = 'Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("decryptedImageFunc - Post Request Recieved!")

        number_Blocks = request.json.get('numBlocks')
        # sent_image = request.json.get('image')  # NEED TO ADJUST FOR THE BLOB
        # check if the post request has the file part
        if 'image' not in request.files:
            return 'No image uploaded', 400

        # get the file object from the request
        file = request.files['image']

        # read the bytes from the file object
        image_bytes = file.read()

        # Generate key pairs & Display them
        # sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

        # print('\n')
        # print('Sender private key:', sender_private_key.private_numbers().private_value)
        # print('Sender public key:', sender_public_key.public_numbers().x)
        # print('Receiver private key:', receiver_private_key.private_numbers().private_value)
        # print('Receiver public key:', receiver_public_key.public_numbers().x)

        decrypted_blocks = decrypt(str(image_bytes), number_Blocks)

        print(f"Image Sent: {image_bytes} \n Number Of Blocks: {number_Blocks}")
        # return jsonify(success=True)
        return decrypted_blocks


# Route to decrypt image data
@demo.route('/decrypt-text', methods=['GET', 'POST'])
def decryptedTextFunc():
    title = "Route to decrypt text data - Alt N Bit Encryption Demo - Luna and Jacob "

    if request.method == "GET":
        # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status': 'success'}
        response_object['message'] = 'Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("decryptedTextFunc - Post Request Recieved!")

        number_Blocks = request.json.get('numBlocks')
        sent_text = request.json.get('text')

        # Generate key pairs & Display them
        # sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

        # print('\n')
        # print('Sender private key:', sender_private_key.private_numbers().private_value)
        # print('Sender public key:', sender_public_key.public_numbers().x)
        # print('Receiver private key:', receiver_private_key.private_numbers().private_value)
        # print('Receiver public key:', receiver_public_key.public_numbers().x)

        decrypted_blocks = decrypt(str(sent_text), number_Blocks)

        print(f"Text Sent: {sent_text} \n Number Of Blocks: {number_Blocks}")

        return decrypted_blocks





# # Route to test if data was being sent properly
# @demo.route('/message1', methods=['POST'])
# def receive_message():
#     message = request.json.get('message')
#     print(message)
#     return jsonify(success=True)


# -------------------------------------
# main statement - used to set dev mode and do auto reloading - remove this before going to production
# -------------------------------------
if __name__ == '__main__':
    demo.run(debug=True)
