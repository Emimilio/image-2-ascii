
from PIL import Image 
from image_ascii_converter import convert_image_to_ascii, get_image_high_freq, detect_edges, resize_image
from image_exporter import save_ascii_as_image, save_as_colored_html
import numpy as np


if __name__ == "__main__":

    base_dir = "./images"
    filename = "flat_iron"
    image_path = f"{base_dir}/{filename}.png"
    output_path = f"{base_dir}/results/{filename}_ascii.png"
    image = Image.open(image_path)
    image = resize_image(image)
    ascii_matrix, color_matrix = convert_image_to_ascii(image)

    image = get_image_high_freq(image)

    edge_matrix = detect_edges(image)

    final_image = np.where(edge_matrix == " ", ascii_matrix, edge_matrix)

    save_as_colored_html(final_image, color_matrix)
    save_ascii_as_image(final_image, color_matrix, output_path)

