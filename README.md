# DESCARGAS ULTRA

Descargas Ultra is a command-line tool to download audio or video from YouTube, TikTok, Facebook, and Instagram in a simple and organized way.

## Features

- Interactive terminal menu.
- YouTube download support (MP3 audio or video).
- TikTok, Facebook, and Instagram downloads.
- Platform-specific URL validation.
- URL testing without downloading.
- Output folders by platform in `~/DescargasUltra/`.
- Optional Hacker Mode to show the technical command being executed.
- Clear status and error messages.

## Current Menu

```text
[1] YouTube Audio
[2] YouTube Video
[3] TikTok
[4] Facebook
[5] Instagram
[6] Toggle Hacker Mode
[7] Test URL (without downloading)
[0] Exit
```

## Requirements (Termux)

- Python 3.8+
- yt-dlp
- colorama
- ffmpeg (required for MP3 audio conversion)

### Requirement Installation Commands (Termux)

```bash
pkg update && pkg upgrade -y
pkg install -y python ffmpeg
pip install --upgrade pip
pip install yt-dlp colorama
```

## Installation on Termux

```bash
pkg update && pkg upgrade -y
pkg install -y git

git clone https://github.com/hackcrist/descargasultra.git
cd descargasultra
chmod +x install.sh install_termux_command.sh
bash install.sh
```

## Usage on Termux

```bash
# From any folder
descarga
```

## How to Use the `descarga` Command

Once installed, you can run it from any folder with:

```bash
descarga
```

Quick usage flow:

1. Run `descarga`.
2. Choose an option from the menu.
3. Paste the URL when prompted.
4. Wait for the download and check `~/DescargasUltra/<Platform>/`.

Tip: use option `7` first to validate links before downloading.

## Output Structure

Downloads are saved to:

- `~/DescargasUltra/YouTube/`
- `~/DescargasUltra/TikTok/`
- `~/DescargasUltra/Facebook/`
- `~/DescargasUltra/Instagram/`

Output filename format:

```text
%(title).120B [%(id)s].%(ext)s
```

## Security and Stability

- Subprocess execution without `shell=True`.
- Local/private host blocking in URL validation.
- Download retries and continuation enabled.
- Prevents overwriting existing files.

## License

This project is licensed under Apache License 2.0.
See `LICENSE` and `NOTICE` for details.

## Author

Crist

## Responsible Use

Use this tool ethically and legally, respecting each platform's terms and policies.

