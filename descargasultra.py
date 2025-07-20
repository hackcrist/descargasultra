 #!/usr/bin/env python3
# By Crist

import sys
import re
import subprocess
import os
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_3d_frame(lines):
    green = Fore.GREEN + Style.BRIGHT
    reset = Style.RESET_ALL
    width = max(len(line) for line in lines) + 4
    shadow_offset = 2

    print(green + "╔" + "═" * (width - 2) + "╗" + reset)
    for line in lines:
        print(green + "║ " + reset + line.ljust(width - 4) + green + " ║" + reset)
    print(green + "╚" + "═" * (width - 2) + "╝" + reset)
    print(" " * shadow_offset + green + "╚" + "═" * (width - 2) + "╝" + reset)

def banner():
    lines = [
        "   ____ ____ ____ ____ ____ ",
        "  ||C |||R |||I |||S |||T ||",
        "  ||__|||__|||__|||__|||__||",
        "  |/__\\|/__\\|/__\\|/__\\|/__\\|",
        "",
        "    Crist-All-Downloader v1.2",
        "",
        "           By Crist"
    ]
    clear_screen()
    print_3d_frame(lines)
    print()

def check_dependencies():
    try:
        subprocess.run(["python", "-m", "yt_dlp", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(Fore.RED + "Error: yt-dlp no está instalado o no está en PATH.")
        print("Instálalo con: pip install yt-dlp")
        sys.exit(1)
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(Fore.RED + "Error: ffmpeg no está instalado o no está en PATH.")
        print("Instálalo según tu sistema operativo.")
        sys.exit(1)

def validar_url(url, plataforma):
    patrones = {
        "YouTube": r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+",
        "TikTok": r"^(https?://)?(www\.)?tiktok\.com/.+",
        "Facebook": r"^(https?://)?(www\.)?facebook\.com/.+",
        "Instagram": r"^(https?://)?(www\.)?instagram\.com/.+"
    }
    patron = patrones.get(plataforma)
    if patron and re.match(patron, url):
        return True
    return False

def pedir_url(tipo, plataforma):
    url = input(Fore.CYAN + f"Ingrese enlace {tipo} {plataforma}: ").strip()
    if not url:
        print(Fore.RED + "❌ No ingresaste ningún enlace. Volviendo al menú...")
        input(Fore.CYAN + "Presiona ENTER para continuar...")
        return None
    if not validar_url(url, plataforma):
        print(Fore.RED + f"❌ URL inválida para {plataforma}.")
        input(Fore.CYAN + "Presiona ENTER para continuar...")
        return None
    return url

def ejecutar_descarga(comando, descripcion):
    print(Fore.YELLOW + descripcion)
    try:
        resultado = subprocess.run(comando, shell=True)
        if resultado.returncode == 0:
            print(Fore.GREEN + "✅ Descarga completada con éxito.\n")
        else:
            print(Fore.RED + "❌ Error en la descarga. Revisa el enlace o tu conexión.\n")
    except Exception as e:
        print(Fore.RED + f"❌ Error inesperado: {e}\n")
    input(Fore.CYAN + "Presiona ENTER para continuar...")

def descargar_youtube(audio=True):
    tipo = "de audio" if audio else "de video"
    url = pedir_url(tipo, "YouTube")
    if url:
        if audio:
            cmd = f'python -m yt_dlp -x --audio-format mp3 "{url}"'
            desc = "Descargando audio YouTube..."
        else:
            cmd = f'python -m yt_dlp -f bestvideo+bestaudio "{url}"'
            desc = "Descargando video YouTube..."
        ejecutar_descarga(cmd, desc)

def descargar_tiktok():
    url = pedir_url("", "TikTok")
    if url:
        ejecutar_descarga(f'python -m yt_dlp "{url}"', "Descargando TikTok...")

def descargar_facebook():
    url = pedir_url("", "Facebook")
    if url:
        ejecutar_descarga(f'python -m yt_dlp "{url}"', "Descargando Facebook...")

def descargar_instagram():
    url = pedir_url("", "Instagram")
    if url:
        ejecutar_descarga(f'python -m yt_dlp "{url}"', "Descargando Instagram...")

def menu():
    check_dependencies()
    while True:
        banner()
        print(Fore.CYAN + "[1] YouTube Audio")
        print(Fore.CYAN + "[2] YouTube Video")
        print(Fore.CYAN + "[3] TikTok")
        print(Fore.CYAN + "[4] Facebook")
        print(Fore.CYAN + "[5] Instagram")
        print(Fore.CYAN + "[0] Salir")
        choice = input(Fore.CYAN + "Opción: ").strip()

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
        elif choice == "0":
            print(Fore.GREEN + "¡Adiós, Crist!")
            sys.exit()
        else:
            print(Fore.RED + "Opción inválida.")
            input(Fore.CYAN + "Presiona ENTER para continuar...")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nInterrumpido por el usuario.")
        sys.exit(0)
