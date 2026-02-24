#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

if ! command -v pkg >/dev/null 2>&1; then
  echo "Error: este instalador es para Termux (comando pkg no encontrado)." >&2
  exit 1
fi

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

echo "[1/5] Actualizando paquetes de Termux..."
pkg update -y
pkg upgrade -y

echo "[2/5] Instalando dependencias del sistema..."
pkg install -y python git ffmpeg

echo "[3/5] Instalando dependencias Python..."
if command -v pip >/dev/null 2>&1; then
  pip install --upgrade pip
  pip install -r requirements.txt
else
  python -m ensurepip --upgrade
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
fi

echo "[4/5] Instalando comando global..."
bash "$REPO_DIR/install_termux_command.sh"

echo "[5/5] Verificando instalacion..."
if command -v descarga >/dev/null 2>&1; then
  echo "Instalacion completada correctamente."
  echo "Ejecuta: descarga"
else
  echo "Error: no se pudo registrar el comando 'descarga'." >&2
  exit 1
fi
