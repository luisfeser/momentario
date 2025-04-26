#!/bin/sh
set -eu

# Variables obligatorias
: "${PUID:?PUID environment variable is required}"
: "${PGID:?PGID environment variable is required}"

# Asegura que el grupo 'users' existe con el PGID correcto
if getent group users >/dev/null; then
  groupmod -g "${PGID}" users
else
  groupadd -g "${PGID}" users
fi

# Asegura que el usuario 'appuser' existe con PUID/PGID
if id appuser >/dev/null 2>&1; then
  usermod -u "${PUID}" -g "${PGID}" appuser
else
  useradd -u "${PUID}" -g "${PGID}" -M -s /usr/sbin/nologin appuser
fi

# Cambia dueño de los directorios montados
chown -R "${PUID}:${PGID}" /data/origen /data/destino /data/videos_originales

# Ejecuta la app como 'appuser'
exec gosu appuser python3 -m momentario.cli "$@"
