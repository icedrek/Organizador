#!/usr/bin/env python3
"""Organiza los ficheros de una carpeta en subcarpetas según su tipo.

Uso:
    python organizar_ficheros.py RUTA            # organiza RUTA
    python organizar_ficheros.py RUTA --simular  # solo muestra lo que haría
"""

import argparse
import shutil
from pathlib import Path

CATEGORIAS = {
    "Imágenes": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"},
    "Hojas de cálculo": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentaciones": {".ppt", ".pptx", ".odp"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "Vídeo": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"},
    "Comprimidos": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Código": {".py", ".js", ".html", ".css", ".json", ".xml", ".sql", ".cob", ".cbl"},
    "Instaladores": {".exe", ".msi", ".dmg", ".deb", ".apk"},
}
OTROS = "Otros"


def categoria_de(fichero: Path) -> str:
    ext = fichero.suffix.lower()
    for nombre, extensiones in CATEGORIAS.items():
        if ext in extensiones:
            return nombre
    return OTROS


def destino_libre(destino: Path) -> Path:
    """Si ya existe un fichero con ese nombre, añade un sufijo (1), (2)..."""
    if not destino.exists():
        return destino
    n = 1
    while True:
        candidato = destino.with_name(f"{destino.stem} ({n}){destino.suffix}")
        if not candidato.exists():
            return candidato
        n += 1


def organizar(carpeta: Path, simular: bool = False) -> int:
    movidos = 0
    for fichero in sorted(carpeta.iterdir()):
        if not fichero.is_file() or fichero.name.startswith("."):
            continue
        if fichero.resolve() == Path(__file__).resolve():
            continue  # no mover el propio script

        subcarpeta = carpeta / categoria_de(fichero)
        destino = destino_libre(subcarpeta / fichero.name)

        print(f"{fichero.name}  ->  {subcarpeta.name}/{destino.name}")
        if not simular:
            subcarpeta.mkdir(exist_ok=True)
            shutil.move(str(fichero), str(destino))
        movidos += 1
    return movidos


def main() -> None:
    parser = argparse.ArgumentParser(description="Organiza ficheros por tipo.")
    parser.add_argument("ruta", type=Path, help="Carpeta a organizar")
    parser.add_argument(
        "--simular", action="store_true", help="Muestra los cambios sin mover nada"
    )
    args = parser.parse_args()

    if not args.ruta.is_dir():
        parser.error(f"'{args.ruta}' no es una carpeta válida")

    total = organizar(args.ruta, args.simular)
    accion = "Se moverían" if args.simular else "Movidos"
    print(f"\n{accion} {total} fichero(s).")


if __name__ == "__main__":
    main()
