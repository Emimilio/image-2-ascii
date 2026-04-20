
from PIL import Image 
from image_ascii_converter import convert_image_to_ascii, get_image_high_freq, detect_edges, resize_image
from image_exporter import save_ascii_as_image, save_as_colored_html
import numpy as np


if __name__ == "__main__":

    base_dir = "./images"
    filename = "black_circle"
    image_path = f"{base_dir}/{filename}.png"
    output_path = f"{base_dir}/results/{filename}_ascii.png"
    image = Image.open(image_path).convert("RGB")
    image_resize = resize_image(image)
    color_matrix = np.array(image_resize)
    ascii_matrix = convert_image_to_ascii(image_resize)

    high_freq_image = get_image_high_freq(image)
    high_freq_image_resize = resize_image(high_freq_image)
    edge_matrix = detect_edges(high_freq_image_resize)

    final_image = np.where(edge_matrix == " ", ascii_matrix, edge_matrix)

    save_as_colored_html(final_image, color_matrix)
    save_ascii_as_image(final_image, color_matrix)

