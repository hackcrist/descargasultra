#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

if [ "${PREFIX:-}" = "" ]; then
  PREFIX="/data/data/com.termux/files/usr"
fi

if [ ! -d "$PREFIX/bin" ]; then
  echo "Error: no se encontro PREFIX/bin. Ejecuta esto en Termux." >&2
  exit 1
fi

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="$PREFIX/bin/descarga"

cat > "$TARGET" << EOF
#!/data/data/com.termux/files/usr/bin/bash
set -e

if command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "Error: Python no esta instalado en Termux." >&2
  exit 1
fi

exec "\$PYTHON_BIN" "$REPO_DIR/descargasultra.py" "\$@"
EOF

chmod +x "$TARGET"

echo "Comando global instalado: descarga"
echo "Ya puedes ejecutar: descarga"
