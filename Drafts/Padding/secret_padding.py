# https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/

import secrets # for padding MSN up to block size
import string # for padding MSN up to block size


message_test = 'the rain is nice'
block_size = 3

# --- Function to add random padding to anemic inputs (if they are less than desired length) ---
def do_we_need_padding(messageToAnalyze,targetBlockSizeInteger):
    # Usually targetBlockSizeInteger will be like 32
    if (len(messageToAnalyze) < targetBlockSizeInteger):
        numberOfCharsLeft = targetBlockSizeInteger - len(messageToAnalyze) # figure out how many chars we are short by
        print(f"We need to pad {numberOfCharsLeft} characters!")
        # using secrets.choices() - generating random strings
        toConcatBoi = ''.join(secrets.choice(string.ascii_letters + string.digits)
            for i in range(numberOfCharsLeft))
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
