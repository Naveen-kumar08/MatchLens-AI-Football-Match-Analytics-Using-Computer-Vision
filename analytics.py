import pandas as pd
import numpy as np


def calculate_player_analytics(
    csv_path="outputs/tracks.csv",
    output_path="outputs/player_analytics.csv",
    fps=25
):
    # Load tracking data
    df = pd.read_csv(csv_path)

    required_columns = [
        "frame",
        "track_id",
        "team",
        "pitch_x_m",
        "pitch_y_m"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    # Keep only player detections
    if "class" in df.columns:
        df = df[df["class"] == "player"].copy()

    # Sort correctly
    df = df.sort_values(
        ["track_id", "frame"]
    ).copy()

    # Time between observations
    df["dt"] = (
        df.groupby("track_id")["frame"].diff() / fps
    )

    # Position change
    df["dx"] = (
        df.groupby("track_id")["pitch_x_m"].diff()
    )

    df["dy"] = (
        df.groupby("track_id")["pitch_y_m"].diff()
    )

    # Distance travelled between frames
    df["distance_m"] = np.sqrt(
        df["dx"] ** 2 +
        df["dy"] ** 2
    )

    # Speed in m/s
    df["speed_mps"] = (
        df["distance_m"] / df["dt"]
    )

    # Invalid values
    df.loc[
        (df["dt"] <= 0) |
        (df["dt"].isna()),
        "speed_mps"
    ] = np.nan

    # Remove unrealistic tracking jumps
    df.loc[
        df["speed_mps"] > 12,
        "speed_mps"
    ] = np.nan

    # Convert to km/h
    df["speed_kmh"] = (
        df["speed_mps"] * 3.6
    )

    # Summary for each player
    summary = (
        df.groupby(
            ["track_id", "team"],
            dropna=False
        )
        .agg(
            total_distance_m=(
                "distance_m",
                "sum"
            ),
            max_speed_kmh=(
                "speed_kmh",
                "max"
            ),
            average_speed_kmh=(
                "speed_kmh",
                "mean"
            ),
            frames_tracked=(
                "frame",
                "count"
            )
        )
        .reset_index()
    )

    # Convert metres to kilometres
    summary["total_distance_km"] = (
        summary["total_distance_m"] / 1000
    )

    # Round values
    summary["total_distance_m"] = (
        summary["total_distance_m"].round(2)
    )

    summary["total_distance_km"] = (
        summary["total_distance_km"].round(3)
    )

    summary["max_speed_kmh"] = (
        summary["max_speed_kmh"].round(2)
    )

    summary["average_speed_kmh"] = (
        summary["average_speed_kmh"].round(2)
    )

    # Save detailed frame-by-frame data
    df.to_csv(
        "outputs/tracks_with_speed.csv",
        index=False
    )

    # Save player summary
    summary.to_csv(
        output_path,
        index=False
    )

    print("\n===================================")
    print("MATCHLENS AI - PLAYER ANALYTICS")
    print("===================================")

    print(
        f"\nSaved detailed data:"
        f" outputs/tracks_with_speed.csv"
    )

    print(
        f"Saved player summary:"
        f" {output_path}"
    )

    print("\nPlayer Statistics:\n")

    print(
        summary.to_string(index=False)
    )

    return summary