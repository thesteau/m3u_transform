from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.config import TransformConfig


@dataclass
class TransformationResult:
    source: Path
    destination: Path
    lines_written: int


class M3UTransformer:
    def __init__(self, config: TransformConfig) -> None:
        self.config = config

    def transform_file(self, source_file: Path) -> TransformationResult:
        lines = source_file.read_text(encoding="utf-8").splitlines()
        transformed_lines = self._transform_lines(lines)
        destination = self._resolve_output_path(source_file)
        destination.write_text("\n".join(transformed_lines) + "\n", encoding="utf-8")
        return TransformationResult(
            source=source_file,
            destination=destination,
            lines_written=len(transformed_lines),
        )

    def _transform_lines(self, lines: list[str]) -> list[str]:
        output: list[str] = [self.config.header]

        for raw_line in lines:
            line = raw_line.strip()
            if not line or line == self.config.header:
                continue

            normalized = line.replace("\\", "/")
            if self.config.kill_line and self.config.kill_line in normalized:
                continue

            normalized = self._title_case_artist_segment(normalized)
            normalized = self._replace_items(normalized)
            normalized = self._replace_prefix(normalized)
            output.append(normalized)

        return output

    def _replace_prefix(self, line: str) -> str:
        if self.config.initiator and line.startswith(self.config.initiator):
            return f"{self.config.replacement}{line[len(self.config.initiator):]}"
        return line

    def _replace_items(self, line: str) -> str:
        updated = line
        for target, replacement in zip(self.config.target_items, self.config.replacement_items):
            updated = updated.replace(target, replacement)
        return updated

    def _title_case_artist_segment(self, line: str) -> str:
        segments = line.split("/")
        if len(segments) > 2 and segments[2].isupper():
            segments[2] = segments[2].title()
            return "/".join(segments)
        return line

    def _resolve_output_path(self, source_file: Path) -> Path:
        if self.config.replace_file:
            return source_file
        return source_file.with_name(f"{source_file.stem}{self.config.replace_file_value}{source_file.suffix}")
