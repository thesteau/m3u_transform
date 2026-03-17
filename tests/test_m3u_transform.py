import shutil
import uuid
from pathlib import Path

from src.config import TransformConfig
from src.m3u_transform import M3UTransformer
from src.runner import discover_m3u_files


def build_config(input_dir: Path, replace_file: bool = False) -> TransformConfig:
    return TransformConfig(
        input_dir=input_dir,
        initiator="C:/Music/",
        replacement="../../library/",
        kill_line="#EXTINF",
        header="#EXTM3U",
        replace_file=replace_file,
        replace_file_value="-synology",
        target_items=["Mixtape", "LIVE SET"],
        replacement_items=["MixTape", "Live Set"],
    )


def make_test_dir() -> Path:
    root = Path(".tmp-tests")
    root.mkdir(exist_ok=True)
    test_dir = root / str(uuid.uuid4())
    test_dir.mkdir()
    return test_dir


def test_transform_file_creates_new_output() -> None:
    test_dir = make_test_dir()
    try:
        playlist = test_dir / "sample.m3u"
        playlist.write_text(
            "#EXTM3U\n"
            "#EXTINF:123,Example Song\n"
            "C:\\Music\\DJ\\LIVE SET\\Mixtape\\track.mp3\n",
            encoding="utf-8",
        )

        transformer = M3UTransformer(build_config(test_dir))
        result = transformer.transform_file(playlist)

        assert result.destination == test_dir / "sample-synology.m3u"
        assert result.destination.read_text(encoding="utf-8") == (
            "#EXTM3U\n"
            "../../library/Dj/Live Set/MixTape/track.mp3\n"
        )
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_transform_file_can_replace_in_place() -> None:
    test_dir = make_test_dir()
    try:
        playlist = test_dir / "sample.m3u"
        playlist.write_text("#EXTM3U\nC:\\Music\\ARTIST\\Album\\track.mp3\n", encoding="utf-8")

        transformer = M3UTransformer(build_config(test_dir, replace_file=True))
        result = transformer.transform_file(playlist)

        assert result.destination == playlist
        assert playlist.read_text(encoding="utf-8") == (
            "#EXTM3U\n"
            "../../library/Artist/Album/track.mp3\n"
        )
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_discover_m3u_files_returns_only_playlists() -> None:
    test_dir = make_test_dir()
    try:
        first = test_dir / "a.m3u"
        second = test_dir / "b.M3U"
        note = test_dir / "notes.txt"
        first.write_text("#EXTM3U\n", encoding="utf-8")
        second.write_text("#EXTM3U\n", encoding="utf-8")
        note.write_text("ignore me\n", encoding="utf-8")

        results = discover_m3u_files(test_dir)

        assert results == [first, second]
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)
