FROM python:3.12-slim

# Variables de entorno
ARG PGID=100
ENV PGID=${PGID}

# Instala dependencias del sistema y herramientas necesarias
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry solo para instalar dependencias
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

WORKDIR /app

# Copia solo los archivos de dependencias primero para aprovechar el cache
COPY pyproject.toml poetry.lock ./

# Instala dependencias del proyecto (sin dev)
RUN poetry install --no-interaction --no-ansi --no-root \
    && pip uninstall -y poetry \
    && rm -rf /root/.cache/pip /root/.cache/pypoetry /root/.cache/build /tmp/*

# Copia el código fuente
COPY momentario ./momentario

# Copia el entrypoint
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["/data/origen", "/data/destino", "/data/videos_originales"]
