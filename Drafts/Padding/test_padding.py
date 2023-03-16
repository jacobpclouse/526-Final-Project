# https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/

import string # for padding MSN up to block size
import random # for padding MSN up to block size

# initializing size of string
# N = 25

message_test = 'the rain is nice'
block_size = 100

# --- Function to add random padding to anemic inputs (if they are less than desired length) ---
def do_we_need_padding(messageToAnalyze,targetBlockSizeInteger):
    # Usually targetBlockSizeInteger will be like 32
    if (len(messageToAnalyze) < targetBlockSizeInteger):
        numberOfCharsLeft = targetBlockSizeInteger - len(messageToAnalyze) # figure out how many chars we are short by
        print(f"We need to pad {numberOfCharsLeft} characters!")
        # using random.choices() - generating random strings
        toConcatBoi = ''.join(random.choices(string.ascii_letters, k=numberOfCharsLeft))
        # print result
        # print("The generated random string : " + str(toConcatBoi))
        messageToAnalyze = messageToAnalyze + str(toConcatBoi)
        return messageToAnalyze # return new message with concatonated data
    else:
        print("We don't need padding...")
        return messageToAnalyze # don't need to adjust, we can leave it as it is

# -------------------------------------------------------------------------------------


result = do_we_need_padding(message_test,block_size)
print(f"Result: '{result}'")
print(f"Length: {len(result)}")
