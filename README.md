# DESCARGAS ULTRA

Descargas Ultra es una herramienta de linea de comandos para descargar audio o video desde YouTube, TikTok, Facebook e Instagram de forma simple y ordenada.

## Caracteristicas

- Menu interactivo en terminal.
- Descarga de YouTube (audio MP3 o video).
- Descarga de TikTok, Facebook e Instagram.
- Validacion de URL por plataforma.
- Prueba de URL sin descargar para validar enlaces.
- Directorios de salida por plataforma en `~/DescargasUltra/`.
- Modo Hacker opcional para ver el comando tecnico ejecutado.
- Mensajes claros de estado y errores.

## Menu actual

```text
[1] YouTube Audio
[2] YouTube Video
[3] TikTok
[4] Facebook
[5] Instagram
[6] Toggle Modo Hacker
[7] Probar URL (sin descargar)
[0] Salir
```

## Requisitos (Termux)

- Python 3.8+
- yt-dlp
- colorama
- ffmpeg (requerido para conversion de audio MP3)

### Comandos de instalacion de requisitos (Termux)

```bash
pkg update && pkg upgrade -y
pkg install -y python ffmpeg
pip install --upgrade pip
pip install yt-dlp colorama
```

## Instalacion en Termux

```bash
pkg update && pkg upgrade -y
pkg install -y git

git clone https://github.com/hackcrist/descargasultra.git
cd descargasultra
bash install.sh
```

## Uso en Termux

```bash
# Desde cualquier carpeta
descarga
```

## Como usar el comando `descarga`

Una vez instalado, puedes ejecutarlo desde cualquier carpeta con:

```bash
descarga
```

Flujo rapido de uso:

1. Ejecuta `descarga`.
2. Elige una opcion del menu.
3. Pega la URL cuando el programa la pida.
4. Espera la descarga y revisa la carpeta `~/DescargasUltra/<Plataforma>/`.

Tip: usa primero la opcion `7` para validar enlaces antes de descargar.

## Estructura de salida

Las descargas se guardan en:

- `~/DescargasUltra/YouTube/`
- `~/DescargasUltra/TikTok/`
- `~/DescargasUltra/Facebook/`
- `~/DescargasUltra/Instagram/`

Formato de archivo de salida:

```text
%(title).120B [%(id)s].%(ext)s
```

## Seguridad y estabilidad

- Ejecucion de subprocess sin `shell=True`.
- Bloqueo de hosts locales/privados en validacion de URL.
- Reintentos y continuidad de descarga configurados.
- Evita sobreescritura de archivos existentes.

## Licencia

Este proyecto esta licenciado bajo Apache License 2.0.
Consulta `LICENSE` y `NOTICE` para mas detalles.

## Autor

Crist

## Uso responsable

Usa esta herramienta de forma etica y legal, respetando los terminos y politicas de cada plataforma.
