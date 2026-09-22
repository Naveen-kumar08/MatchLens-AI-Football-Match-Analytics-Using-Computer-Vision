import cv2
import numpy as np
from sklearn.cluster import KMeans

class TeamClassifier:
    """Baseline team identification using upper-body jersey colour.

    This is intentionally simple. Production systems should add:
    - player re-identification
    - jersey segmentation
    - referee/goalkeeper filtering
    - temporal smoothing
    - a trained appearance classifier
    """

    def __init__(self, min_pixels=80):
        self.min_pixels = min_pixels
        self.model = None
        self.ready = False

    def _feature(self, frame, box):
        x1, y1, x2, y2 = [int(v) for v in box]
        h, w = frame.shape[:2]

        x1, x2 = max(0, x1), min(w - 1, x2)
        y1, y2 = max(0, y1), min(h - 1, y2)

        if x2 <= x1 or y2 <= y1:
            return None

        # Upper 60% of player box, where the shirt normally appears.
        yb = y1 + max(1, int((y2 - y1) * 0.60))
        crop = frame[y1:yb, x1:x2]

        if crop.size == 0:
            return None

        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        pixels = hsv.reshape(-1, 3)

        # Remove very dark/bright/low-saturation pixels.
        mask = (
            (pixels[:, 1] > 45) &
            (pixels[:, 2] > 35) &
            (pixels[:, 2] < 245)
        )

        pixels = pixels[mask]

        if len(pixels) < self.min_pixels:
            return None

        return np.median(pixels, axis=0)

    def fit(self, frame, boxes):
        features = []

        for box in boxes:
            feature = self._feature(frame, box)
            if feature is not None:
                features.append(feature)

        if len(features) < 2:
            return False

        self.model = KMeans(
            n_clusters=2,
            n_init=20,
            random_state=42
        )
        self.model.fit(np.asarray(features))
        self.ready = True
        return True

    def predict(self, frame, box):
        feature = self._feature(frame, box)

        if feature is None or not self.ready:
            return None

        return int(self.model.predict([feature])[0]) + 1
