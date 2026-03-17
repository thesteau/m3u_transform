from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


LIST_SEPARATOR = "||"


def _to_bool(value: str, env_name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{env_name} must be a boolean value.")


def _required_env(env_name: str) -> str:
    value = os.getenv(env_name, "").strip()
    if not value:
        raise ValueError(f"{env_name} is required.")
    return value


def _env_or_default(env_name: str, default: str = "") -> str:
    return os.getenv(env_name, default).strip()


def _optional_list(env_name: str) -> list[str]:
    value = os.getenv(env_name, "").strip()
    if not value:
        return []
    return [item for item in (part.strip() for part in value.split(LIST_SEPARATOR)) if item]


@dataclass(frozen=True)
class TransformConfig:
    input_dir: Path
    initiator: str
    replacement: str
    kill_line: str
    header: str
    replace_file: bool
    replace_file_value: str
    target_items: list[str]
    replacement_items: list[str]

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "TransformConfig":
        load_dotenv(dotenv_path=env_file, override=False)

        input_dir = Path(_required_env("INPUT_DIR"))
        initiator = _env_or_default("INITIATOR")
        replacement = _env_or_default("REPLACEMENT")
        kill_line = _env_or_default("KILL_LINE")
        header = _env_or_default("HEADER", "#EXTM3U")
        replace_file = _to_bool(_env_or_default("REPLACE_FILE", "false"), "REPLACE_FILE")
        replace_file_value = _env_or_default("REPLACE_FILE_VALUE", "-transformed")
        target_items = _optional_list("TARGET_ITEMS")
        replacement_items = _optional_list("REPLACEMENT_ITEMS")

        if bool(initiator) != bool(replacement):
            raise ValueError("INITIATOR and REPLACEMENT must both be set or both be empty.")

        if len(target_items) != len(replacement_items):
            raise ValueError("TARGET_ITEMS and REPLACEMENT_ITEMS must contain the same number of values.")

        return cls(
            input_dir=input_dir,
            initiator=initiator,
            replacement=replacement,
            kill_line=kill_line,
            header=header,
            replace_file=replace_file,
            replace_file_value=replace_file_value,
            target_items=target_items,
            replacement_items=replacement_items,
        )
