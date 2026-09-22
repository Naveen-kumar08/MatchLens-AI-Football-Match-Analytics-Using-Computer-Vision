import cv2
import pandas as pd


INPUT_VIDEO = "input.mp4"
TRACKS_FILE = "outputs/tracks_with_speed.csv"
OUTPUT_VIDEO = "outputs/matchlens_analytics.mp4"


# --------------------------------------------------
# Load tracking data
# --------------------------------------------------

df = pd.read_csv(TRACKS_FILE)

# Keep player detections
df = df[df["class"] == "player"].copy()

# Make sure frame and ID are integers
df["frame"] = df["frame"].astype(int)
df["track_id"] = df["track_id"].astype(int)

# Create frame lookup
frame_data = {}

for frame_number, group in df.groupby("frame"):
    frame_data[frame_number] = group


# --------------------------------------------------
# Open video
# --------------------------------------------------

cap = cv2.VideoCapture(INPUT_VIDEO)

if not cap.isOpened():
    print("ERROR: Could not open input.mp4")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 25

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

total_frames = int(
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
)


# --------------------------------------------------
# Output video
# --------------------------------------------------

fourcc = cv2.VideoWriter_fourcc(
    *"mp4v"
)

out = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    fps,
    (width, height)
)

print("Processing video...")
print(f"Resolution: {width} x {height}")
print(f"FPS: {fps:.2f}")
print(f"Frames: {total_frames}")


# --------------------------------------------------
# Mini tactical pitch
# --------------------------------------------------

def draw_tactical_pitch(frame, players):

    pitch_w = 300
    pitch_h = 195

    margin = 15

    x0 = width - pitch_w - margin
    y0 = margin

    # Background
    cv2.rectangle(
        frame,
        (x0, y0),
        (x0 + pitch_w, y0 + pitch_h),
        (40, 120, 40),
        -1
    )

    # Pitch boundary
    cv2.rectangle(
        frame,
        (x0, y0),
        (x0 + pitch_w, y0 + pitch_h),
        (255, 255, 255),
        2
    )

    # Halfway line
    center_x = x0 + pitch_w // 2

    cv2.line(
        frame,
        (center_x, y0),
        (center_x, y0 + pitch_h),
        (255, 255, 255),
        1
    )

    # Center circle
    cv2.circle(
        frame,
        (center_x, y0 + pitch_h // 2),
        27,
        (255, 255, 255),
        1
    )

    # Penalty boxes
    box_h = int(pitch_h * 0.60)

    top = y0 + (pitch_h - box_h) // 2
    bottom = top + box_h

    box_w = int(pitch_w * 0.16)

    # Left box
    cv2.rectangle(
        frame,
        (x0, top),
        (x0 + box_w, bottom),
        (255, 255, 255),
        1
    )

    # Right box
    cv2.rectangle(
        frame,
        (x0 + pitch_w - box_w, top),
        (x0 + pitch_w, bottom),
        (255, 255, 255),
        1
    )

    # Plot players
    for _, player in players.iterrows():

        pitch_x = player.get("pitch_x_m")
        pitch_y = player.get("pitch_y_m")

        if pd.isna(pitch_x) or pd.isna(pitch_y):
            continue

        # Convert metres to mini pitch pixels
        px = int(
            x0 + (float(pitch_x) / 105.0) * pitch_w
        )

        py = int(
            y0 + (float(pitch_y) / 68.0) * pitch_h
        )

        team = player.get("team")

        if pd.isna(team):
            color = (200, 200, 200)
        elif int(team) == 1:
            color = (255, 80, 80)
        else:
            color = (80, 80, 255)

        cv2.circle(
            frame,
            (px, py),
            5,
            color,
            -1
        )

        cv2.putText(
            frame,
            str(int(player["track_id"])),
            (px + 6, py),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    cv2.putText(
        frame,
        "TACTICAL VIEW",
        (x0, y0 + pitch_h + 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


# --------------------------------------------------
# Process frames
# --------------------------------------------------

frame_number = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    players = frame_data.get(
        frame_number,
        pd.DataFrame()
    )

    # ----------------------------------------------
    # Draw player detections
    # ----------------------------------------------

    for _, player in players.iterrows():

        x1 = int(player["x1"])
        y1 = int(player["y1"])
        x2 = int(player["x2"])
        y2 = int(player["y2"])

        track_id = int(
            player["track_id"]
        )

        team = player.get("team")

        speed = player.get(
            "speed_kmh",
            0
        )

        if pd.isna(speed):
            speed = 0

        # Team color
        if pd.isna(team):
            color = (200, 200, 200)
            team_text = "Unknown"
        elif int(team) == 1:
            color = (255, 80, 80)
            team_text = "Team 1"
        else:
            color = (80, 80, 255)
            team_text = "Team 2"

        # Bounding box
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # Label
        label = (
            f"ID {track_id} | "
            f"{team_text} | "
            f"{speed:.1f} km/h"
        )

        # Label background
        (tw, th), _ = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            1
        )

        label_y = max(
            y1 - 8,
            th + 5
        )

        cv2.rectangle(
            frame,
            (x1, label_y - th - 5),
            (x1 + tw + 5, label_y + 2),
            color,
            -1
        )

        cv2.putText(
            frame,
            label,
            (x1 + 2, label_y - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    # ----------------------------------------------
    # Tactical pitch
    # ----------------------------------------------

    if not players.empty:
        draw_tactical_pitch(
            frame,
            players
        )

    # ----------------------------------------------
    # Information panel
    # ----------------------------------------------

    cv2.rectangle(
        frame,
        (10, 10),
        (260, 65),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        "MatchLens AI",
        (20, 32),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        f"Frame: {frame_number}",
        (20, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    # ----------------------------------------------
    # Write frame
    # ----------------------------------------------

    out.write(frame)

    frame_number += 1

    if frame_number % 100 == 0:

        print(
            f"Processed "
            f"{frame_number}/{total_frames}"
        )


# --------------------------------------------------
# Cleanup
# --------------------------------------------------

cap.release()
out.release()

print()
print("===================================")
print("Analytics video created successfully")
print("===================================")
print(
    f"Output: {OUTPUT_VIDEO}"
)