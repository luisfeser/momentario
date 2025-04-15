# Momentario

Organizador de fotos y videos que:
- Organiza fotos en estructura de directorios por año/mes basándose en metadatos
- Convierte videos a codec AV1 preservando originales
- Mantiene los nombres originales de los archivos
- Extrae fechas de metadatos o nombres de archivo

## Requisitos previos

1. Instalar dependencias necesarias para pyenv
   ```bash
   sudo apt update
   sudo apt install -y make build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
   libffi-dev liblzma-dev git
   ```

2. Instalar pyenv
   ```bash
   curl https://pyenv.run | bash
   
   # Agregar pyenv al PATH (añadir al final de ~/.bashrc)
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init -)"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Instalar Python 3.12 con pyenv
   ```bash
   pyenv install 3.12.0
   pyenv global 3.12.0
   ```

4. Instalar Poetry con pip
   ```bash
   pip install poetry
   ```

5. FFmpeg con soporte AV1
   ```bash
   sudo apt install ffmpeg
   ```

## Instalación

1. Clonar el repositorio
   ```bash
   git clone https://github.com/usuario/momentario.git
   cd momentario
   ```

2. Configurar el entorno virtual y las dependencias
   ```bash
   # Configurar Poetry para crear el venv en el proyecto
   poetry config virtualenvs.in-project true --local
   
   # Instalar dependencias
   poetry install
   
   # Activar el entorno virtual (dos opciones)
   source $(poetry env info --path)/bin/activate  # Opción 1: activación directa
   # O
   poetry env use python  # Opción 2: usando poetry env
   ```

## Uso

```bash
# Dentro del entorno virtual activado
python -m momentario.cli <carpeta_origen> <carpeta_destino> <carpeta_videos_originales>
```

### Ejemplo

```bash
python -m momentario.cli ~/Descargas/fotos ~/Fotos/organizadas ~/Videos/originales
```

## Uso con Docker

1. Construir la imagen
   ```bash
   docker build -t momentario .
   ```

2. Ejecutar con Docker montando los volúmenes
   ```bash
   docker run --rm \
             -e PUID=$(id -u) \
             -e PGID=$(id -g) \
             -v /ruta/origen:/data/origen \
             -v /ruta/destino:/data/destino \
             -v /ruta/videos_originales:/data/videos_originales \
             momentario
   ```

   Por ejemplo:
   ```bash
   docker run --rm \
             -e PUID=$(id -u) \
             -e PGID=$(id -g) \
             -v ~/Descargas/fotos:/data/origen \
             -v ~/Fotos/organizadas:/data/destino \
             -v ~/Videos/originales:/data/videos_originales \
             momentario
   ```

   Notas:
   - Las variables `PUID` y `PGID` definen el usuario que ejecutará el proceso dentro del contenedor
   - Los archivos creados/movidos tendrán los permisos del usuario especificado
   - La opción `--rm` elimina el contenedor automáticamente al terminar
   - Los archivos se procesan directamente, sin usar almacenamiento temporal
   - Puedes personalizar las rutas modificando los paths antes del `:`
