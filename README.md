# 526-Final-Project
ICSI Final Project for Dolunay (Luna) Dagci and Jacob Clouse - Spring 2023 [![GitHub contributors](https://img.shields.io/github/contributors/jacobpclouse/526-Final-Project.svg)]("https://github.com/jacobpclouse/526-Final-Project/graphs/contributors")
<!-- <a href="https://github.com/jacobpclouse/526-Final-Project/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/jacobpclouse/526-Final-Project" /></a> -->
        
> This is the backend, the frontend is stored at: https://github.com/dolnuea/frontend-alt-n-bit

This project was shown at UAlbany's first ever Showcase Day on April 27th, 2023!

## Paper: Alternative N-bit Key Data Encryption for Block Ciphers
- Download link: https://sol.sbc.org.br/index.php/sbseg/article/download/13990/13839/

## Goals:
1) Figure out hashing, figure out XOR / bitwise (encrypt & decrypt)
2) Combine the two above, figure out how to encrypt a single block with both
3) Figure out how to reverse and decrypt that block
4) Figure out how to chain blocks n number of times (based on user input) - encryption then decryption
5) Figure out how to add the obfuscation with Alt n bits
6) Cleanup code, add additional funtionality and potentially Web GUI

## How to run this code:
1) In your destination folder, you have to clone this repo using ```https://github.com/jacobpclouse/526-Final-Project.git```
2) You will also have to clone the frontend using ```https://github.com/dolnuea/frontend-alt-n-bit.git```
3) You will need cd into the '526-Final-Project' folder and install requirements.txt using ```pip install -r requirements.text```
4) You will then need to follow the README.md in the 'frontend-alt-n-bit' folder to install the needed packages
5) You will run the flask backend using ```python demo.py```
6) You will run the vue frontend using ```npm run serve```
7) You should be able to navigate to the webpage via your browser (localhost on port 8080), and test our our project!

## Issues:
- [x] How do we retrieve a public key and multiply it with our own private key? - see in function 'generate_key_pair'
- [x] How do we determine the block size of our encryption? - measure size of ENCK
- [x] How to get the data back after decryption(how do we even do that with the hashing?)
- [x] Need adjustable block size (currently it stays at 32)
- [x] Need function to adding padding to the test data if it is smaller than the block size (it will just give you an empty result and cause the program to fail during decryption - maybe autokey? Make it random) - Done, implimented just after we get size of ENCK
- [x] Finally, Add the extra PEP at the end of encryption and decryption
- [x] Need to port this to a web app (we can wip up a very quick Flask App)
- [x] Need to find way to use image (convert to bits, convert back - function) - expanding on this, needs to be a certain size or it will not work

## Resources:
- Python hash() method: https://www.geeksforgeeks.org/python-hash-method/
- Python Bitwise Operators (ex: ^): https://www.geeksforgeeks.org/python-bitwise-operators/
- Python: for loops - for i in range(0,len(list) vs for i in list: https://stackoverflow.com/questions/32930246/python-for-loops-for-i-in-range0-lenlist-vs-for-i-in-list
- Symmetric encryption: https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
- hashlib module in Python: https://www.geeksforgeeks.org/hashlib-module-in-python/
- Public Keys - A unique number generated from your private key: https://learnmeabitcoin.com/beginners/public_keys
- Elliptic Curve Cryptography (ECC): https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
- SHA in Python: https://www.geeksforgeeks.org/sha-in-python/
- Scalar Multiplication in Python: https://onyb.gitbook.io/secp256k1-python/scalar-multiplication-in-python
- pycryptodome ECC: https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html
- *python-ecdsa’s documentation*: https://ecdsa.readthedocs.io/en/latest/
- The Wonderful World of Elliptic Curve Cryptography (MEDIUM): https://medium.com/coinmonks/the-wonderful-world-of-elliptic-curve-cryptography-b7784acdef50
- How to find size of an object in Python?: https://www.geeksforgeeks.org/how-to-find-size-of-an-object-in-python/
- hashlib — Secure hashes and message digests: https://docs.python.org/3/library/hashlib.html
- Convert input () to bytes in Python 3? [duplicate]: https://stackoverflow.com/questions/50997921/convert-input-to-bytes-in-python-3
- Can anyone identify this encoding? [ASCII]: https://stackoverflow.com/questions/26802581/can-anyone-identify-this-encoding
- how to hash two arguments: https://stackoverflow.com/questions/57902680/how-to-hash-two-arguments
- pickle — Python object serialization (for storing byte arrays): https://docs.python.org/3/library/pickle.html
- Python | Generate random string of given length: https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/
- TypeError: string argument without an encoding: https://stackoverflow.com/questions/51961386/typeerror-string-argument-without-an-encoding
- Provable Things encrypted-queries (EC example): https://github.com/provable-things/encrypted-queries/blob/master/tools/encrypted_queries_tools.py
- National Institute of Standards and Technology (.gov) | Computer security and the data encryption standard: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nbsspecialpublication500-27.pdf
- Python – Convert Image to String and vice-versa: https://www.geeksforgeeks.org/python-convert-image-to-string-and-vice-versa/
- Python PIL | Image.frombytes() Method: https://www.geeksforgeeks.org/python-pil-image-frombytes-method/
- Python PIL | Image.save() method: https://www.geeksforgeeks.org/python-pil-image-save-method/
- How To Create Your First Web Application Using Flask and Python 3: https://www.digitalocean.com/community/tutorials/how-to-create-your-first-web-application-using-flask-and-python-3
- Connect Vue.js with Flask: https://medium.com/featurepreneur/connect-vuejs-with-flask-1316ea0afecf
- Receive or Return files-Flask API: https://medium.com/analytics-vidhya/receive-or-return-files-flask-api-8389d42b0684
- Python Script to convert Image into Byte array: https://stackoverflow.com/questions/22351254/python-script-to-convert-image-into-byte-array
- **NumPy: Set whether to print full or truncated ndarray (stop them truncating data): https://note.nkmk.me/en/python-numpy-set-printoptions-threshold/
- Vue upload image using Axios (with Preview): https://www.bezkoder.com/vue-upload-image-axios/
- Image download mime type validation python requests: https://stackoverflow.com/questions/43048099/image-download-mime-type-validation-python-requests
- **Convert PIL or OpenCV Image to Bytes without Saving to Disk: https://jdhao.github.io/2019/07/06/python_opencv_pil_image_to_bytes/
- Display and save Numpy array as Image: https://iq.opengenus.org/display-numpy-array-as-image/#:~:text=To%20save%20the%20Numpy%20array,directory%20where%20to%20save%20it.&text=This%20will%20save%20the%20Numpy%20array%20as%20a%20jpeg%20image.
- How to open and view a numpy array in Python (numpy.ndarray.view()): https://www.geeksforgeeks.org/numpy-ndarray-view-in-python/#