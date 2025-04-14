# Momentario

Organizador de fotos y videos que:
- Organiza fotos en estructura de directorios por año/mes basándose en metadatos
- Convierte videos a codec AV1 preservando originales
- Mantiene los nombres originales de los archivos
- Extrae fechas de metadatos o nombres de archivo

## Requisitos

- Python 3.12+
- FFmpeg con soporte AV1
- Poetry para gestión de dependencias

## Instalación

```bash
poetry install
```

## Uso

```bash
python -m momentario.cli <carpeta_origen> <carpeta_destino> <carpeta_videos_originales>
```
