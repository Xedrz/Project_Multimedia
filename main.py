from utils.video_utils import extract_frames_with_hands

if __name__ == "__main__":
    video_path = "ssstik.io_@supervinzt_1745947204672.mp4"
    output_dir = "output_frames"
    extract_frames_with_hands(video_path, output_dir)
