
from PIL import Image 
from image_ascii_converter import convert_image_to_ascii
from video_ascii_converter import convert_video_to_ascii
from image_exporter import save_ascii_as_image, save_as_colored_html
import numpy as np


if __name__ == "__main__":

    base_dir = "./images"
    filename = "mario"
    image_path = f"{base_dir}/{filename}.png"
    output_path = f"{base_dir}/results/{filename}_ascii.png"
    image = Image.open(image_path)

    ascii_image, color_image = convert_image_to_ascii(image)

    save_ascii_as_image(ascii_image, color_image, output_path)

    # base_video_dir = "./video"
    # filename = "mario_clip"
    # video_path = f"{base_video_dir}/{filename}.mp4"
    # output_path = f"{base_video_dir}/results/{filename}_ascii.mp4"
    #
    # convert_video_to_ascii(video_path=video_path, output_path=output_path)


