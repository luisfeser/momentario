#!/bin/sh

# Crear usuario con el UID/GID proporcionado
if [ ! -z "$PUID" ] && [ ! -z "$PGID" ]; then
    groupadd -g $PGID appuser
    useradd -u $PUID -g $PGID -m appuser
    chown -R appuser:appuser /app
    exec su appuser -c "python -m momentario.cli $*"
else
    # Si no se proporciona UID/GID, ejecutar como root (no recomendado)
    exec python -m momentario.cli "$@"
fi
