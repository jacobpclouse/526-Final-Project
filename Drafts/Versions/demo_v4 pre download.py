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
from Alt_N_Bit import generate_key_pair, encrypt, decrypt, split_blocks, create_image_from_bytes, write_to_file
from cryptography.hazmat.primitives.asymmetric import ec  # For generating initial ec key pair

# Backend imports 
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file, make_response,\
    jsonify  # for web back end
from flask_cors import CORS, cross_origin

# moving files and folders
import shutil
import os
import numpy as np # used to store actual encrypted data in a file and retrieve it
import zipfile

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
demo = Flask(__name__)
# without cors, app will refuse the requests from the frontend
Cors = CORS(demo)
CORS(demo, resources={r'/*': {'origins': '*'}}, CORS_SUPPORTS_CREDENTIALS=True)
demo.config['CORS_HEADERS'] = 'Content-Type'

# array and data names:
test_list_name_encryption = 'test_encryption_numpy_array.npy'
the_enck_value = 'the_enck_val.bin'

# Text file names
e_encryption_text_output_name = 'e_val_from_text_encryption.txt'
e_decryption_text_output_name = 'e_val_from_text_decryption.txt'
numpy_encryption_text_name = 'numpy_encryption_text_data.npy'
the_enck_text_name = 'the_enck_text_data.bin'
text_zip = 'text_zip.zip'


# Image File names
e_encryption_image_output_name = 'e_val_from_image_encryption.txt'
e_decryption_image_output_name = 'e_val_from_image_decryption.txt'
numpy_encryption_image_name = 'numpy_encryption_image_data.npy'
the_enck_image_name = 'the_enck_image_data.bin'
image_zip = 'image_zip.zip'


# File Paths
path_to_uploads = 'UPLOADS'


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


# --- Function to store data into a bin file for later retrival ---
def store_the_enck_bin(value,filename):
    with open(filename, 'wb') as file:
        file.write(value)
    file.close()


# --- Function to read data into variable from bin ---
def read_enck_to_variable(textName):
    with open(textName, 'rb') as f:
        my_bytes_object = f.read()
    return my_bytes_object


# --- Function to empty out a directory ---
def clean_out_directory(folderPath):
    for filename in os.listdir(folderPath):
        filePath = os.path.join(folderPath, filename)
        try:
            if os.path.isfile(filePath):
                os.unlink(filePath)
        except Exception as e:
            print(f"Failed to delete {filePath} due to {e}")


# --- Function to check and see if a directory exists and, if not, create that directory ---
def create_folder(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)


# -- Function that takes zip name and then an array of files to zip
def zip_files(zip_name, files_to_zip):
    with zipfile.ZipFile(zip_name, 'w') as zip_file:
        # Add each file to the zip file
        for file_path in files_to_zip:
            # Add the file to the zip file with its original name
            zip_file.write(file_path, arcname=file_path.split('/')[-1])


# --- Function that unzips files from zip file ---
def unzip_files(zip_name):
    # Create a ZipFile object with the name of the zip file and mode 'r' for read
    with zipfile.ZipFile(zip_name, mode='r') as zip_obj:
        # Print a list of all files in the zip file
        print("Files in zip file:")
        for file_name in zip_obj.namelist():
            print(f"- {file_name}")
        # Extract all files to the current working directory
        zip_obj.extractall()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

''' ENCRYPTION '''

'''TO DO!!!'''
# Route to process encrypted image data ** NEED TO STORE AS BLOB IN UPLOADS
@demo.route('/encrypt-image', methods=['GET', 'POST'])
def encryptedImageFunc():
    # todo do image encryption
    global image_bytes
    title = "Route to process encrypted image data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)

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
        print(f"Image Sent: {image_bytes} \n Number Of Blocks: {number_Blocks}")
        
        # Generate key pairs & Display them
        sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

        # Grabbing the ENCK - This needs to be given to the user as a key in order to retrieve their data
        the_enck = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
        
        # pass data to encryption function
        encrypted_blocks = encrypt(str(image_bytes), number_Blocks, the_enck, e_encryption_image_output_name )

        # store enck, store encrypted block data, and move files to the uploads folder for zipping
        # first enck 
        store_the_enck_bin(the_enck,the_enck_image_name)
        shutil.move(the_enck_image_name, path_to_uploads)
        # second encrypted blocks array
        np.save(numpy_encryption_image_name, encrypted_blocks)
        shutil.move(numpy_encryption_image_name, path_to_uploads)


        # zip and return the file to the users

        # clean out the directory:
        clean_out_directory(path_to_uploads)



        print('\n')
        print(f"Final result of encryption: {encrypted_blocks}")

        return create_image_from_bytes(image_bytes), 200

        # return jsonify(success=True)


# Route to process encrypted text data
@demo.route('/encrypt-text', methods=['GET', 'POST'])
def encryptedTextFunc():
    title = "Route to process encrypted text data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)

    if request.method == "GET":
        # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status': 'success'}
        response_object['message'] = 'Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("encryptedTextFunc - Post Request Recieved!")

        number_Blocks = request.json.get('numBlocks')
        msn_text = request.json.get('text')
        print(f"Text Sent: {msn_text} \n Number Of Blocks: {number_Blocks}")

        # Generate key pairs & get ENK
        sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

        # Grabbing the ENCK
        the_enck = sender_private_key.exchange(ec.ECDH(), receiver_public_key)

        # pass data to encryption function
        encrypted_blocks = encrypt(str(msn_text), number_Blocks, the_enck, e_encryption_text_output_name)

        # store enck, store encrypted block data, and move files to the uploads folder for zipping
        # first enck, second encrypted blocks array
        store_the_enck_bin(the_enck,the_enck_text_name)
        np.save(numpy_encryption_text_name, encrypted_blocks)
        # zip to downloads
        zip_files(text_zip,[the_enck_text_name,numpy_encryption_text_name])
        # then move them to the uploads
        shutil.move(the_enck_text_name, path_to_uploads)
        shutil.move(numpy_encryption_text_name, path_to_uploads)
        # shutil.move(text_zip, path_to_uploads) # return this to user before moving it


        # zip and return the file to the users

        # clean out the directory:
        clean_out_directory(path_to_uploads)



        print('\n')
        print(f"Final result of encryption: {encrypted_blocks}")
        # return b''.join(encrypted_blocks).hex(), 200
        return ''.join(encrypted_blocks), 200


        # return data to the frontend - add just returning a blob or a file
        # encrypted_blocks_for_Frontend = [b.decode('utf-8') for b in encrypted_blocks]
        # return encrypted_blocks_for_Frontend


''' DECRYPTION '''

'''TO DO!!!'''
# Route to decrypt image data ** NEED TO STORE AS BLOB IN UPLOADS
@demo.route('/decrypt-image', methods=['GET', 'POST'])
def decryptedImageFunc():
    title = "Route to decrypt image data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)

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
        print(f"Image Sent: {image_bytes} \n Number Of Blocks: {number_Blocks}")
        # read the bytes from the file object
        image_bytes = file.read()
        # you need to get the original enck value from the user to decrypt the whole thing


        # decrypted_blocks = decrypt(str(image_bytes), number_Blocks)
        decrypted_blocks = decrypt(image_bytes, number_Blocks)

        
        # return jsonify(success=True)
        return decrypted_blocks


'''TO DO!!!'''
# Route to decrypt image data
@demo.route('/decrypt-text', methods=['GET', 'POST'])
def decryptedTextFunc():
    title = "Route to decrypt text data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)

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
        print(f"Text Sent: {sent_text} \n Number Of Blocks: {number_Blocks}")
        # you need to get the original enck value from the user to decrypt the whole thing
        

        # decrypted_blocks = decrypt(str(sent_text), number_Blocks)
        decrypted_blocks = decrypt(sent_text, number_Blocks)

        

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
