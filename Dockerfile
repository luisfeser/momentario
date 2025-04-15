FROM python:3.12-slim

# Instalar dependencias del sistema y FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la aplicación
WORKDIR /app

# Instalar poetry
RUN pip install poetry

# Copiar código fuente y archivos de configuración
COPY pyproject.toml poetry.lock ./
COPY momentario ./momentario

# Eliminar carpeta de pruebas si existe
RUN rm -rf ./momentario/pruebas

# Configurar poetry para no crear entorno virtual en Docker
RUN poetry config virtualenvs.create false

# Instalar dependencias (solo principales, sin dev)
RUN poetry install --only main --no-interaction --no-ansi --no-root

# Copiar y configurar el script de entrada
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Comando por defecto
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["/data/origen", "/data/destino", "/data/videos_originales"]
