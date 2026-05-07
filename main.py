import argparse
from image_ascii_converter import convert_and_save_image_to_ascii
from video_ascii_converter import convert_video_to_ascii


def parse_args():
    parser = argparse.ArgumentParser(description="Convert images and videos to ASCII art.")

    parser.add_argument("-i", "--input_path", type=str, required=True,
                        help="Path to input video or image file")

    parser.add_argument("-o", "--output_path", type=str,
                        help="Path to save the output file (required for 'image' or 'html' formats)")

    parser.add_argument("-f", "--format", type=str, choices=['terminal', 'image', 'html'], default='terminal',
                        help="Output format: 'terminal' (print to console), 'image' (save as png), or 'html' (save as webpage)")

    parser.add_argument("-w", "--width", type=int, default=150, help="Width of output in characters")

    parser.add_argument(
        "--edge",
        dest="edge_detection",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable or disable edge detection (default: True)"
    )

    return parser.parse_args()


def is_video(filename):
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
    return filename.lower().endswith(video_extensions)


if __name__ == "__main__":
    args = parse_args()

    if args.format in ['image', 'html'] and not args.output_path:
        print(f"Error: --output_path is required when using format '{args.format}'")
        exit(1)

    print(f"--- Processing: {args.input_path} ---")

    if is_video(args.input_path):
        convert_video_to_ascii(
            video_path=args.input_path,
            output_path=args.output_path,
            new_width=args.width,
            use_edge_detection=args.edge_detection
        )

    else:
        try:
            convert_and_save_image_to_ascii(args.input_path, args.output_path, args.width, args.edge_detection, args.format)
        except Exception as e:
            print(f"Failed to process image: {e}")