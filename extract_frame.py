import argparse
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--source", required=True)
parser.add_argument("--frame", type=int, default=0)
parser.add_argument("--output", default="frame.jpg")
args = parser.parse_args()

cap = cv2.VideoCapture(args.source)

if not cap.isOpened():
    raise RuntimeError("Cannot open video")

cap.set(cv2.CAP_PROP_POS_FRAMES, args.frame)
ok, frame = cap.read()
cap.release()

if not ok:
    raise RuntimeError("Could not read requested frame")

cv2.imwrite(args.output, frame)
print(f"Saved {args.output}")
