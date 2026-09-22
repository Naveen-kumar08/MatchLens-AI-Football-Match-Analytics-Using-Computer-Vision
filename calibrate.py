import argparse
import cv2

points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append([x, y])
        print(f"Point {len(points)} = [{x}, {y}]")

parser = argparse.ArgumentParser()
parser.add_argument("--image", required=True)
args = parser.parse_args()

image = cv2.imread(args.image)

if image is None:
    raise RuntimeError("Could not read image")

cv2.namedWindow("Pitch calibration")
cv2.setMouseCallback("Pitch calibration", mouse_callback)

while True:
    display = image.copy()

    for i, (x, y) in enumerate(points):
        cv2.circle(display, (x, y), 7, (255, 255, 255), -1)

        cv2.putText(
            display,
            str(i+1),
            (x+8, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

    cv2.imshow("Pitch calibration", display)

    key = cv2.waitKey(20) & 0xFF

    if key == 27:
        break

    if key == ord("r"):
        points.clear()
        print("Points reset")

    if key == 13 and len(points) == 4:
        print("\nCopy this into config.yaml:")
        print("image_points:")
        for p in points:
            print(f"  - [{p[0]}, {p[1]}]")
        break

cv2.destroyAllWindows()
