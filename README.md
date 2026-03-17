# M3U Playlist Transformer

This project rebuilds the playlist transformer around a simple `.env` configuration model and a container-friendly workflow. It scans a directory for `.m3u` files, rewrites each playlist, and either saves a sibling output file or replaces the original in place.

## What It Does

For each playlist, the transformer:

1. Normalizes Windows path separators to `/`.
2. Removes lines containing a configured marker.
3. Replaces a configured path prefix.
4. Applies optional string-for-string replacements.
5. Title-cases the third path segment when it is fully uppercase.
6. Writes a clean playlist with a fixed header.

## Configuration

Copy `.env.example` to `.env` and update the values for your environment.

```dotenv
INPUT_DIR=./files
INITIATOR=C:/Music/
REPLACEMENT=../../music/
KILL_LINE=#EXTINF
HEADER=#EXTM3U
REPLACE_FILE=false
REPLACE_FILE_VALUE=-synology
TARGET_ITEMS=OLD_NAME||LIVE SET
REPLACEMENT_ITEMS=New_Name||Live Set
```

Notes:

- `INPUT_DIR` points to the folder containing your `.m3u` files.
- `REPLACE_FILE=false` writes a new file using `REPLACE_FILE_VALUE` as a suffix.
- `REPLACE_FILE=true` overwrites the original file and ignores `REPLACE_FILE_VALUE`.
- `TARGET_ITEMS` and `REPLACEMENT_ITEMS` are optional paired lists separated by `||`.

## Local Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the transformer:

```bash
python main.py --env-file .env
```

## Docker

Build the image:

```bash
docker build -t m3u-transform .
```

Run it:

```bash
docker run --rm --env-file .env -v "${PWD}/files:/app/files" m3u-transform
```

## Docker Compose

1. Create a local `files/` directory for your playlists.
2. Copy `.env.example` to `.env` and set `INPUT_DIR=/app/files`.
3. Start the job:

```bash
docker compose up --build
```

## Testing

```bash
pytest
```
