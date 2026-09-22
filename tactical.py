import cv2
import numpy as np

def draw_pitch(width, height):
    img = np.zeros((height, width, 3), dtype=np.uint8)

    margin = 30
    x0, y0 = margin, margin
    x1, y1 = width - margin, height - margin

    cv2.rectangle(img, (x0, y0), (x1, y1), (80, 80, 80), 2)

    xm = (x0 + x1) // 2
    ym = (y0 + y1) // 2

    cv2.line(img, (xm, y0), (xm, y1), (80, 80, 80), 2)
    cv2.circle(img, (xm, ym), int(min(x1-x0, y1-y0) * 0.12),
               (80, 80, 80), 2)

    box_w = int((x1 - x0) * 0.16)
    box_h = int((y1 - y0) * 0.44)

    cv2.rectangle(
        img,
        (x0, ym-box_h//2),
        (x0+box_w, ym+box_h//2),
        (80, 80, 80), 2
    )

    cv2.rectangle(
        img,
        (x1-box_w, ym-box_h//2),
        (x1, ym+box_h//2),
        (80, 80, 80), 2
    )

    return img

def pitch_to_canvas(x, y, width, height, length_m, width_m):
    margin = 30
    px = int(margin + (x / length_m) * (width - 2*margin))
    py = int(margin + (y / width_m) * (height - 2*margin))
    return px, py

def render_tactical(tracks, width, height, length_m, width_m):
    img = draw_pitch(width, height)

    for track in tracks:
        if track.get("pitch_x") is None:
            continue

        px, py = pitch_to_canvas(
            track["pitch_x"],
            track["pitch_y"],
            width,
            height,
            length_m,
            width_m,
        )

        team = track.get("team")

        if team == 1:
            label = "A"
        elif team == 2:
            label = "B"
        else:
            label = "?"

        cv2.circle(img, (px, py), 8, (255, 255, 255), -1)

        cv2.putText(
            img, label, (px-4, py+5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45, (0, 0, 0), 1
        )

        if track.get("track_id") is not None:
            cv2.putText(
                img, str(track["track_id"]), (px+9, py),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (220, 220, 220), 1
            )

    return img
