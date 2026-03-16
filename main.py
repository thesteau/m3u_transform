from __future__ import annotations

import argparse
import sys

from src import TransformConfig, process_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Transform .m3u playlists using environment-based configuration.")
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to the environment file to load. Defaults to .env in the working directory.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = TransformConfig.from_env(args.env_file)
        results = process_files(config)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for result in results:
        print(f"{result.source.name} -> {result.destination.name} ({result.lines_written} lines)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
