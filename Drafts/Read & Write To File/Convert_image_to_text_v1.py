import base64
from io import BytesIO
from PIL import Image


def imageToBase64(ImageName, ImageExtension):
    # Open the image file
    with open(f"{ImageName}.{ImageExtension}", "rb") as image_file:
        # Read the image data
        image_data = image_file.read()

    # Convert the image data to bytes
    bytes_image = BytesIO(image_data)

    # Convert the bytes image to base64 encoding
    base64_image = base64.b64encode(bytes_image.getvalue())
    
    # Return bytes object to user (ex: b'ew;jeaekkel....')
    return base64_image


''' DO WE WANT TO HAVE IT SO THAT IT WILL OPEN UP THE BYTES OBJECT AUTOMATICALLY? OR WILL WE ASSUME THAT IT HAS BEEN OPENED OUTSIDE THE PROGRAM?
ALSO: DO WE WANT THIS TO SAVE IT AS AN IMAGE? '''
def base64ToImage(inputBase64Bytes):
    # Convert the base64 encoded image back to bytes
    decoded_image = base64.b64decode(inputBase64Bytes)

    # Open the decoded image using the PIL library
    img = Image.open(BytesIO(decoded_image))

    # Display the image
    img.show()

    # # creating a image object (main image) 
    im1 = Image.open(img) 

    # # save a image using extension
    im1 = im1.save("OUTPUTIMAGE.jpg")



sample = imageToBase64('guts','jpg')
print(sample)


originalBack = base64ToImage(sample)