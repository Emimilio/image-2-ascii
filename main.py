
from PIL import Image 
from image_ascii_converter import convert_image_to_ascii, save_ascii_as_image


if __name__ == "__main__":

    base_dir = "./images"
    filename = "meme"
    image_path = f"{base_dir}/{filename}.jpg"
    output_path = f"{base_dir}/results/{filename}_ascii.png"
    image = Image.open(image_path)
    ascii_matrix, color_matrix = convert_image_to_ascii(image)
    save_ascii_as_image(ascii_matrix, color_matrix, output_path)
