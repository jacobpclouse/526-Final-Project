# https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/

import secrets # for padding MSN up to block size
import string # for padding MSN up to block size
import random # adding so we add an arbitrary length to our msg


message_test = b'the rain is nice'
block_size = 32

# --- Function to add random padding to anemic inputs (if they are less than desired length) ---
def do_we_need_padding(messageToAnalyze,targetBlockSizeInteger):
    # Usually targetBlockSizeInteger will be like 32
    if (len(messageToAnalyze) < targetBlockSizeInteger):
        numberOfCharsLeft = targetBlockSizeInteger - len(messageToAnalyze) # figure out how many chars we are short by
        print(f"We need to pad at least {numberOfCharsLeft} characters!")
        numberOfCharsLeft = numberOfCharsLeft + (random.randint(0,200))
        print(numberOfCharsLeft)
        # using secrets.choices() - generating random strings
        toConcatBoi = ''.join(secrets.choice(string.ascii_letters + string.digits)
            for i in range(numberOfCharsLeft))
        messageToAnalyze = messageToAnalyze + bytes(toConcatBoi,encoding='utf8') # updating orig data by concat
        return messageToAnalyze # return new message with concatonated data
    else:
        print("We don't need padding...")
        return messageToAnalyze # don't need to adjust, we can leave it as it is

# -------------------------------------------------------------------------------------


result = do_we_need_padding(message_test,block_size)
print(f"Result: '{result}'")
print(f"Length: {len(result)}")
