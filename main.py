
from PIL import Image 
from image_ascii_converter import convert_image_to_ascii, detect_edges, resize_image, get_difference_of_gaussian 
from image_exporter import save_ascii_as_image, save_as_colored_html
import numpy as np


if __name__ == "__main__":

    base_dir = "./images"
    filename = "mario"
    image_path = f"{base_dir}/{filename}.png"
    output_path = f"{base_dir}/results/{filename}_ascii.png"
    image = Image.open(image_path)

    ascii_image, color_image = convert_image_to_ascii(image)

    save_ascii_as_image(ascii_image, color_image)
    save_as_colored_html(ascii_image, color_image)

