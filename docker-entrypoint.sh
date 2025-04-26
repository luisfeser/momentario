#!/usr/bin/env bash
set -euxo pipefail

# Require PUID and PGID
: "${PUID:?PUID environment variable is required}"
: "${PGID:?PGID environment variable is required}"

# Create or update group 'users' to match PGID
if getent group users >/dev/null; then
  groupmod -g "${PGID}" users
else
  groupadd -g "${PGID}" users
fi

# Create or update user 'appuser' with dynamic UID/GID
if id appuser >/dev/null 2>&1; then
  usermod -u "${PUID}" --gid "${PGID}" appuser
else
  useradd --uid "${PUID}" --gid "${PGID}" --create-home --shell /usr/sbin/nologin appuser
fi

# Adjust ownership of mounted data directories
chown -R "${PUID}:${PGID}" /data/origen /data/destino /data/videos_originales

# Drop privileges and execute the application
exec gosu appuser "$@"