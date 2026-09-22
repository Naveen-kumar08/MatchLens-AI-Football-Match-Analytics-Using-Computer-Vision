import pandas as pd
import matplotlib.pyplot as plt


def create_speed_chart():
    input_path = "outputs/player_analytics.csv"
    output_path = "outputs/player_speed.png"

    df = pd.read_csv(input_path)

    # Remove invalid values
    df = df.dropna(
        subset=[
            "track_id",
            "max_speed_kmh",
            "average_speed_kmh"
        ]
    )

    # Sort by maximum speed
    df = df.sort_values(
        "max_speed_kmh",
        ascending=False
    )

    # Top 20 tracked players
    df = df.head(20)

    labels = df["track_id"].astype(int).astype(str)

    x = range(len(df))
    width = 0.35

    plt.figure(figsize=(13, 7))

    plt.bar(
        [i - width / 2 for i in x],
        df["max_speed_kmh"],
        width=width,
        label="Maximum Speed"
    )

    plt.bar(
        [i + width / 2 for i in x],
        df["average_speed_kmh"],
        width=width,
        label="Average Speed"
    )

    plt.xlabel("Track ID")
    plt.ylabel("Speed (km/h)")
    plt.title(
        "MatchLens AI - Player Speed Analysis"
    )

    plt.xticks(
        list(x),
        labels,
        rotation=45
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=200
    )

    plt.close()

    print(
        f"Speed chart saved: {output_path}"
    )


if __name__ == "__main__":
    create_speed_chart()