from PIL import Image
import numpy as np
import math
import sys


def rectify_image(input_path, output_path):
    # Open the input image
    input_image = Image.open(input_path)
    width, height = input_image.size

    # Calculate variables for rectilinear projection
    midy = height // 2
    midx = width // 2
    maxmag = max(midy, midx)
    circum = int(2 * math.pi * maxmag)

    # Create a mesh grid of x and y coordinates
    x, y = np.meshgrid(np.arange(circum), np.arange(maxmag))

    # Calculate the corresponding theta and mag values
    theta = -1.0 * x / maxmag
    mag = maxmag - y

    # Calculate the corresponding target coordinates
    targety = np.rint(midy + mag * np.cos(theta)).astype(int)
    targetx = np.rint(midx + mag * np.sin(theta)).astype(int)

    # Create masks for invalid coordinates
    invalid_mask = np.logical_or(targety < 0, targety >= height) | np.logical_or(
        targetx < 0, targetx >= width
    )

    # Extract pixel values from the input image
    input_pixels = np.array(input_image)

    # Initialize the output image array
    output_pixels = np.zeros((maxmag, circum, 3), dtype=np.uint8)

    # Assign pixel values from the input image to the corresponding coordinates in the output image
    output_pixels[~invalid_mask] = input_pixels[
        targety[~invalid_mask], targetx[~invalid_mask]
    ]

    # Create the output image from the pixel array
    output_image = Image.fromarray(output_pixels, "RGB")

    # Save the rectified image as JPEG
    output_image.save(output_path, "JPEG")
    print("Rectified image saved successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python rectify_image.py <input_image.jpg> <output_image.jpg>")
    else:
        input_image_path = sys.argv[1]
        output_image_path = sys.argv[2]
        rectify_image(input_image_path, output_image_path)
