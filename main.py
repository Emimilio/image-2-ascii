
from PIL import Image 
from image_ascii_converter import convert_image_to_ascii, detect_edges, resize_image, get_skimage_high_freq
from image_exporter import save_ascii_as_image, save_as_colored_html
import numpy as np


if __name__ == "__main__":

    base_dir = "./images"
    filename = "banana"
    image_path = f"{base_dir}/{filename}.png"
    output_path = f"{base_dir}/results/{filename}_ascii.png"
    image = Image.open(image_path).convert("RGB")
    image_resize = resize_image(image)
    color_matrix = np.array(image_resize)
    ascii_matrix = convert_image_to_ascii(image_resize)

    high = get_skimage_high_freq(image)
    high.show()
    edge_matrix = detect_edges(high)

    final_image = np.where(edge_matrix == " ", ascii_matrix, edge_matrix)

    save_ascii_as_image(final_image, color_matrix)
    save_as_colored_html(final_image, color_matrix)

