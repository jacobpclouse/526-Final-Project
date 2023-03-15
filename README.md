# 526-Final-Project
ICSI Final Project for Dolunay (Luna) Dagci and Jacob Clouse - Spring 2023

## Paper: Alternative N-bit Key Data Encryption for Block Ciphers

## Goals:
1) Figure out hashing, figure out XOR / bitwise (encrypt & decrypt)
2) Combine the two above, figure out how to encrypt a single block with both
3) Figure out how to reverse and decrypt that block
4) Figure out how to chain blocks n number of times (based on user input) - encryption then decryption
5) Figure out how to add the obfuscation with Alt n bits
6) Cleanup code, add additional funtionality and potentially GUI

## Issues:
- [ ] How do we retrieve a public key and multiply it with our own private key?
- [ ] How do we determine the block size of our encryption?

## Resources:
- Python hash() method: https://www.geeksforgeeks.org/python-hash-method/
- Python Bitwise Operators (ex: ^): https://www.geeksforgeeks.org/python-bitwise-operators/
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
