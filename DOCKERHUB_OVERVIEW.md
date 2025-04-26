# Overview

**Momentario** is a containerized tool for organizing photos and videos by date and optimizing videos to AV1, while preserving the original files. It is designed for efficient, automated processing of media collections, making it ideal for backups, deduplication, and archival workflows.

## Source Code

The source code for Momentario is available at: [https://github.com/luisfeser/momentario](https://github.com/luisfeser/momentario)

## How it works

- **Photos** are organized into a directory structure by year and month, based on their metadata (EXIF or filename).
- **Videos** are converted to the AV1 codec for efficient storage. The original video is preserved in a separate folder.
- The original file names are maintained.
- The process is robust: only fully converted and validated AV1 videos are accepted.

## Example Resulting Filesystem

After running Momentario, your directories will look like:

```
.
|-- output
|   |-- 2022
|   |   |-- 06
|   |   |   `-- IMG_20220611_161328.jpg
|   |   |-- 08
|   |   |   |-- IMG_20220814_123022.jpg
|   |   |   |-- IMG_20220814_123038.jpg
|   |   |   |-- IMG_20220814_143000.jpg
|   |   |   `-- IMG_20220814_143022_1.jpg
|   |   `-- 11
|   |       |-- IMG_20221128_162849.jpg
|   |       |-- IMG_20221128_162931.jpg
|   |       `-- IMG_20221128_163015.jpg
|   `-- 2024
|       `-- 06
|           |-- IMG_20170825_195317.jpg
|           |-- PXL_20240607_185952040_AV1.mp4  # The optimized video
|-- input  # input is empty after processing
`-- videos-originales
    `-- PXL_20240607_185952040.mp4  # The original video
```

- All processed photos and optimized videos are in `output`, organized by year/month.
- The original (unconverted) videos are moved to `videos-originales`.
- The `input` directory will be empty after processing.

## Usage

Mount your media directories as Docker volumes. For example:

```bash
docker run --rm \
  -e PUID=$(id -u) \
  -e PGID=$(getent group users | cut -d: -f3) \
  -v /path/to/input:/data/origen \
  -v /path/to/output:/data/destino \
  -v /path/to/videos-originales:/data/videos_originales \
  momentario
```

## Permissions and the `users` group

**Important:**  
The container runs as a non-root user (with the group `users`).  
To ensure the container can write to the mounted folders, you must:

- Set the group of all mounted directories to `users` on your host system.
- Grant group write permissions.

For example, on Linux:

```bash
sudo chown -R :users /path/to/input /path/to/output /path/to/videos-originales
sudo chmod -R 775 /path/to/input /path/to/output /path/to/videos-originales
```

This ensures all files created or moved by the container are accessible and modifiable by the `users` group, preventing permission issues.

---

