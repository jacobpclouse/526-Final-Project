# Written by Luna D. and Jacob Clouse for ICSI 526 

# Original Paper -> Alternative N-bit Key Data Encryption for Block Ciphers
# Edited on Windows 10 - may need to be edited if you want to use on Linux/MacOS

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import datetime
from distutils import extension
import io

from PIL import Image

# import random

# encryption imports
from AES import AES
from Alt_N_Bit import generate_key_pair, encrypt, decrypt, split_blocks, create_image_from_bytes, read_image_bytes, decryptImage,write_to_file
from cryptography.hazmat.primitives.asymmetric import ec  # For generating initial ec key pair

# Backend imports 
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, send_file, make_response,Response,\
    jsonify  # for web back end
from flask_cors import CORS, cross_origin
import base64
import json
from io import BytesIO
import builtins

# moving files and folders
import shutil # used to move files around and clean folders
import os
import numpy as np # used to store actual encrypted data in a file and retrieve it
import zipfile # used in zipping images
import glob 
import uuid # get extensions for images
import magic # used to get mime data for the image


# shamir Secret Sharing stuff
from sss import sss_question2
from sss.homomorphism_question2 import downscale_shares, generate_shares, reconstruct_downscaled
from sss.sss_question2 import read_grayscale_pixels

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
np.set_printoptions(threshold=np.inf)
demo = Flask(__name__)
# without cors, app will refuse the requests from the frontend
Cors = CORS(demo)
CORS(demo, resources={r'/*': {'origins': '*'}}, CORS_SUPPORTS_CREDENTIALS=True)
demo.config['CORS_HEADERS'] = 'Content-Type'

# array and data names:
test_list_name_encryption = 'test_encryption_numpy_array.npy'
the_enck_value = 'the_enck_val.bin'

# Text file names
# e_encryption_text_output_name = 'e_val_from_text_encryption.txt'
# e_decryption_text_output_name = 'e_val_from_text_decryption.txt'
numpy_encryption_text_name = 'numpy_encryption_text_data.npy'
the_enck_text_name = 'the_enck_text_data.bin'
text_zip = 'text_zip.zip'


# Image File names

mime_data_encryption_image= 'mime_data_encryption_image_data.txt'
numpy_encryption_image_name = 'numpy_encryption_image_data.npy'
CIPHER_encryption_image_name = 'cipher_encryption_image_data.cipher'
the_enck_image_name = 'the_enck_image_data.bin'
shape_of_numpy_encryption = 'shape_numpy_encryption_image_data.shape'
image_zip = 'image_zip.zip'
TEMP_IMAGE_FILENAME = 'uploaded_unencrypted_image'
OUTBOUND_DECRYPTED_IMAGE_FILENAME = 'decrypted_image'


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


# --- Function to get the mimedata of an uploaded image for encryption ---
def get_image_mime_data(targetImage,outputFileName):
    mime_data = magic.from_file(targetImage, mime=True) # grab mime data
    with open(outputFileName, 'w') as mime_file:# Save the mime data to a file
        mime_file.write(mime_data)

# --- Function to remove unneeded zip files ---
def delete_zip_file(extraZip):
    if os.path.exists(extraZip) and extraZip.endswith('.zip'):
        os.remove(extraZip)
        print(f"{extraZip} has been deleted.")

# --- Function to get extension for retrieval --
def need_extension(filename):
    name, extension = filename.split(".")
    upperCaseExt = extension.upper()  
    print(upperCaseExt)
    return upperCaseExt

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

''' ENCRYPTION '''

# todo test & review header not intact
'''TO DO!!!'''
# Route to process encrypted image data ** NEED TO STORE AS BLOB IN UPLOADS
@demo.route('/encrypt-image', methods=['GET', 'POST'])
def encryptedImageFunc():
    # todo do image encryption
    global image_bytes
    title = "Route to process encrypted image data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)
    # clean out the directory and extra zips:
    clean_out_directory(path_to_uploads)
    delete_zip_file(image_zip)
    delete_zip_file(text_zip)

    # do something with the image bytes here
    if request.method == "GET":
        # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status': 'success'}
        response_object['message'] = 'Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("encryptedImageFunc - Post Request Recieved!")

        # read in number of blocks -- un needed
        # number_Blocks = request.json.get('numBlocks')
        # enck = request.json.get('enck')
        number_Blocks = 32 # TEMP - getting this from the user causes a 400 bad request error


        # check if the post request has the file part
        if 'image' not in request.files:
            print("No image uploaded")
            return 'No image uploaded', 400

        # get the file object from the request
        file = request.files['image']

        # store image temp
        # DONOTUSE_file_name, extension = os.path.splitext(file.filename)
        extension = need_extension(file.filename)
        temp_image_name_internal = f"{TEMP_IMAGE_FILENAME}.{extension}"
        file.save(temp_image_name_internal)
        orig_name = file.filename
  
        # Generate key pairs & Display them
        sender_private_key, sender_public_key, receiver_private_key, receiver_public_key = generate_key_pair()

        # Grabbing the ENCK - This needs to be given to the user as a key in order to retrieve their data
        the_enck = sender_private_key.exchange(ec.ECDH(), receiver_public_key)

        
        # # print(f"Image Sent: {image_bytes} \n Number Of Blocks: {number_Blocks}")


        # Open the image file as a binary file
        with open(temp_image_name_internal, "rb") as image_file:
            # Read the contents of the image file as a sequence of bytes
            image_bytes = image_file.read()
        
        # Create a PIL Image object from the bytes
        image = Image.open(io.BytesIO(image_bytes))
        # Convert the PIL Image object to a numpy array
        image_array = np.array(image)
        # image_array = np.clip(np.array(image), -np.inf, np.inf)
        # flattened_arr = image_array.flatten()

        # # Save the shape of the array to a file
        # with open(shape_of_numpy_encryption, 'w') as f:
        #     f.write(','.join(map(str, image_array.shape)))
        #     image_array.tofile(f, sep=',', format='%d')
        with open(shape_of_numpy_encryption, 'w') as f:
            f.write(str(image_array.shape))


        
        # pass data to encryption function
        # encrypted_blocks = encrypt(str(image_bytes), number_Blocks, the_enck, e_encryption_image_output_name )
        encrypted_blocks = encrypt(str(image_array), the_enck)
        # encrypted_blocks = encrypt(str(flattened_arr), the_enck)

        # store enck data and encrypted data into files for zipping
        store_the_enck_bin(the_enck,the_enck_image_name)
        np.save(numpy_encryption_image_name, encrypted_blocks)
        print(f"Image Shape: {image_array.shape}")
        # get_image_mime_data(temp_image_name_internal,mime_data_encryption_image)
        write_to_file(extension,mime_data_encryption_image) # just store extension into a file
        print(type(encrypted_blocks))
        print(type(encrypted_blocks[0]))
        big_byte = ''.join(encrypted_blocks)
        # print(big_byte)
        with open(CIPHER_encryption_image_name, 'wb') as bytes_file_output:
            bytes_file_output.write(big_byte.encode())

        
        # zip and return the file to the users
        # zip_files(image_zip,[the_enck_image_name,numpy_encryption_image_name,mime_data_encryption_image])
        zip_files(image_zip,[the_enck_image_name,CIPHER_encryption_image_name,mime_data_encryption_image,numpy_encryption_image_name,shape_of_numpy_encryption])

        # move data to uploads for removal
        shutil.move(the_enck_image_name, path_to_uploads)
        shutil.move(numpy_encryption_image_name, path_to_uploads)
        shutil.move(mime_data_encryption_image, path_to_uploads)
        shutil.move(temp_image_name_internal, path_to_uploads)
        shutil.move(CIPHER_encryption_image_name, path_to_uploads)

        # this goes after move with shutil to uploads
        # # files_to_zip = [the_enck_image_name,numpy_encryption_image_name,mime_data_encryption_image]
        # # os.chdir(path_to_uploads)
        # old_name_zip = shutil.make_archive(image_zip, "zip", root_dir=path_to_uploads)
        # # rename the original zip file
        # os.rename(old_name_zip, image_zip)



        # clean out the directory:
        # clean_out_directory(path_to_uploads)

        print('\n')
        print(f"Image {orig_name} has been encrypted!")
        # print(f"Final result of encryption: {encrypted_blocks}")
        return send_file(image_zip, as_attachment=True)
        # # get mime data for original image
        # image_data = io.BytesIO(image_bytes)
        # image = Image.open(image_data)

        # # todo send the image and get image from frontend

        # return send_file(image, as_attachment=True)
        # # return jsonify(success=True)


# Route to process encrypted text data
@demo.route('/encrypt-text', methods=['GET', 'POST'])
def encryptedTextFunc():
    title = "Route to process encrypted text data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)
    # if it exists, clean it out
    clean_out_directory(path_to_uploads)
    delete_zip_file(image_zip)
    delete_zip_file(text_zip)

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
        # encrypted_blocks = encrypt(str(msn_text), number_Blocks, the_enck, e_encryption_text_output_name)
        encrypted_blocks = encrypt(str(msn_text), the_enck)

        print('\n')
        print(f"Final result of encryption: {encrypted_blocks}")

        # store enck, store encrypted block data, and move files to the uploads folder for zipping
        # first enck, second encrypted blocks array
        store_the_enck_bin(the_enck,the_enck_text_name)
        np.save(numpy_encryption_text_name, encrypted_blocks)
        # zip and return the file to the users
        zip_files(text_zip,[the_enck_text_name,numpy_encryption_text_name])

        # then move them to the uploads
        shutil.move(the_enck_text_name, path_to_uploads)
        shutil.move(numpy_encryption_text_name, path_to_uploads)
        # shutil.move(text_zip, path_to_uploads) # return this to user before moving it


        # ## testing download 
        # attached_zip_file = send_file(text_zip, as_attachment=True)

        # # replace text with the string of text you want to send
        # # text_encrypted = ''.join(encrypted_blocks)
        # text_encrypted = 'hello there'

        # # create a JSON object with the zip file and the text
        # response = make_response(json.dumps({'zip_file': attached_zip_file, 'text': text_encrypted}))

        # # set the content type of the response to 'application/json'
        # response.headers['Content-Type'] = 'application/json'

        # # return the JSON object
        # return json.dumps(response)
           # replace filename with the name of your zip file
        # replace filename with the name of your zip file
        return send_file(text_zip, as_attachment=True)
    



''' DECRYPTION '''

'''TO DO!!!'''
# todo test & review
# Route to decrypt image data ** NEED TO STORE AS BLOB IN UPLOADS
@demo.route('/decrypt-image', methods=['GET', 'POST'])
def decryptedImageFunc():
    title = "Route to decrypt image data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)
    # if it exists, clean it out
    clean_out_directory(path_to_uploads)
    delete_zip_file(image_zip)
    delete_zip_file(text_zip)

    if request.method == "GET":
        # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status': 'success'}
        response_object['message'] = 'Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("decryptedImageFunc - Post Request Recieved!")

        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No Zip uploaded', 400

        # get the file object from the request
        file = request.files['file']
        # number_Blocks = request.json.get('numBlocks')
        # enck = request.json.get('enck')
        number_Blocks = 32 # TEMP - getting this from the user causes a 400 bad request error

        if file.filename.endswith('.zip'):
            # Save the zip file
            file.save(file.filename)
            # Extract the zip file
            with zipfile.ZipFile(file.filename, 'r') as zip_ref:
                zip_ref.extractall(path_to_uploads)

        # use glob to get the first .npy file in the directory
        npy_file = glob.glob(os.path.join(path_to_uploads, "*.npy"))[0]
        npy_filename = os.path.basename(npy_file)

        cipher_file = glob.glob(os.path.join(path_to_uploads, "*.cipher"))[0]
        cipher_filename = os.path.basename(cipher_file)

        # use glob to get the first .bin file in the directory
        bin_file = glob.glob(os.path.join(path_to_uploads, "*.bin"))[0]
        bin_filename = os.path.basename(bin_file)

        # use glob to get the first .txt file in the directory - mime info - just using the extension stored
        txt_file = glob.glob(os.path.join(path_to_uploads, "*.txt"))[0]
        txt_filename = os.path.basename(txt_file)
        with open(os.path.join(path_to_uploads,txt_filename), 'r') as file:
            thisExtension = file.read()


        # use glob to get the first .shape file in the directory
        shape_file = glob.glob(os.path.join(path_to_uploads, "*.shape"))[0]
        print(shape_file)
        shape_filename = os.path.basename(shape_file)
        print(shape_filename)
        with open(shape_file, 'r') as f:
            file_contents = f.read()
            my_image_shape = eval(file_contents)
        # print(my_image_shape)

        print(f"npy filename: {npy_filename}, bin filename: {bin_filename}, ext is: {thisExtension}, shape is: {my_image_shape}")

        from_image_enck = read_enck_to_variable(os.path.join(path_to_uploads,bin_filename))
        from_image_encrypted_blocks = np.load(os.path.join(path_to_uploads,npy_filename))
        # with open(os.path.join(path_to_uploads,cipher_filename), 'rb') as bytes_file_output:
        #     from_image_encrypted_blocks = bytes_file_output.read()
        


        # make sure that the values are correct
        # print(f"From encrypted blocks: {from_image_encrypted_blocks}")
        # print(f"From enck: {from_image_enck}")
        # decrypted_blocks = decrypt(str(image_bytes), number_Blocks)
        decrypted_blocks = decryptImage(from_image_encrypted_blocks, from_image_enck)
        # print(decrypted_blocks)
        
        print(f"Made it past decryption, type: {type(decrypted_blocks)}")

        output_name = f"{OUTBOUND_DECRYPTED_IMAGE_FILENAME}.{thisExtension}"

        arr = np.array(decrypted_blocks)
        # print(arr)
        # create a PIL image from the array
        # img = Image.fromarray(arr)
        img = Image.fromarray(arr, mode='RGB')
        # save the image to a file
        img.save(output_name)


        #         # # Create a new PIL Image object from the numpy array
        # new_image = Image.fromarray(encoded_blocks)
        # # Save the image to a file
        # new_image.save('new_image.jpg')


        # Convert the bytes to a numpy array
        # image_nparray = np.frombuffer(encoded_blocks, dtype=np.uint8)
        # # Convert the numpy array to an Image object
        # image = Image.fromarray(image_nparray)
        # # Save the image to a file -- this isn't working for some reason
        # image.save(output_name)


        # Unflatten the array
        # arr = image_nparray.reshape(my_image_shape)
        # Assume that you have some bytes data in a BytesIO object


        # with open(output_name, "wb") as copy_file:
        #     # Write the image bytes to the new file
        #     copy_file.write(decrypted_blocks)
        # Create a new PIL Image object from the numpy array
        # output_name = Image.fromarray(decrypted_blocks)


        # # Assuming 'output_name' is the name of the file you want to save the image to
        # decrypted_image.save(output_name)



        # # todo check if actually reads bytes https://groups.google.com/g/pocoo-libs/c/Cwr-muUZOts
        # image_bytes = file.stream.read()
        # # read the bytes from the file object
        # image_bytes = file.read()
        # # you need to get the original enck value from the user to decrypt the whole thing


        # # decrypted_blocks = decrypt(str(image_bytes), number_Blocks)
        # decrypted_blocks = decrypt(image_bytes, number_Blocks)

        

        # # convert the string to bytes
        # image_bytes = decrypted_blocks.encode()

        # # create an in-memory file-like object
        # file = io.BytesIO(image_bytes)

        # # open the image from the file
        # image = Image.open(file)

        # # todo send the image and get image from frontend

        # # return decrypted_blocks
        return send_file(new_image, as_attachment=True)
        # return jsonify(success=True)


'''TO DO!!!'''
# Route to decrypt text data
@demo.route('/decrypt-text', methods=['GET', 'POST'])
def decryptedTextFunc():
    title = "Route to decrypt text data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)
    # if it exists, clean it out
    clean_out_directory(path_to_uploads)
    delete_zip_file(image_zip)
    delete_zip_file(text_zip)

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



# Route to decrypt zip data -- TEXT!!!!
@demo.route('/decrypt-zip', methods=['GET', 'POST'])
def decryptedZipFunc():
    title = "Route to decrypt zip data - Alt N Bit Encryption Demo - Luna and Jacob "
    create_folder(path_to_uploads)
    # if it exists, clean it out
    clean_out_directory(path_to_uploads)
    delete_zip_file(image_zip)
    delete_zip_file(text_zip)

    if request.method == "GET":
        # Program Startup -- Logo Print Out shows that it is working
        our_Logo()

        response_object = {'status': 'success'}
        response_object['message'] = 'Data added!'
        return jsonify(response_object)

    if request.method == "POST":
        print("decryptedZipFunc - Post Request Recieved!")

        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No Zip uploaded', 400

        # get the file object from the request
        file = request.files['file']
        # number_Blocks = request.json.get('numBlocks')
        # enck = request.json.get('enck')
        
        if file.filename.endswith('.zip'):
            # Save the zip file
            file.save(file.filename)
            # Extract the zip file
            with zipfile.ZipFile(file.filename, 'r') as zip_ref:
                zip_ref.extractall(path_to_uploads)
            # print('Zip file uploaded and extracted successfully!')
        # else:
        #     print('Invalid file format')
        # you need to get the original enck value from the user to decrypt the whole thing

        # use glob to get the first .npy file in the directory
        npy_file = glob.glob(os.path.join(path_to_uploads, "*.npy"))[0]
        npy_filename = os.path.basename(npy_file)

        # use glob to get the first .bin file in the directory
        bin_file = glob.glob(os.path.join(path_to_uploads, "*.bin"))[0]
        bin_filename = os.path.basename(bin_file)

        # print(f"npy filename: {npy_filename} and bin filename: {bin_filename}")

        from_text_encrypted_blocks = np.load(os.path.join(path_to_uploads,npy_filename))
        from_text_enck = read_enck_to_variable(os.path.join(path_to_uploads,bin_filename))

        # decrypted_blocks = decrypt(str(image_bytes), number_Blocks)
        decrypted_blocks = decrypt(from_text_encrypted_blocks, from_text_enck)

        # Print out the data: 
        print(f"Decrypted: {decrypted_blocks}")
        # return jsonify(success=True)
        return decrypted_blocks


"""
Shamir's secret sharing w/ homomorphism methods
"""
# todo test & review
@demo.route('/generate-shares', methods=['GET', 'POST'])
def encrypt_sss():
    # save the uploaded file from client
    file = request.files['image']
    file.save('uploaded_image.bmp')
    i, i_shape = sss_question2.read_grayscale_pixels('uploaded_image.bmp')

    n = request.json.get('numShares')
    k = request.json.get('numThreshold')

    #  generate downscaled shares using a mock method
    share_paths = generate_shares(i, n)[1]
    # share_paths = ["share_grayscale_1.bmp", "share_grayscale_2.bmp", "share_grayscale_3.bmp"]
    downscaled_shares, paths, img_list = downscale_shares(share_paths)

    # send shares to the client
    return downscaled_shares[0:k, :], i_shape, send_file(img_list, as_attachment=True)


@demo.route('/reconstruct-image', methods=['GET', 'POST'])
# todo test & review
def decrypt_sss():
    # save all downscaled share images uploaded from the client
    global shape
    files = request.files.getlist('file')
    filenames = []
    for file in files:
        filename = file.filename
        filenames.append(filename)
        file.save(filename)

    n = request.json.get('numShares')
    k = request.json.get('numThreshold')

    downscaled_shares = np.array([])
    for filename in filenames:
        downscaled_share, shape = list(read_grayscale_pixels(filename)[0]), read_grayscale_pixels(filename)[1]
        downscaled_shares = np.append(list(read_grayscale_pixels(filename)[0]))

    # reconstruct imgs with their paths with a fake method
    reconstructed_image = reconstruct_downscaled(downscaled_shares[0:k, :], (shape[0] * 2, shape[1] *2))[2]
    send_file(reconstructed_image, as_attachment=True)

# -------------------------------------
# main statement - used to set dev mode and do auto reloading - remove this before going to production
# -------------------------------------
if __name__ == '__main__':
    demo.run(debug=True)
