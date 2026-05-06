
from PIL import Image
import numpy as np
import cv2
from image_exporter import draw_image
from image_ascii_converter import convert_image_to_ascii


def convert_video_to_ascii(video_path: str, output_path: str, new_width: int=200, use_edge_detection: bool=True):
    cap = cv2.VideoCapture(video_path)
    codec_id = "mp4v"
    fourcc = cv2.VideoWriter_fourcc(*codec_id)
    out = None

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    fps = cap.get(cv2.CAP_PROP_FPS)
    
    while True:

        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(frame)
        ascii_image, color_image = convert_image_to_ascii(image, new_width=new_width, use_edge_detection=use_edge_detection)
        frame_to_write = np.array(draw_image(ascii_image, color_image))

        if out is None:
            height, width, _ = frame_to_write.shape
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        final_frame = cv2.cvtColor(frame_to_write, cv2.COLOR_RGB2BGR)
        out.write(final_frame)

    cap.release()
    if out is not None:
        out.release()
