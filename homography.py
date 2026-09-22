import cv2
import numpy as np

class PitchMapper:
    def __init__(self, image_points, length_m=105.0, width_m=68.0):
        src = np.array(image_points, dtype=np.float32)

        dst = np.array([
            [0, 0],
            [length_m, 0],
            [length_m, width_m],
            [0, width_m],
        ], dtype=np.float32)

        self.H = cv2.getPerspectiveTransform(src, dst)
        self.length = length_m
        self.width = width_m

    def image_to_pitch(self, x, y):
        pts = np.array([[[float(x), float(y)]]], dtype=np.float32)
        result = cv2.perspectiveTransform(pts, self.H)[0, 0]
        return float(result[0]), float(result[1])
