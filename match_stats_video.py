import cv2
import pandas as pd


INPUT_VIDEO = "input.mp4"
TRACKS_FILE = "outputs/tracks_with_speed.csv"
OUTPUT_VIDEO = "outputs/matchlens_stats.mp4"


# --------------------------------------------------
# Load tracking data
# --------------------------------------------------

df = pd.read_csv(TRACKS_FILE)

# Keep players only
df = df[df["class"] == "player"].copy()

df["frame"] = df["frame"].astype(int)
df["track_id"] = df["track_id"].astype(int)

# Frame-wise lookup
frame_data = {}

for frame_number, group in df.groupby("frame"):
    frame_data[frame_number] = group


# --------------------------------------------------
# Open input video
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
# Create output video
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


print("Creating MatchLens AI statistics video...")
print(f"Resolution: {width} x {height}")
print(f"FPS: {fps:.2f}")
print(f"Total frames: {total_frames}")


# --------------------------------------------------
# Draw statistics panel
# --------------------------------------------------

def draw_statistics_panel(frame, players, frame_number):

    panel_x = 10
    panel_y = 10

    panel_w = 310
    panel_h = 225

    # Panel background
    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (panel_x, panel_y),
        (
            panel_x + panel_w,
            panel_y + panel_h
        ),
        (0, 0, 0),
        -1
    )

    # Slight transparency
    cv2.addWeighted(
        overlay,
        0.75,
        frame,
        0.25,
        0,
        frame
    )

    # Title
    cv2.putText(
        frame,
        "MATCHLENS AI",
        (25, 42),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        "LIVE MATCH ANALYTICS",
        (25, 67),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (200, 200, 200),
        1,
        cv2.LINE_AA
    )

    # Default values
    total_players = 0
    team1_count = 0
    team2_count = 0
    unknown_count = 0

    average_speed = 0
    maximum_speed = 0

    if not players.empty:

        total_players = len(players)

        # Team counts
        team1_count = (
            players["team"] == 1
        ).sum()

        team2_count = (
            players["team"] == 2
        ).sum()

        unknown_count = players["team"].isna().sum()

        # Speed values
        speeds = pd.to_numeric(
            players["speed_kmh"],
            errors="coerce"
        ).dropna()

        # Avoid displaying extreme tracking spikes
        valid_speeds = speeds[
            (speeds >= 0) &
            (speeds <= 40)
        ]

        if len(valid_speeds) > 0:

            average_speed = (
                valid_speeds.mean()
            )

            maximum_speed = (
                valid_speeds.max()
            )

    # Statistics
    y = 100

    cv2.putText(
        frame,
        f"Players Detected : {total_players}",
        (25, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    y += 25

    cv2.putText(
        frame,
        f"Team 1           : {team1_count}",
        (25, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 120, 120),
        1,
        cv2.LINE_AA
    )

    y += 25

    cv2.putText(
        frame,
        f"Team 2           : {team2_count}",
        (25, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (120, 120, 255),
        1,
        cv2.LINE_AA
    )

    y += 25

    cv2.putText(
        frame,
        f"Unknown          : {unknown_count}",
        (25, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (200, 200, 200),
        1,
        cv2.LINE_AA
    )

    y += 25

    cv2.putText(
        frame,
        f"Average Speed    : {average_speed:.1f} km/h",
        (25, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    y += 25

    cv2.putText(
        frame,
        f"Maximum Speed    : {maximum_speed:.1f} km/h",
        (25, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    y += 25

    cv2.putText(
        frame,
        f"Frame            : {frame_number}",
        (25, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (180, 180, 180),
        1,
        cv2.LINE_AA
    )


# --------------------------------------------------
# Process video
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

    # ------------------------------------------------
    # Draw player bounding boxes
    # ------------------------------------------------

    for _, player in players.iterrows():

        x1 = int(player["x1"])
        y1 = int(player["y1"])
        x2 = int(player["x2"])
        y2 = int(player["y2"])

        track_id = int(
            player["track_id"]
        )

        team = player["team"]

        speed = player["speed_kmh"]

        if pd.isna(speed):
            speed = 0

        # Team color
        if pd.isna(team):

            color = (180, 180, 180)
            team_name = "Unknown"

        elif int(team) == 1:

            color = (255, 100, 100)
            team_name = "Team 1"

        else:

            color = (100, 100, 255)
            team_name = "Team 2"

        # Bounding box
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # Player label
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

    # ------------------------------------------------
    # Statistics panel
    # ------------------------------------------------

    draw_statistics_panel(
        frame,
        players,
        frame_number
    )

    # ------------------------------------------------
    # Write frame
    # ------------------------------------------------

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
print("======================================")
print("Match statistics video created")
print("======================================")
print(
    f"Output: {OUTPUT_VIDEO}"
)