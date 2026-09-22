from matchlens.analytics import calculate_player_analytics


if __name__ == "__main__":
    calculate_player_analytics(
        csv_path="outputs/tracks.csv",
        output_path="outputs/player_analytics.csv",
        fps=25
    )