
import numpy as np
import numpy.typing as npt
from PIL import Image 
from skimage import feature
import utils
from image_exporter import draw_image_to_terminal, save_ascii_as_image, save_as_colored_html


def convert_and_save_image_to_ascii(image_path: str, output_path: str, new_width: int=150, use_edge_detection: bool=False, output_format: str="terminal"):
    image = Image.open(image_path)

    ascii_image, color_image = convert_image_to_ascii(image, new_width, use_edge_detection, output_format)

    if output_format == 'terminal':
        draw_image_to_terminal(ascii_image, color_image)

    elif output_format == 'image':
        save_ascii_as_image(ascii_image, color_image, output_path)

    elif output_format == 'html':
        save_as_colored_html(ascii_image, color_image, output_path)


def convert_image_to_ascii(image: Image, new_width: int=150, use_edge_detection: bool=True, output_format: str="terminal") -> tuple[npt.NDArray, npt.NDArray]:
    image = image.convert("RGB")
    image_resized = utils.resize_image(image, new_width, output_format)
    gray_image = utils.normalize_image(np.array(image_resized.convert("L")))

    ascii_image = utils.map_pixel_to_ascii(image_resized)

    if use_edge_detection:
        canny_edge_mask = feature.canny(gray_image, sigma=1)
        edge_matrix = utils.detect_edges(gray_image)
        edge_matrix = np.where(canny_edge_mask, edge_matrix, " ")

        ascii_image = np.where(edge_matrix == " ", ascii_image, edge_matrix)

    return ascii_image, np.array(image_resized)
