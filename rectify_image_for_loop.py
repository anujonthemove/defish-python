from PIL import Image
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

    # Create a new image with the rectilinear projection format
    output_image = Image.new("RGB", (circum, maxmag))

    for y in range(maxmag):
        for x in range(circum):
            theta = -1.0 * x / maxmag
            mag = maxmag - y
            targety = int(midy + mag * math.cos(theta))
            targetx = int(midx + mag * math.sin(theta))

            if targety < 0 or targety >= height or targetx < 0 or targetx >= width:
                output_image.putpixel((x, y), (0, 0, 0))
            else:
                pixel = input_image.getpixel((targetx, targety))
                output_image.putpixel((x, y), pixel)

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
