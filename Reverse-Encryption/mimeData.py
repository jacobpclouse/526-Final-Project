import magic   # You need to install the 'python-magic' package for this library
import shutil

# Open the image file in binary mode
image_path = '4041x4041square.jpg'
# Use the magic library to get the mime data
mime_data = magic.from_file(image_path, mime=True)

# Save the mime data to a file
with open('mime_data.txt', 'w') as mime_file:
    mime_file.write(mime_data)
# Alternatively, you can use the shutil module to copy the file and preserve its metadata
# shutil.copy2('example_image.jpg', 'example_copy.jpg')
