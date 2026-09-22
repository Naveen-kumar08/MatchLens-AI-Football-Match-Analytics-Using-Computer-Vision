import os
import math
from collections import defaultdict, deque

import cv2
import numpy as np
import pandas as pd


# ============================================================
# MATCHLENS AI
# FINAL PROFESSIONAL FOOTBALL ANALYTICS VIDEO
# ============================================================

INPUT_VIDEO = "input.mp4"

TRACKS_FILE = "outputs/tracks.csv"
SPEED_FILE = "outputs/tracks_with_speed.csv"

OUTPUT_VIDEO = "outputs/MatchLens_AI_Final.mp4"

# ============================================================
# FOOTBALL PITCH
# ============================================================

PITCH_LENGTH = 105.0
PITCH_WIDTH = 68.0


# ============================================================
# FINAL DASHBOARD SIZE
# ============================================================

OUTPUT_WIDTH = 1600
OUTPUT_HEIGHT = 900

HEADER_HEIGHT = 100

MAIN_WIDTH = 1120
SIDE_WIDTH = OUTPUT_WIDTH - MAIN_WIDTH


# ============================================================
# TACTICAL PITCH POSITION
# ============================================================

TACTICAL_X = MAIN_WIDTH + 25
TACTICAL_Y = 300

TACTICAL_W = SIDE_WIDTH - 50
TACTICAL_H = 390


# ============================================================
# TRAJECTORY
# ============================================================

TRAIL_LENGTH = 40


# ============================================================
# COLORS - OpenCV uses BGR
# ============================================================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

DARK_BACKGROUND = (12, 10, 7)

# TEAM 1 = BLUE
TEAM_1_COLOR = (255, 0, 0)

# TEAM 2 = GREEN
TEAM_2_COLOR = (0, 220, 0)

# UNKNOWN = GRAY
UNKNOWN_COLOR = (180, 180, 180)

# BALL = YELLOW
BALL_COLOR = (0, 255, 255)

# Cyan
CYAN = (255, 220, 0)


# ============================================================
# TEAM COLOR FUNCTION
# ============================================================

def get_team_color(team):

    if pd.isna(team):
        return UNKNOWN_COLOR

    try:

        team_number = int(float(team))

        if team_number == 1:
            return TEAM_1_COLOR

        if team_number == 2:
            return TEAM_2_COLOR

    except Exception:
        pass

    return UNKNOWN_COLOR


# ============================================================
# TEAM NAME
# ============================================================

def get_team_name(team):

    if pd.isna(team):
        return "UNKNOWN"

    try:

        team_number = int(float(team))

        if team_number == 1:
            return "TEAM 1"

        if team_number == 2:
            return "TEAM 2"

    except Exception:
        pass

    return "UNKNOWN"


# ============================================================
# SAFE FLOAT
# ============================================================

def safe_float(value, default=0.0):

    try:

        if pd.isna(value):
            return default

        return float(value)

    except Exception:

        return default


# ============================================================
# SAFE INTEGER
# ============================================================

def safe_int(value, default=-1):

    try:

        if pd.isna(value):
            return default

        return int(float(value))

    except Exception:

        return default


# ============================================================
# TEXT
# ============================================================

def draw_text(
    image,
    text,
    position,
    size=0.5,
    color=WHITE,
    thickness=1
):

    cv2.putText(
        image,
        str(text),
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        size,
        color,
        thickness,
        cv2.LINE_AA
    )


# ============================================================
# FIT VIDEO INSIDE DASHBOARD
# ============================================================

def fit_video(
    frame,
    target_width,
    target_height
):

    frame_height, frame_width = frame.shape[:2]

    if frame_width <= 0 or frame_height <= 0:

        return np.zeros(
            (target_height, target_width, 3),
            dtype=np.uint8
        )

    scale = min(
        target_width / frame_width,
        target_height / frame_height
    )

    new_width = int(
        frame_width * scale
    )

    new_height = int(
        frame_height * scale
    )

    resized = cv2.resize(
        frame,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR
    )

    canvas = np.zeros(
        (target_height, target_width, 3),
        dtype=np.uint8
    )

    x = (
        target_width -
        new_width
    ) // 2

    y = (
        target_height -
        new_height
    ) // 2

    canvas[
        y:y + new_height,
        x:x + new_width
    ] = resized

    return canvas


# ============================================================
# PITCH TO SCREEN
# ============================================================

def pitch_to_pixel(
    x_m,
    y_m
):

    x_m = max(
        0,
        min(PITCH_LENGTH, x_m)
    )

    y_m = max(
        0,
        min(PITCH_WIDTH, y_m)
    )

    pixel_x = int(
        TACTICAL_X +
        (x_m / PITCH_LENGTH) *
        TACTICAL_W
    )

    pixel_y = int(
        TACTICAL_Y +
        (y_m / PITCH_WIDTH) *
        TACTICAL_H
    )

    return pixel_x, pixel_y


# ============================================================
# DRAW TACTICAL PITCH
# ============================================================

def draw_tactical_pitch(image):

    # Pitch background
    cv2.rectangle(
        image,
        (
            TACTICAL_X,
            TACTICAL_Y
        ),
        (
            TACTICAL_X + TACTICAL_W,
            TACTICAL_Y + TACTICAL_H
        ),
        (30, 75, 30),
        -1
    )

    # Outer boundary
    cv2.rectangle(
        image,
        (
            TACTICAL_X,
            TACTICAL_Y
        ),
        (
            TACTICAL_X + TACTICAL_W,
            TACTICAL_Y + TACTICAL_H
        ),
        WHITE,
        2
    )

    # Centre line
    centre_x = (
        TACTICAL_X +
        TACTICAL_W // 2
    )

    cv2.line(
        image,
        (
            centre_x,
            TACTICAL_Y
        ),
        (
            centre_x,
            TACTICAL_Y + TACTICAL_H
        ),
        WHITE,
        2
    )

    # Centre circle
    centre_y = (
        TACTICAL_Y +
        TACTICAL_H // 2
    )

    centre = (
        centre_x,
        centre_y
    )

    radius = int(
        min(
            TACTICAL_W,
            TACTICAL_H
        ) * 0.13
    )

    cv2.circle(
        image,
        centre,
        radius,
        WHITE,
        2
    )

    cv2.circle(
        image,
        centre,
        3,
        WHITE,
        -1
    )

    # Penalty boxes
    penalty_width = int(
        TACTICAL_W * 0.16
    )

    penalty_height = int(
        TACTICAL_H * 0.44
    )

    # Left penalty box
    cv2.rectangle(
        image,
        (
            TACTICAL_X,
            centre_y - penalty_height // 2
        ),
        (
            TACTICAL_X + penalty_width,
            centre_y + penalty_height // 2
        ),
        WHITE,
        2
    )

    # Right penalty box
    cv2.rectangle(
        image,
        (
            TACTICAL_X + TACTICAL_W - penalty_width,
            centre_y - penalty_height // 2
        ),
        (
            TACTICAL_X + TACTICAL_W,
            centre_y + penalty_height // 2
        ),
        WHITE,
        2
    )

    # Goal boxes
    goal_width = int(
        TACTICAL_W * 0.055
    )

    goal_height = int(
        TACTICAL_H * 0.20
    )

    cv2.rectangle(
        image,
        (
            TACTICAL_X,
            centre_y - goal_height // 2
        ),
        (
            TACTICAL_X + goal_width,
            centre_y + goal_height // 2
        ),
        WHITE,
        2
    )

    cv2.rectangle(
        image,
        (
            TACTICAL_X + TACTICAL_W - goal_width,
            centre_y - goal_height // 2
        ),
        (
            TACTICAL_X + TACTICAL_W,
            centre_y + goal_height // 2
        ),
        WHITE,
        2
    )


# ============================================================
# CALCULATE PLAYER DISTANCES
# ============================================================

def calculate_player_distances(df):

    distance_map = {}

    players = df[
        df["class"] == "player"
    ].copy()

    required = [
        "track_id",
        "frame",
        "pitch_x_m",
        "pitch_y_m"
    ]

    for column in required:

        if column not in players.columns:

            return distance_map

    players = players.dropna(
        subset=required
    )

    players = players.sort_values(
        [
            "track_id",
            "frame"
        ]
    )

    for track_id, group in players.groupby(
        "track_id"
    ):

        dx = group[
            "pitch_x_m"
        ].diff()

        dy = group[
            "pitch_y_m"
        ].diff()

        distance = np.sqrt(
            dx ** 2 +
            dy ** 2
        )

        total_distance = distance.sum()

        distance_map[
            int(track_id)
        ] = float(
            total_distance
        )

    return distance_map


# ============================================================
# LOAD DATA
# ============================================================

print()
print("================================================")
print("MATCHLENS AI")
print("FINAL PROFESSIONAL ANALYTICS VIDEO")
print("================================================")
print()

if not os.path.exists(INPUT_VIDEO):

    raise FileNotFoundError(
        f"Input video not found: {INPUT_VIDEO}"
    )


if not os.path.exists(TRACKS_FILE):

    raise FileNotFoundError(
        f"Tracking file not found: {TRACKS_FILE}"
    )


if os.path.exists(SPEED_FILE):

    print(
        "Loading:",
        SPEED_FILE
    )

    df = pd.read_csv(
        SPEED_FILE
    )

else:

    print(
        "WARNING: tracks_with_speed.csv not found."
    )

    print(
        "Using tracks.csv."
    )

    df = pd.read_csv(
        TRACKS_FILE
    )


print(
    f"Total tracking rows: {len(df):,}"
)


# ============================================================
# NORMALIZE DATA
# ============================================================

df["class"] = (
    df["class"]
    .astype(str)
    .str.lower()
)


df["frame"] = pd.to_numeric(
    df["frame"],
    errors="coerce"
).fillna(0).astype(int)


df["track_id"] = pd.to_numeric(
    df["track_id"],
    errors="coerce"
).fillna(-1).astype(int)


# ============================================================
# FRAME GROUPS
# ============================================================

frame_groups = {}

for frame_number, group in df.groupby(
    "frame"
):

    frame_groups[
        int(frame_number)
    ] = group


# ============================================================
# DISTANCE
# ============================================================

distance_map = (
    calculate_player_distances(df)
)


top_distance_players = sorted(
    distance_map.items(),
    key=lambda x: x[1],
    reverse=True
)[:3]


# ============================================================
# VIDEO
# ============================================================

cap = cv2.VideoCapture(
    INPUT_VIDEO
)

if not cap.isOpened():

    raise RuntimeError(
        "Could not open input.mp4"
    )


fps = cap.get(
    cv2.CAP_PROP_FPS
)

if fps <= 0:

    fps = 25.0


source_width = int(
    cap.get(
        cv2.CAP_PROP_FRAME_WIDTH
    )
)

source_height = int(
    cap.get(
        cv2.CAP_PROP_FRAME_HEIGHT
    )
)

total_frames = int(
    cap.get(
        cv2.CAP_PROP_FRAME_COUNT
    )
)


print(
    f"Source: "
    f"{source_width} x "
    f"{source_height}"
)

print(
    f"FPS: {fps:.2f}"
)

print(
    f"Frames: {total_frames}"
)


# ============================================================
# OUTPUT
# ============================================================

os.makedirs(
    "outputs",
    exist_ok=True
)


fourcc = cv2.VideoWriter_fourcc(
    *"mp4v"
)


writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    fps,
    (
        OUTPUT_WIDTH,
        OUTPUT_HEIGHT
    )
)


if not writer.isOpened():

    raise RuntimeError(
        "Could not create output video."
    )


# ============================================================
# TRAJECTORIES
# ============================================================

trails = defaultdict(
    lambda: deque(
        maxlen=TRAIL_LENGTH
    )
)


# ============================================================
# MAIN LOOP
# ============================================================

frame_number = 0


while True:

    ret, frame = cap.read()

    if not ret:

        break


    # ========================================================
    # DASHBOARD
    # ========================================================

    dashboard = np.zeros(
        (
            OUTPUT_HEIGHT,
            OUTPUT_WIDTH,
            3
        ),
        dtype=np.uint8
    )

    dashboard[:] = (
        DARK_BACKGROUND
    )


    # ========================================================
    # HEADER
    # ========================================================

    cv2.rectangle(
        dashboard,
        (0, 0),
        (
            OUTPUT_WIDTH,
            HEADER_HEIGHT
        ),
        (8, 7, 5),
        -1
    )


    cv2.line(
        dashboard,
        (
            0,
            HEADER_HEIGHT - 1
        ),
        (
            OUTPUT_WIDTH,
            HEADER_HEIGHT - 1
        ),
        (70, 70, 70),
        1
    )


    draw_text(
        dashboard,
        f"FRAME {frame_number:04d}",
        (25, 38),
        0.70,
        (0, 220, 255),
        2
    )


    draw_text(
        dashboard,
        "MATCHLENS AI",
        (25, 75),
        0.55,
        WHITE,
        2
    )


    # ========================================================
    # CURRENT FRAME DATA
    # ========================================================

    group = frame_groups.get(
        frame_number,
        pd.DataFrame()
    )


    if not group.empty:

        players = group[
            group["class"] == "player"
        ].copy()

        balls = group[
            group["class"].isin(
                [
                    "ball",
                    "sports ball"
                ]
            )
        ].copy()

    else:

        players = pd.DataFrame()

        balls = pd.DataFrame()


    # ========================================================
    # TEAM COUNTS
    # ========================================================

    team_1_count = 0
    team_2_count = 0
    unknown_count = 0


    for _, player in players.iterrows():

        team = player.get(
            "team",
            np.nan
        )

        if pd.isna(team):

            unknown_count += 1

            continue


        try:

            team_number = int(
                float(team)
            )

            if team_number == 1:

                team_1_count += 1

            elif team_number == 2:

                team_2_count += 1

            else:

                unknown_count += 1

        except Exception:

            unknown_count += 1


    # ========================================================
    # HEADER TEAM INFORMATION
    # ========================================================

    draw_text(
        dashboard,
        f"TEAM 1: {team_1_count}",
        (480, 38),
        0.55,
        TEAM_1_COLOR,
        2
    )


    draw_text(
        dashboard,
        f"TEAM 2: {team_2_count}",
        (690, 38),
        0.55,
        TEAM_2_COLOR,
        2
    )


    draw_text(
        dashboard,
        f"UNKNOWN: {unknown_count}",
        (890, 38),
        0.42,
        UNKNOWN_COLOR,
        1
    )


    # ========================================================
    # VIDEO SCALING
    # ========================================================

    video_area_height = (
        OUTPUT_HEIGHT -
        HEADER_HEIGHT
    )


    scale = min(
        MAIN_WIDTH / source_width,
        video_area_height / source_height
    )


    resized_width = int(
        source_width * scale
    )


    resized_height = int(
        source_height * scale
    )


    offset_x = (
        MAIN_WIDTH -
        resized_width
    ) // 2


    offset_y = (
        HEADER_HEIGHT +
        (
            video_area_height -
            resized_height
        ) // 2
    )


    resized_frame = cv2.resize(
        frame,
        (
            resized_width,
            resized_height
        ),
        interpolation=cv2.INTER_LINEAR
    )


    dashboard[
        offset_y:
        offset_y + resized_height,
        offset_x:
        offset_x + resized_width
    ] = resized_frame


    # ========================================================
    # DRAW PLAYER BOUNDING BOXES
    # ========================================================

    for _, player in players.iterrows():

        track_id = safe_int(
            player.get(
                "track_id",
                -1
            )
        )


        if track_id < 0:

            continue


        x1 = safe_float(
            player.get(
                "x1",
                0
            )
        )


        y1 = safe_float(
            player.get(
                "y1",
                0
            )
        )


        x2 = safe_float(
            player.get(
                "x2",
                0
            )
        )


        y2 = safe_float(
            player.get(
                "y2",
                0
            )
        )


        # Convert original coordinates
        # to dashboard coordinates

        screen_x1 = int(
            offset_x +
            x1 * scale
        )

        screen_y1 = int(
            offset_y +
            y1 * scale
        )


        screen_x2 = int(
            offset_x +
            x2 * scale
        )

        screen_y2 = int(
            offset_y +
            y2 * scale
        )


        # ====================================================
        # TEAM COLOR
        # ====================================================

        team = player.get(
            "team",
            np.nan
        )


        color = get_team_color(
            team
        )


        team_label = get_team_name(
            team
        )


        # ====================================================
        # FOOT POINT
        # ====================================================

        foot_x = int(
            offset_x +
            (
                (x1 + x2) / 2
            ) * scale
        )


        foot_y = int(
            offset_y +
            y2 * scale
        )


        # ====================================================
        # TRAJECTORY
        # ====================================================

        trails[
            track_id
        ].append(
            (
                foot_x,
                foot_y
            )
        )


        points = list(
            trails[
                track_id
            ]
        )


        for i in range(
            1,
            len(points)
        ):

            cv2.line(
                dashboard,
                points[i - 1],
                points[i],
                color,
                2,
                cv2.LINE_AA
            )


        # ====================================================
        # BOUNDING BOX
        # ====================================================

        cv2.rectangle(
            dashboard,
            (
                screen_x1,
                screen_y1
            ),
            (
                screen_x2,
                screen_y2
            ),
            color,
            3
        )


        # ====================================================
        # PLAYER ID LABEL BACKGROUND
        # ====================================================

        speed = safe_float(
            player.get(
                "speed_kmh",
                0
            )
        )


        if speed < 0:

            speed = 0


        label = (
            f"ID {track_id}"
            f" | {team_label}"
            f" | {speed:.1f} km/h"
        )


        text_size = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.40,
            1
        )[0]


        label_x = screen_x1

        label_y = max(
            screen_y1 - 8,
            HEADER_HEIGHT + 20
        )


        cv2.rectangle(
            dashboard,
            (
                label_x,
                label_y - text_size[1] - 6
            ),
            (
                label_x + text_size[0] + 6,
                label_y + 3
            ),
            color,
            -1
        )


        # Black text for visibility
        draw_text(
            dashboard,
            label,
            (
                label_x + 3,
                label_y - 2
            ),
            0.40,
            BLACK,
            1
        )


    # ========================================================
    # BALL
    # ========================================================

    ball_pitch_x = None
    ball_pitch_y = None


    if not balls.empty:

        ball = balls.iloc[0]


        bx1 = safe_float(
            ball.get(
                "x1",
                0
            )
        )

        by1 = safe_float(
            ball.get(
                "y1",
                0
            )
        )

        bx2 = safe_float(
            ball.get(
                "x2",
                0
            )
        )

        by2 = safe_float(
            ball.get(
                "y2",
                0
            )
        )


        ball_center_x = (
            bx1 + bx2
        ) / 2


        ball_center_y = (
            by1 + by2
        ) / 2


        ball_screen_x = int(
            offset_x +
            ball_center_x * scale
        )


        ball_screen_y = int(
            offset_y +
            ball_center_y * scale
        )


        # Yellow ball
        cv2.circle(
            dashboard,
            (
                ball_screen_x,
                ball_screen_y
            ),
            8,
            BALL_COLOR,
            -1
        )


        cv2.circle(
            dashboard,
            (
                ball_screen_x,
                ball_screen_y
            ),
            12,
            WHITE,
            2
        )


        # Pitch coordinates
        ball_pitch_x = safe_float(
            ball.get(
                "pitch_x_m",
                np.nan
            ),
            np.nan
        )


        ball_pitch_y = safe_float(
            ball.get(
                "pitch_y_m",
                np.nan
            ),
            np.nan
        )


    # ========================================================
    # RIGHT SIDE PANEL
    # ========================================================

    side_x = MAIN_WIDTH


    cv2.rectangle(
        dashboard,
        (
            side_x,
            HEADER_HEIGHT
        ),
        (
            OUTPUT_WIDTH,
            OUTPUT_HEIGHT
        ),
        (
            12,
            11,
            8
        ),
        -1
    )


    # ========================================================
    # TEAM LEGEND
    # ========================================================

    draw_text(
        dashboard,
        "TEAM COLORS",
        (
            side_x + 25,
            130
        ),
        0.52,
        WHITE,
        2
    )


    # Blue
    cv2.rectangle(
        dashboard,
        (
            side_x + 25,
            145
        ),
        (
            side_x + 50,
            165
        ),
        TEAM_1_COLOR,
        -1
    )


    draw_text(
        dashboard,
        "TEAM 1",
        (
            side_x + 60,
            162
        ),
        0.40,
        TEAM_1_COLOR,
        1
    )


    # Green
    cv2.rectangle(
        dashboard,
        (
            side_x + 150,
            145
        ),
        (
            side_x + 175,
            165
        ),
        TEAM_2_COLOR,
        -1
    )


    draw_text(
        dashboard,
        "TEAM 2",
        (
            side_x + 185,
            162
        ),
        0.40,
        TEAM_2_COLOR,
        1
    )


    # Gray
    cv2.rectangle(
        dashboard,
        (
            side_x + 275,
            145
        ),
        (
            side_x + 300,
            165
        ),
        UNKNOWN_COLOR,
        -1
    )


    draw_text(
        dashboard,
        "UNKNOWN",
        (
            side_x + 310,
            162
        ),
        0.40,
        UNKNOWN_COLOR,
        1
    )


    # ========================================================
    # PLAYER COUNTS
    # ========================================================

    draw_text(
        dashboard,
        f"Team 1 Players: {team_1_count}",
        (
            side_x + 25,
            200
        ),
        0.43,
        TEAM_1_COLOR,
        1
    )


    draw_text(
        dashboard,
        f"Team 2 Players: {team_2_count}",
        (
            side_x + 25,
            225
        ),
        0.43,
        TEAM_2_COLOR,
        1
    )


    draw_text(
        dashboard,
        f"Unknown: {unknown_count}",
        (
            side_x + 25,
            250
        ),
        0.40,
        UNKNOWN_COLOR,
        1
    )


    # ========================================================
    # TEAM SPREAD
    # ========================================================

    def calculate_team_spread(
        team_number
    ):

        if players.empty:

            return 0.0, 0.0


        numeric_team = pd.to_numeric(
            players["team"],
            errors="coerce"
        )


        team_players = players[
            numeric_team ==
            team_number
        ].copy()


        if team_players.empty:

            return 0.0, 0.0


        if (
            "pitch_x_m" not in
            team_players.columns
        ):

            return 0.0, 0.0


        if (
            "pitch_y_m" not in
            team_players.columns
        ):

            return 0.0, 0.0


        team_players = team_players.dropna(
            subset=[
                "pitch_x_m",
                "pitch_y_m"
            ]
        )


        if team_players.empty:

            return 0.0, 0.0


        spread_x = (
            team_players[
                "pitch_x_m"
            ].max()
            -
            team_players[
                "pitch_x_m"
            ].min()
        )


        spread_y = (
            team_players[
                "pitch_y_m"
            ].max()
            -
            team_players[
                "pitch_y_m"
            ].min()
        )


        return (
            float(spread_x),
            float(spread_y)
        )


    spread_1_x, spread_1_y = (
        calculate_team_spread(1)
    )


    spread_2_x, spread_2_y = (
        calculate_team_spread(2)
    )


    draw_text(
        dashboard,
        (
            f"Team 1 Spread: "
            f"{spread_1_x:.1f}m x "
            f"{spread_1_y:.1f}m"
        ),
        (
            side_x + 25,
            275
        ),
        0.38,
        TEAM_1_COLOR,
        1
    )


    draw_text(
        dashboard,
        (
            f"Team 2 Spread: "
            f"{spread_2_x:.1f}m x "
            f"{spread_2_y:.1f}m"
        ),
        (
            side_x + 25,
            295
        ),
        0.38,
        TEAM_2_COLOR,
        1
    )


    # ========================================================
    # TACTICAL MAP TITLE
    # ========================================================

    draw_text(
        dashboard,
        "TACTICAL 2D PITCH MAP (105m x 68m)",
        (
            side_x + 25,
            325
        ),
        0.45,
        WHITE,
        1
    )


    # ========================================================
    # DRAW PITCH
    # ========================================================

    draw_tactical_pitch(
        dashboard
    )


    # ========================================================
    # TACTICAL PLAYERS
    # ========================================================

    for _, player in players.iterrows():

        pitch_x = safe_float(
            player.get(
                "pitch_x_m",
                np.nan
            ),
            np.nan
        )


        pitch_y = safe_float(
            player.get(
                "pitch_y_m",
                np.nan
            ),
            np.nan
        )


        if (
            np.isnan(pitch_x)
            or
            np.isnan(pitch_y)
        ):

            continue


        tx, ty = pitch_to_pixel(
            pitch_x,
            pitch_y
        )


        color = get_team_color(
            player.get(
                "team",
                np.nan
            )
        )


        track_id = safe_int(
            player.get(
                "track_id",
                -1
            )
        )


        speed = safe_float(
            player.get(
                "speed_kmh",
                0
            )
        )


        # Player circle
        cv2.circle(
            dashboard,
            (
                tx,
                ty
            ),
            11,
            color,
            -1
        )


        # White outline
        cv2.circle(
            dashboard,
            (
                tx,
                ty
            ),
            11,
            WHITE,
            1
        )


        # ID inside marker
        draw_text(
            dashboard,
            str(track_id),
            (
                tx - 7,
                ty + 4
            ),
            0.28,
            BLACK,
            1
        )


        # Speed beside marker
        draw_text(
            dashboard,
            f"{speed:.0f}",
            (
                tx + 14,
                ty + 4
            ),
            0.27,
            WHITE,
            1
        )


    # ========================================================
    # TACTICAL BALL
    # ========================================================

    if (
        ball_pitch_x is not None
        and
        ball_pitch_y is not None
        and
        not np.isnan(ball_pitch_x)
        and
        not np.isnan(ball_pitch_y)
    ):

        bx, by = pitch_to_pixel(
            ball_pitch_x,
            ball_pitch_y
        )


        cv2.circle(
            dashboard,
            (
                bx,
                by
            ),
            7,
            BALL_COLOR,
            -1
        )


        cv2.circle(
            dashboard,
            (
                bx,
                by
            ),
            10,
            WHITE,
            1
        )


        draw_text(
            dashboard,
            "BALL",
            (
                bx + 12,
                by
            ),
            0.30,
            BALL_COLOR,
            1
        )


    # ========================================================
    # POSSESSION ESTIMATE
    # ========================================================

    possession_1 = None
    possession_2 = None


    if (
        ball_pitch_x is not None
        and
        ball_pitch_y is not None
        and
        not np.isnan(ball_pitch_x)
        and
        not np.isnan(ball_pitch_y)
        and
        not players.empty
    ):

        nearest_team = None

        nearest_distance = float(
            "inf"
        )


        for _, player in players.iterrows():

            px = safe_float(
                player.get(
                    "pitch_x_m",
                    np.nan
                ),
                np.nan
            )


            py = safe_float(
                player.get(
                    "pitch_y_m",
                    np.nan
                ),
                np.nan
            )


            if (
                np.isnan(px)
                or
                np.isnan(py)
            ):

                continue


            distance = math.sqrt(
                (
                    px -
                    ball_pitch_x
                ) ** 2
                +
                (
                    py -
                    ball_pitch_y
                ) ** 2
            )


            if distance < nearest_distance:

                nearest_distance = distance

                try:

                    nearest_team = int(
                        float(
                            player.get(
                                "team"
                            )
                        )
                    )

                except Exception:

                    nearest_team = None


        if nearest_team == 1:

            possession_1 = 70
            possession_2 = 30

        elif nearest_team == 2:

            possession_1 = 30
            possession_2 = 70


    # ========================================================
    # POSSESSION DISPLAY
    # ========================================================

    if (
        possession_1 is not None
        and
        possession_2 is not None
    ):

        draw_text(
            dashboard,
            f"TEAM 1: {possession_1}%",
            (
                480,
                65
            ),
            0.50,
            TEAM_1_COLOR,
            2
        )


        draw_text(
            dashboard,
            f"TEAM 2: {possession_2}%",
            (
                690,
                65
            ),
            0.50,
            TEAM_2_COLOR,
            2
        )


        # Possession bar
        bar_x = 480
        bar_y = 80
        bar_width = 400
        bar_height = 10


        cv2.rectangle(
            dashboard,
            (
                bar_x,
                bar_y
            ),
            (
                bar_x + bar_width,
                bar_y + bar_height
            ),
            (40, 40, 40),
            -1
        )


        team_1_width = int(
            bar_width *
            possession_1 /
            100
        )


        cv2.rectangle(
            dashboard,
            (
                bar_x,
                bar_y
            ),
            (
                bar_x +
                team_1_width,
                bar_y +
                bar_height
            ),
            TEAM_1_COLOR,
            -1
        )


        cv2.rectangle(
            dashboard,
            (
                bar_x +
                team_1_width,
                bar_y
            ),
            (
                bar_x +
                bar_width,
                bar_y +
                bar_height
            ),
            TEAM_2_COLOR,
            -1
        )


    else:

        draw_text(
            dashboard,
            "POSSESSION: N/A",
            (
                480,
                55
            ),
            0.48,
            GRAY,
            1
        )


    # ========================================================
    # TOP DISTANCE PANEL
    # ========================================================

    distance_box_x1 = (
        side_x + 25
    )


    distance_box_y1 = (
        TACTICAL_Y +
        TACTICAL_H +
        25
    )


    distance_box_x2 = (
        OUTPUT_WIDTH -
        25
    )


    distance_box_y2 = (
        distance_box_y1 +
        105
    )


    cv2.rectangle(
        dashboard,
        (
            distance_box_x1,
            distance_box_y1
        ),
        (
            distance_box_x2,
            distance_box_y2
        ),
        (40, 36, 25),
        1
    )


    draw_text(
        dashboard,
        "TOP DISTANCE",
        (
            distance_box_x1 + 12,
            distance_box_y1 + 25
        ),
        0.42,
        (0, 220, 255),
        1
    )


    distance_y = (
        distance_box_y1 +
        48
    )


    for track_id, distance in (
        top_distance_players
    ):

        draw_text(
            dashboard,
            (
                f"ID {track_id}: "
                f"{distance:.1f} m"
            ),
            (
                distance_box_x1 + 12,
                distance_y
            ),
            0.36,
            WHITE,
            1
        )


        distance_y += 20


    # ========================================================
    # SPEED STATISTICS
    # ========================================================

    average_speed = 0.0
    maximum_speed = 0.0


    if (
        not players.empty
        and
        "speed_kmh" in players.columns
    ):

        speeds = pd.to_numeric(
            players[
                "speed_kmh"
            ],
            errors="coerce"
        ).dropna()


        speeds = speeds[
            (speeds >= 0)
            &
            (speeds <= 40)
        ]


        if not speeds.empty:

            average_speed = float(
                speeds.mean()
            )


            maximum_speed = float(
                speeds.max()
            )


    # ========================================================
    # BOTTOM BAR
    # ========================================================

    bottom_y = (
        OUTPUT_HEIGHT -
        25
    )


    draw_text(
        dashboard,
        f"PLAYERS: {len(players)}",
        (
            25,
            bottom_y
        ),
        0.42,
        WHITE,
        1
    )


    draw_text(
        dashboard,
        (
            f"AVG SPEED: "
            f"{average_speed:.1f} km/h"
        ),
        (
            190,
            bottom_y
        ),
        0.42,
        CYAN,
        1
    )


    draw_text(
        dashboard,
        (
            f"MAX SPEED: "
            f"{maximum_speed:.1f} km/h"
        ),
        (
            410,
            bottom_y
        ),
        0.42,
        (0, 220, 255),
        1
    )


    draw_text(
        dashboard,
        "105m x 68m",
        (
            680,
            bottom_y
        ),
        0.42,
        WHITE,
        1
    )


    draw_text(
        dashboard,
        "COMPUTER VISION ANALYTICS",
        (
            1250,
            bottom_y
        ),
        0.36,
        GRAY,
        1
    )


    # ========================================================
    # WRITE FRAME
    # ========================================================

    writer.write(
        dashboard
    )


    frame_number += 1


    if frame_number % 100 == 0:

        print(
            f"Processed "
            f"{frame_number}/"
            f"{total_frames}"
        )


# ============================================================
# RELEASE
# ============================================================

cap.release()

writer.release()


print()
print("================================================")
print("MATCHLENS AI FINAL VIDEO COMPLETED")
print("================================================")
print(
    f"Output: {OUTPUT_VIDEO}"
)
print(
    f"Frames: {frame_number}"
)
print(
    f"Resolution: "
    f"{OUTPUT_WIDTH} x "
    f"{OUTPUT_HEIGHT}"
)
print("================================================")