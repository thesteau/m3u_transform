# M3U Playlist Transformer

This program transforms M3U playlist files by replacing specific lines and deleting unwanted lines. It uses the pandas library for data processing and can handle various transformations on M3U playlists.

# Motivation
This project came to be because I wanted to import my iTunes playlist's m3u files to synchonize with my Synology Nas' Audio Station.

## Requirements

- Docker (version >= 19.03)

## Usage

1. Make sure you have Docker installed on your system.

2. Clone this repository to your local machine.

3. Place your `.m3u` files in a folder on your local machine. See the [Settings File](#settings-file) below regarding the settings file.

4. Open a terminal or command prompt and navigate to the cloned repository's directory.

5. Build the Docker image using the following command:

   ```shell
   docker build -t m3u-transformer .
    ```

6. Run the Docker container, specifying the folder path as a volume mount:

    ```bash
    docker run -v /path/to/folder:/app/files m3u-transformer /app/files [settings_file]
    ```

    Replace /path/to/folder with the actual folder path containing the .m3u files you want to process. If you created a settings file, specify the filename as the settings_file argument. Otherwise, it will use the existing settings file in the program. Make sure you update it accordingly!

    Note: Make sure to provide the absolute path to the folder.

7. The program will process all the .m3u files in the specified folder and perform the necessary transformations. The transformed files will be saved with the suffix -u appended to the original file name.

8. Once the program finishes running, you will find the transformed files in the same folder as the original files.

9. If there are any errors during the transformation process, an error log file error_log.txt will be generated, listing the file names and corresponding error messages.

10. If no .m3u files are found in the specified folder, the program will display a message indicating that there are no files to process.

11. You can repeat steps 6-10 whenever you want to process a different folder of .m3u files.

## Transformation Steps

The program performs the following transformations on the M3U playlist file:

1. Lines starting with value from the "initator" are replaced with the value of "replacement".

2. Lines containing the value of "kill_line" are deleted.

Ensure that the input file is a valid M3U playlist file. If the file does not match the expected format, the program will exit and display an appropriate error message.

## File Structure

The folder structure should be as follows:
```graphql
m3u_transform/
  |── README.md
  |── Dockerfile
  |── settings.json
  |── requirements.txt
  |── LICENSE
  |── main.py
  |── src/
  |   ├── __init__.py
  |   └── m3u_transformer.py
  └── tests/
      ├── __init__.py
      └── test_m3u_transform.py
```

## Settings File:

You must include a settings file updated in the root directory or pass it as an optional third argument. No value can be empty.
```json
{
    "initiator": "" ,# string, key to determine replacement, "eg; C:"
    "replacement": "", # string, repalcement key, eg "../../C"
    "kill_line": "", # string, line to remove containing value, eg "#EXT"
    "header": "", # string, Fixed constant header on output, eg "#EXTM3U"
    "replace_file": false, # bool, true to inplace replacement
    "replace_file_value": "", # string, if replace_file is true, eg "-updated"
}
```

## Example
Your iTunes' exported SAMPLE.m3u file contains the following

```
#EXTM3U
#EXTINF:40,song - artist
C:\Music\folder\artist\song.mp3
```

With the sample settings above (Please customize and in accordance to what you see in the export)

After running the program, the expected result should be the following.
SAMPLE-updated.m3u
```
#EXTM3U
../../C/Music/folder/artist/song.mp3
```