#!/usr/bin/env python3
# By Crist

import ipaddress
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from colorama import Fore, Style, init

init(autoreset=True)

HACKER_MODE = False


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_frame(lines):
    green = Fore.GREEN + Style.BRIGHT
    reset = Style.RESET_ALL
    width = max(len(line) for line in lines) + 4

    print(green + "+" + "-" * (width - 2) + "+" + reset)
    for line in lines:
        print(green + "| " + reset + line.ljust(width - 4) + green + " |" + reset)
    print(green + "+" + "-" * (width - 2) + "+" + reset)


def mode_label():
    return "ACTIVO" if HACKER_MODE else "INACTIVO"


def banner():
    lines = [
        "   ____ ____ ____ ____ ____ ",
        "  ||C |||R |||I |||S |||T ||",
        "  ||__|||__|||__|||__|||__||",
        "  |/__\\|/__\\|/__\\|/__\\|/__\\|",
        "",
        "    Crist-All-Downloader v1.5",
        "",
        "           By Crist",
        f"      Modo Hacker: {mode_label()}",
    ]
    clear_screen()
    print_frame(lines)
    print()


def command_available(command):
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_dependencies(require_ffmpeg=False):
    if not command_available([sys.executable, "-m", "yt_dlp", "--version"]):
        print(Fore.RED + "Error: yt-dlp no esta instalado o no esta disponible.")
        print("Instalalo con: pip install -r requirements.txt")
        sys.exit(1)

    if require_ffmpeg and not command_available(["ffmpeg", "-version"]):
        print(Fore.RED + "Error: ffmpeg no esta instalado o no esta en PATH.")
        print("Instalalo segun tu sistema operativo.")
        sys.exit(1)


def host_bloqueado(host):
    host_lower = host.lower()
    if host_lower in {"localhost", "127.0.0.1", "::1"}:
        return True

    try:
        ip = ipaddress.ip_address(host_lower)
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            return True
    except ValueError:
        pass

    return False


def validar_url(url, plataforma):
    plataformas = {
        "YouTube": {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"},
        "TikTok": {"tiktok.com", "www.tiktok.com", "m.tiktok.com"},
        "Facebook": {"facebook.com", "www.facebook.com", "m.facebook.com", "fb.watch"},
        "Instagram": {"instagram.com", "www.instagram.com", "m.instagram.com"},
    }

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if parsed.scheme not in {"http", "https"}:
        return False

    if not parsed.netloc:
        return False

    host = parsed.netloc.lower().split(":")[0]

    if host_bloqueado(host):
        return False

    if parsed.username or parsed.password:
        return False

    valid_hosts = plataformas.get(plataforma, set())
    if host in valid_hosts:
        return True

    if plataforma == "YouTube" and re.search(r"(^|\.)youtube\.com$", host):
        return True

    return False


def pedir_url(tipo, plataforma):
    texto_tipo = f" {tipo}" if tipo else ""
    url = input(Fore.CYAN + f"Ingrese enlace{texto_tipo} {plataforma}: ").strip()

    if not url:
        print(Fore.RED + "No ingresaste ningun enlace. Volviendo al menu...")
        input(Fore.CYAN + "Presiona ENTER para continuar...")
        return None

    if len(url) > 2048:
        print(Fore.RED + "URL demasiado larga. Revisa el enlace.")
        input(Fore.CYAN + "Presiona ENTER para continuar...")
        return None

    if not validar_url(url, plataforma):
        print(Fore.RED + f"URL invalida para {plataforma}.")
        input(Fore.CYAN + "Presiona ENTER para continuar...")
        return None

    return url


def output_dir_for(platform):
    base = Path.home() / "DescargasUltra"
    folder_map = {
        "YouTube": "YouTube",
        "TikTok": "TikTok",
        "Facebook": "Facebook",
        "Instagram": "Instagram",
    }

    out_dir = base / folder_map.get(platform, "Otros")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(Fore.RED + f"No se pudo crear directorio de salida: {exc}")
        input(Fore.CYAN + "Presiona ENTER para continuar...")
        return None

    return out_dir


def ejecutar_descarga(args, descripcion, plataforma):
    out_dir = output_dir_for(plataforma)
    if out_dir is None:
        return

    output_template = str(out_dir / "%(title).120B [%(id)s].%(ext)s")

    common_flags = [
        "--restrict-filenames",
        "--no-playlist",
        "--continue",
        "--no-overwrites",
        "--retries",
        "10",
        "--fragment-retries",
        "10",
        "--trim-filenames",
        "120",
        "-o",
        output_template,
    ]

    full_cmd = args + common_flags

    print(Fore.YELLOW + descripcion)
    print(Fore.CYAN + f"Destino: {out_dir}")

    if HACKER_MODE:
        print(Fore.GREEN + "Comando ejecutado:")
        print(" ".join(full_cmd))

    try:
        resultado = subprocess.run(full_cmd)
        if resultado.returncode == 0:
            print(Fore.GREEN + "Descarga completada con exito.\n")
        else:
            print(Fore.RED + f"Error en la descarga (codigo {resultado.returncode}).\n")
    except KeyboardInterrupt:
        print(Fore.RED + "\nDescarga interrumpida por el usuario.\n")
    except Exception as exc:
        print(Fore.RED + f"Error inesperado: {exc}\n")

    input(Fore.CYAN + "Presiona ENTER para continuar...")


def elegir_plataforma_para_prueba():
    print(Fore.CYAN + "Selecciona plataforma para probar URL:")
    print(Fore.CYAN + "[1] YouTube")
    print(Fore.CYAN + "[2] TikTok")
    print(Fore.CYAN + "[3] Facebook")
    print(Fore.CYAN + "[4] Instagram")
    opcion = input(Fore.CYAN + "Opcion: ").strip()

    plataformas = {
        "1": "YouTube",
        "2": "TikTok",
        "3": "Facebook",
        "4": "Instagram",
    }
    return plataformas.get(opcion)


def probar_url():
    plataforma = elegir_plataforma_para_prueba()
    if not plataforma:
        print(Fore.RED + "Plataforma invalida.")
        input(Fore.CYAN + "Presiona ENTER para continuar...")
        return

    url = pedir_url("de prueba", plataforma)
    if not url:
        return

    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--skip-download",
        "--no-playlist",
        "--print",
        "title:%(title)s",
        "--print",
        "uploader:%(uploader)s",
        "--print",
        "duration:%(duration_string)s",
        url,
    ]

    print(Fore.YELLOW + "Probando URL sin descargar...")
    if HACKER_MODE:
        print(Fore.GREEN + "Comando ejecutado:")
        print(" ".join(cmd))

    try:
        resultado = subprocess.run(cmd, text=True, capture_output=True)
        if resultado.returncode == 0:
            print(Fore.GREEN + "URL valida y accesible.")
            salida = (resultado.stdout or "").strip()
            if salida:
                print(Fore.CYAN + "Metadatos:")
                print(salida)
        else:
            print(Fore.RED + f"No se pudo validar la URL (codigo {resultado.returncode}).")
            detalle = (resultado.stderr or resultado.stdout or "").strip()
            if detalle:
                print(Fore.RED + "Detalle:")
                print(detalle)
    except Exception as exc:
        print(Fore.RED + f"Error al probar URL: {exc}")

    input(Fore.CYAN + "Presiona ENTER para continuar...")


def descargar_youtube(audio=True):
    tipo = "de audio" if audio else "de video"
    url = pedir_url(tipo, "YouTube")
    if not url:
        return

    if audio:
        check_dependencies(require_ffmpeg=True)
        args = [
            sys.executable,
            "-m",
            "yt_dlp",
            "-x",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "0",
            url,
        ]
        desc = "Descargando audio YouTube..."
    else:
        args = [
            sys.executable,
            "-m",
            "yt_dlp",
            "-f",
            "bv*+ba/b",
            url,
        ]
        desc = "Descargando video YouTube..."

    ejecutar_descarga(args, desc, "YouTube")


def descargar_tiktok():
    url = pedir_url("", "TikTok")
    if url:
        ejecutar_descarga([sys.executable, "-m", "yt_dlp", url], "Descargando TikTok...", "TikTok")


def descargar_facebook():
    url = pedir_url("", "Facebook")
    if url:
        ejecutar_descarga([sys.executable, "-m", "yt_dlp", url], "Descargando Facebook...", "Facebook")


def descargar_instagram():
    url = pedir_url("", "Instagram")
    if url:
        ejecutar_descarga(
            [sys.executable, "-m", "yt_dlp", url],
            "Descargando Instagram...",
            "Instagram",
        )


def toggle_hacker_mode():
    global HACKER_MODE
    HACKER_MODE = not HACKER_MODE
    estado = mode_label()
    print(Fore.GREEN + f"Modo Hacker ahora: {estado}")
    input(Fore.CYAN + "Presiona ENTER para continuar...")


def menu():
    check_dependencies(require_ffmpeg=False)

    while True:
        banner()
        print(Fore.CYAN + "[1] YouTube Audio")
        print(Fore.CYAN + "[2] YouTube Video")
        print(Fore.CYAN + "[3] TikTok")
        print(Fore.CYAN + "[4] Facebook")
        print(Fore.CYAN + "[5] Instagram")
        print(Fore.CYAN + "[6] Toggle Modo Hacker")
        print(Fore.CYAN + "[7] Probar URL (sin descargar)")
        print(Fore.CYAN + "[0] Salir")
        choice = input(Fore.CYAN + "Opcion: ").strip()

        if choice == "1":
            clear_screen()
            banner()
            descargar_youtube(audio=True)
        elif choice == "2":
            clear_screen()
            banner()
            descargar_youtube(audio=False)
        elif choice == "3":
            clear_screen()
            banner()
            descargar_tiktok()
        elif choice == "4":
            clear_screen()
            banner()
            descargar_facebook()
        elif choice == "5":
            clear_screen()
            banner()
            descargar_instagram()
        elif choice == "6":
            toggle_hacker_mode()
        elif choice == "7":
            clear_screen()
            banner()
            probar_url()
        elif choice == "0":
            print(Fore.GREEN + "Adios, Crist!")
            sys.exit(0)
        else:
            print(Fore.RED + "Opcion invalida.")
            input(Fore.CYAN + "Presiona ENTER para continuar...")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nInterrumpido por el usuario.")
        sys.exit(0)
