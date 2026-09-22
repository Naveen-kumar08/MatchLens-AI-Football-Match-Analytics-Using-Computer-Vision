import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_heatmap(
    csv_path="outputs/tracks.csv",
    output_path="outputs/player_heatmap.png"
):
    df = pd.read_csv(csv_path)

    # Keep only player detections
    if "class" in df.columns:
        df = df[df["class"] == "player"].copy()

    # Remove invalid coordinates
    df = df.dropna(
        subset=["pitch_x_m", "pitch_y_m"]
    )

    x = df["pitch_x_m"].values
    y = df["pitch_y_m"].values

    # Create pitch
    fig, ax = plt.subplots(
        figsize=(12, 7)
    )

    # Heatmap
    heatmap, xedges, yedges = np.histogram2d(
        x,
        y,
        bins=[52, 34],
        range=[
            [0, 105],
            [0, 68]
        ]
    )

    ax.imshow(
        heatmap.T,
        origin="lower",
        extent=[0, 105, 0, 68],
        aspect="auto",
        interpolation="gaussian"
    )

    # Pitch boundary
    ax.plot(
        [0, 105, 105, 0, 0],
        [0, 0, 68, 68, 0]
    )

    # Halfway line
    ax.plot(
        [52.5, 52.5],
        [0, 68]
    )

    # Center circle
    circle = plt.Circle(
        (52.5, 34),
        9.15,
        fill=False
    )
    ax.add_patch(circle)

    # Penalty boxes
    ax.plot(
        [0, 16.5, 16.5, 0],
        [13.84, 13.84, 54.16, 54.16]
    )

    ax.plot(
        [105, 88.5, 88.5, 105],
        [13.84, 13.84, 54.16, 54.16]
    )

    ax.set_xlim(0, 105)
    ax.set_ylim(0, 68)

    ax.set_xlabel("Pitch X (metres)")
    ax.set_ylabel("Pitch Y (metres)")
    ax.set_title("MatchLens AI - Player Movement Heatmap")

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=200
    )

    plt.close()

    print(
        f"Heatmap saved: {output_path}"
    )


if __name__ == "__main__":
    create_heatmap()