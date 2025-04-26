# Dockerfile
FROM python:3.12-slim

# Build-time argument for host group ID (users)
ARG PGID=100
ENV PGID=${PGID}

# Install system dependencies, bash and gosu for privilege dropping
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg bash gosu \
    && rm -rf /var/lib/apt/lists/*

# Ensure group 'users' exists with the specified GID
RUN if ! getent group users >/dev/null; then \
      groupadd -g "${PGID}" users; \
    fi

# Set working directory
WORKDIR /app

# Copy project files and install Python dependencies (including the project)
COPY pyproject.toml poetry.lock ./
COPY momentario ./momentario
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pip uninstall -y poetry \
    && rm -rf ~/.cache/pypoetry

# Copy and make entrypoint executable
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Keep root user to adjust permissions at runtime
USER root

# Entrypoint and default command
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["python3", "-m", "momentario.cli", "/data/origen", "/data/destino", "/data/videos_originales"]