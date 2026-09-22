import argparse
from pathlib import Path
from matchlens.pipeline import MatchLensPipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Input football video")
    parser.add_argument("--output", default="outputs/matchlens.mp4")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    MatchLensPipeline(args.config).run(args.source, args.output)

if __name__ == "__main__":
    main()
