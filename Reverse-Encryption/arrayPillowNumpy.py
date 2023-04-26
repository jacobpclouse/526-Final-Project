from PIL import Image
import builtins
import io
import numpy as np 

filename = 'testphoto.png'
# name, extension = filename.split(".")
# upperCaseExt = extension.upper()
# print(upperCaseExt)

# Open the image file in binary mode, convert to bytes
with builtins.open(filename, 'rb') as file:
    image_data = file.read()

# Create a PIL Image object from the bytes
image = Image.open(io.BytesIO(image_data))


# Convert the PIL Image object to a numpy array
image_array = np.array(image)

# Display the shape of the numpy array
print(image_array.shape)

# Save the numpy array to a file
np.save('testphoto.npy', image_array)

# Load the numpy array from the file
new_image_array = np.load('testphoto.npy')

# Create a new PIL Image object from the numpy array
new_image = Image.fromarray(new_image_array)

# Display the image
new_image.show()

# # Get the width and height of the image
# width, height = image.size
# print(f"height: {height}, width: {width}")

# # Convert the PIL Image object to a bytes object
# image_bytes = io.BytesIO()
# image.save(image_bytes, format=upperCaseExt)
# image_bytes = image_bytes.getvalue()

# # Create a new PIL Image object from the bytes
# new_image = Image.open(io.BytesIO(image_bytes))

# # Display the image
# new_image.show()