import random

import numpy as np
from PIL import Image
from scipy.interpolate import lagrange as lag

k = 2  # minimum number of shares required to reconstruct the secret
n = 5  # total number of shares to create
# The largest prime number among [0,255] is 251.
# Therefore, all pixel values of the hidden image are modulated according to 251.
FIELD_SIZE = 251

"""
Image from: https://people.math.sc.edu/Burkardt/data/bmp/bmp.html
Resources used:
https://github.com/williamium3000/shamir-secret-image-sharing
https://pillow.readthedocs.io/en/stable/reference/Image.html
https://stackoverflow.com/questions/56330561/pil-image-fromarrayimg-astypeuint8-mode-rgb-returns-grayscale-image
"""


def load_file(input):
    f = open(input, "rb")

    # keep header intact
    header = f.read(54)
    width = header[18:22][0]
    height = header[22:26][0]

    # convert header bytes to a numpy array of integers
    # header_arr = np.frombuffer(header, dtype=np.uint8)
    # header_reshaped = header_arr.reshape(54,)

    return width, height, header


def read_grayscale_pixels(input):
    img = Image.open(input).convert('L')
    pixels = np.asarray(img)
    return pixels.flatten(), pixels.shape


def read_rgb_pixels(input, width, height):
    pixels = []
    with open(input, "rb") as f:
        # read the header and discard it to keep it intact
        f.read(54)
        # read the rest of the data as a single byte string
        data = f.read()

    # use numpy to convert the byte string into a 1D array of uint8 values
    data_arr = np.frombuffer(data, dtype=np.uint8)

    # reshape the array into a 3D array of RGB values
    data_arr = data_arr.reshape((height, width, 3))

    # iterate over the pixels and append them to the pixels list
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = data_arr[y, x]
            row.append((r, g, b))
        pixels.append(row)

    return pixels, np.array(pixels).shape


def get_coefficients(num_pixels):
    return [[random.randint(0, FIELD_SIZE) for _ in range(k - 1)] for _ in range(num_pixels)]


def generate_shares(image, mode, shape, n=n):
    num_pixels = image.shape[0]
    coefficient = get_coefficients(num_pixels)
    # print(coefficient.shape)
    shares = []
    for i in range(1, n + 1):
        base = np.array([i ** j for j in range(1, k)])
        base = np.matmul(coefficient, base)
        share_image = image + base
        share_image = share_image % FIELD_SIZE
        shares.append(share_image)

    shares = np.array(shares)
    print(shares.shape)
    shares_reshaped = shares.reshape(n, *shape)
    file_names = []
    for i, img in enumerate(shares_reshaped):
        share_img = Image.fromarray(img.astype(np.uint8))
        # Convert to RGB mode
        share_img = share_img.convert('RGB')
        name = "share_{}_{}.bmp".format(mode, i + 1)
        file_names.append(name)
        share_img.save(name)

    return shares, file_names


def reconstruct(shares, shape, k=k, name='reconstructed_grayscale_image.bmp'):
    print("hi")
    """
    :param shares: the share pixels
    :param shape: shape of our image and num channels (3 bc it is an RGB with three color channels)
    """

    # Create a new array to hold the reconstructed pixel values
    reconstructed_pixels = []

    print("hi")

    # the share numbers for the two shares we want to use, which is [1, 2].
    x = np.array([1, k])
    dim = shares.shape[1]

    print("hi")

    print(shape)

    try:
        for i in range(dim):
            print(i)
            # Use Lagrange interpolation to interpolate the polynomial that passes through the two points
            y = shares[:, i]
            poly = lag(x, y)
            # evaluate the interpolated polynomials at x=0 which is the secret
            pixel = poly(0) % FIELD_SIZE
            # Add the reconstructed pixel value to the new array
            reconstructed_pixels.append(pixel)
    except Exception as e:
        print(f"An error occurred: {e}")

    reconstructed_pixels = np.array(reconstructed_pixels)
    reconstructed_pixels = reconstructed_pixels.reshape(*shape)
    reconstructed_img = Image.fromarray(reconstructed_pixels.astype(np.uint8))
    reconstructed_img.save(name)

    print("Saved reconstructed image!")

    return name, np.array(reconstructed_pixels)


def recolor(path, rgb_pixels, width, height, header):
    # load the grayscale image
    gray_renconstructed_img = Image.open(path)

    # convert the image to RGB
    rgb_renconstructed_img = gray_renconstructed_img.convert("RGB")

    # replace the gray pixels with a color of your choice
    for y in range(height):
        for x in range(width):
            r, g, b = rgb_renconstructed_img.getpixel((y, x))
            if r == g == b:
                rgb_renconstructed_img.putpixel((y, x), rgb_pixels[y][x])

    # save the recolored image
    out = "reconstructed_rgb_image.bmp"
    rgb_renconstructed_img.save(out)

    # append the header to keep header intact
    with open(out, "r+b") as f:
        # Append the header to the new image bytes
        f.seek(0)
        f.write(header)


def recolor_noheader(path, rgb_pixels, width, height):
    # load the grayscale image
    gray_renconstructed_img = Image.open(path)

    # convert the image to RGB
    rgb_renconstructed_img = gray_renconstructed_img.convert("RGB")

    # replace the gray pixels with a color of your choice
    for y in range(height):
        for x in range(width):
            r, g, b = rgb_renconstructed_img.getpixel((y, x))
            if r == g == b:
                rgb_renconstructed_img.putpixel((y, x), rgb_pixels[y][x])

    # save the recolored image
    out = "reconstructed_rgb_image.bmp"
    rgb_renconstructed_img.save(out)

    # append the header to keep header intact
    with open(out, "r+b") as f:
        # Append the header to the new image bytes
        f.seek(0)
        f.write(header)


if __name__ == '__main__':
    file = "image.bmp"
    w, h, header = load_file(file)
    pixels, grayscale_shape = read_grayscale_pixels(file)
    rgb_pixels, rgb_shape = read_rgb_pixels(file, w, h)

    # print("Pixels:")
    # print(pixels)

    print("Shape of pixels:")
    print(grayscale_shape)

    print("Generating shares")
    shares = generate_shares(pixels, 'grayscale', grayscale_shape)
    rgb_shares = generate_shares(np.array(rgb_pixels).flatten(), 'rgb', rgb_shape)
    # print("Shares:")
    # print(shares)

    print("Reconstructing the image with 2 shares...")
    output = reconstruct(shares[0:k, :], grayscale_shape)[0]

    print("Recoloring the image...")
    recolor(output, rgb_pixels, w, h, header)
    print("Done!")
