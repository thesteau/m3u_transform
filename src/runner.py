from __future__ import annotations

from pathlib import Path

from src.config import TransformConfig
from src.m3u_transform import M3UTransformer, TransformationResult


def discover_m3u_files(folder: Path) -> list[Path]:
    if not folder.exists():
        raise FileNotFoundError(f"Input directory does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {folder}")

    files = sorted(path for path in folder.iterdir() if path.is_file() and path.suffix.lower() == ".m3u")
    if not files:
        raise FileNotFoundError(f"No .m3u files found in {folder}")
    return files


def process_files(config: TransformConfig) -> list[TransformationResult]:
    transformer = M3UTransformer(config)
    return [transformer.transform_file(path) for path in discover_m3u_files(config.input_dir)]
