import cv2
import pandas as pd

INPUT_VIDEO = "input.mp4"
TRACKS_FILE = "outputs/tracks_with_speed.csv"
OUTPUT_VIDEO = "outputs/matchlens_trajectory.mp4"

TRAIL_LENGTH = 40

df = pd.read_csv(TRACKS_FILE)

df = df[df["class"] == "player"].copy()

df["frame"] = df["frame"].astype(int)
df["track_id"] = df["track_id"].astype(int)

frame_data = {}

for frame_number, group in df.groupby("frame"):
    frame_data[frame_number] = group


cap = cv2.VideoCapture(INPUT_VIDEO)

if not cap.isOpened():
    print("ERROR: Could not open input.mp4")
    raise SystemExit


fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    fps = 25

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

total_frames = int(
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
)


fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    fps,
    (width, height)
)

print("Creating player trajectory video...")
print(f"Resolution: {width} x {height}")
print(f"FPS: {fps:.2f}")
print(f"Total frames: {total_frames}")


# Store image-coordinate trails
trails = {}


frame_number = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    players = frame_data.get(
        frame_number,
        pd.DataFrame()
    )

    current_ids = set()

    for _, player in players.iterrows():

        track_id = int(player["track_id"])

        x1 = int(player["x1"])
        y1 = int(player["y1"])
        x2 = int(player["x2"])
        y2 = int(player["y2"])

        # Foot point of player
        foot_x = int((x1 + x2) / 2)
        foot_y = y2

        current_ids.add(track_id)

        if track_id not in trails:
            trails[track_id] = []

        trails[track_id].append(
            (foot_x, foot_y)
        )

        # Limit trail length
        if len(trails[track_id]) > TRAIL_LENGTH:
            trails[track_id] = trails[track_id][-TRAIL_LENGTH:]

        team = player["team"]

        if pd.isna(team):

            color = (180, 180, 180)
            team_name = "Unknown"

        elif int(team) == 1:

            color = (255, 100, 100)
            team_name = "Team 1"

        else:

            color = (100, 100, 255)
            team_name = "Team 2"


        # ------------------------------------------
        # Draw trajectory
        # ------------------------------------------

        points = trails[track_id]

        for i in range(1, len(points)):

            cv2.line(
                frame,
                points[i - 1],
                points[i],
                color,
                2
            )


        # ------------------------------------------
        # Draw player bounding box
        # ------------------------------------------

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )


        # ------------------------------------------
        # Speed
        # ------------------------------------------

        speed = player.get(
            "speed_kmh",
            0
        )

        if pd.isna(speed):
            speed = 0


        label = (
            f"ID {track_id} | "
            f"{team_name} | "
            f"{speed:.1f} km/h"
        )

        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 8, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            color,
            1,
            cv2.LINE_AA
        )


    # ----------------------------------------------
    # Remove old tracks
    # ----------------------------------------------

    old_ids = list(trails.keys())

    for track_id in old_ids:

        if track_id not in current_ids:

            # Keep history but remove very old trails
            if len(trails[track_id]) > TRAIL_LENGTH:

                trails[track_id] = trails[track_id][
                    -TRAIL_LENGTH:
                ]


    # ----------------------------------------------
    # Header
    # ----------------------------------------------

    cv2.rectangle(
        frame,
        (10, 10),
        (270, 65),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        "MATCHLENS AI",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        f"Trajectory | Frame {frame_number}",
        (20, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (220, 220, 220),
        1,
        cv2.LINE_AA
    )


    # ----------------------------------------------
    # Write output
    # ----------------------------------------------

    out.write(frame)

    frame_number += 1

    if frame_number % 100 == 0:

        print(
            f"Processed "
            f"{frame_number}/{total_frames}"
        )


cap.release()
out.release()

print()
print("===================================")
print("Trajectory video created")
print("===================================")
print(
    f"Output: {OUTPUT_VIDEO}"
)