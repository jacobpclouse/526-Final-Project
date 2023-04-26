from PIL import Image
import builtins
import io
import os

filename = 'testphoto.png'
name, extension = filename.split(".")
upperCaseExt = extension.upper()
print(upperCaseExt)

# Open the image file in binary mode, convert to bytes
with builtins.open(filename, 'rb') as file:
    image_data = file.read()

# Create a PIL Image object from the bytes
image = Image.open(io.BytesIO(image_data))

# Get the width and height of the image
width, height = image.size
print(f"height: {height}, width: {width}")

# Convert the PIL Image object to a bytes object
image_bytes = io.BytesIO()
image.save(image_bytes, format=upperCaseExt)
image_bytes = image_bytes.getvalue()

# Create a new PIL Image object from the bytes
new_image = Image.open(io.BytesIO(image_bytes))

# Display the image
new_image.show()