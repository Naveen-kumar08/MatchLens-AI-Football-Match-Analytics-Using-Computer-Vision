import pandas as pd
import matplotlib.pyplot as plt


def create_distance_chart():
    input_path = "outputs/player_analytics.csv"
    output_path = "outputs/player_distance.png"

    df = pd.read_csv(input_path)

    # Remove invalid distance values
    df = df.dropna(
        subset=["track_id", "total_distance_m"]
    )

    # Sort by total distance
    df = df.sort_values(
        "total_distance_m",
        ascending=False
    )

    # Show top 20 tracked players
    df = df.head(20)

    # Create labels
    labels = df["track_id"].astype(int).astype(str)

    plt.figure(figsize=(12, 7))

    plt.bar(
        labels,
        df["total_distance_m"]
    )

    plt.xlabel("Track ID")
    plt.ylabel("Distance Covered (metres)")
    plt.title(
        "MatchLens AI - Player Distance Analysis"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=200
    )

    plt.close()

    print(
        f"Distance chart saved: {output_path}"
    )


if __name__ == "__main__":
    create_distance_chart()