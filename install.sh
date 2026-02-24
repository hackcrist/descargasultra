#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

if ! command -v pkg >/dev/null 2>&1; then
  echo "Error: this installer is for Termux (pkg command not found)." >&2
  exit 1
fi

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

echo "[1/5] Updating Termux packages..."
pkg update -y
pkg upgrade -y

echo "[2/5] Installing system dependencies..."
pkg install -y python git ffmpeg

echo "[3/5] Installing Python dependencies..."
if command -v pip >/dev/null 2>&1; then
  pip install -r requirements.txt
else
  python -m pip install -r requirements.txt
fi

echo "[4/5] Installing global command..."
PREFIX_DIR="${PREFIX:-/data/data/com.termux/files/usr}"
TARGET="$PREFIX_DIR/bin/descarga"

cat > "$TARGET" << EOF
#!/data/data/com.termux/files/usr/bin/bash
set -e
exec python "$REPO_DIR/descargasultra.py" "\$@"
EOF

chmod +x "$TARGET"

echo "[5/5] Verifying installation..."
if command -v descarga >/dev/null 2>&1; then
  echo "Installation completed successfully."
  echo "Run: descarga"
else
  echo "Error: failed to register 'descarga' command." >&2
  exit 1
fi
