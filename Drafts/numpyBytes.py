import builtins
import numpy as np
from PIL import Image
import io

# Open the image file in binary mode, convert to bytes
with builtins.open('testphoto.png', 'rb') as file:
    image_data = file.read()# Read the content of the image file
print(len(image_data))
image_array = np.frombuffer(image_data, dtype=np.uint8)# Convert the image data to a NumPy array
image_bytes = image_array.tobytes() # Convert the NumPy array to bytes



# Open the image file, Get the width and height of the image
image = Image.open('testphoto.png')
width, height = image.size
print(f"height: {height}, width: {width}")


# ----------


# convert back to image
# Create an image from the bytes
image = Image.frombytes('RGB', (width, height), image_bytes)

# Display the image
image.show()