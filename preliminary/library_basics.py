"""A basic introduction to Open CV

Instructions
------------

Implement the functions below based on their docstrings.

Notice some docstrings include references to third-party documentation
Some docstrings **require** you to add references to third-party documentation.

Make sure you read the docstrings C.A.R.E.F.U.L.Y (yes, I took the L to check that you are awake!)
"""

# imports - add all required imports here
from pathlib import Path
from PIL import Image
import cv2
import numpy as np



VID_PATH = Path("../resources/oop.mp4")

class CodingVideo:
    capture: cv2.VideoCapture

    def __init__(self, video: Path | str):
        self.capture = cv2.VideoCapture(video)
        if not self.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.frame_count = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = self.frame_count / self.fps


    def __str__(self) -> str:

        return f'This video has a total of {int(self.frame_count)} frames, running at {round(self.fps,2)} frames per second for {round(self.duration/60,2)} minutes'


    def get_frame_number_at_time(self, seconds: int) -> int:

        return int(self.fps * seconds)


    def get_frame_rgb_array(self, frame_number: int) -> np.ndarray:

        # Set the frame position
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # Read the frame
        success, frame = self.capture.read()
        if not success:
            raise ValueError(f"Could not read that frame")

        # Convert from BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return rgb_frame


    def get_image_as_bytes(self, seconds: int) -> bytes:

        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.get_frame_number_at_time(seconds))
        ok, frame = self.capture.read()
        if not ok or frame is None:
            raise ValueError("Invalid frame in target location")
        ok, buf = cv2.imencode(".png", frame)
        if not ok:
            raise ValueError("Failed to encode frame")
        return buf.tobytes()


    def save_as_image(self, seconds: int, output_path: Path | str = 'output.png') -> None:

        frame_number = self.get_frame_number_at_time(seconds)
        rgb_array = self.get_frame_rgb_array(frame_number)
        image = Image.fromarray(rgb_array)
        image.save(output_path)

def test():

    oop = CodingVideo("../resources/oop.mp4")
    print(oop)
    oop.save_as_image(42)

if __name__ == '__main__':
    test()
