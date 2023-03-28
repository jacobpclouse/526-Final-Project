'''
ORIGINAL CODE:

    BLK = [e[i:i+block_size] for i in range(0, len(e), block_size)]
    BLK[0] = bytes([BLK[0][i] ^ ENCK[i] for i in range(block_size)])
'''

#  split a byte array into blocks of a given size
def split_into_blocks(e, block_size):
    num_blocks = (len(e) + block_size - 1) // block_size
    blocks = [e[i*block_size : (i+1)*block_size] for i in range(num_blocks)]
    return blocks

# Split the input byte array e - blocks of size block_size
block_size = 16
blocks = split_into_blocks(e, block_size)

# XOR between the first block and the key ENCK
first_block = blocks[0]
key = bytes(ENCK)
xored_block = bytes(b1 ^ b2 for b1, b2 in zip(first_block, key))

# Replace the first block in the list of blocks with the XORed block
blocks[0] = xored_block
