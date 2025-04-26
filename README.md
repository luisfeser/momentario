# Momentario

Photo and Video Organizer that:
- Organizes photos into a year/month directory structure based on metadata
- Converts videos to AV1 codec while preserving originals
- Keeps the original file names
- Extracts dates from metadata or file names

## Prerequisites

1. Install dependencies required for pyenv
   ```bash
   sudo apt update
   sudo apt install -y make build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
   libffi-dev liblzma-dev git
   ```

2. Install pyenv
   ```bash
   curl https://pyenv.run | bash
   
   # Add pyenv to PATH (append to ~/.bashrc)
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo 'eval "$(pyenv init -)"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Install Python 3.12 with pyenv
   ```bash
   pyenv install 3.12.0
   pyenv global 3.12.0
   ```

4. Install Poetry with pip
   ```bash
   pip install poetry
   ```

5. Install FFmpeg with AV1 support
   ```bash
   sudo apt install ffmpeg
   ```

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/usuario/momentario.git
   cd momentario
   ```

2. Configure the virtual environment and dependencies
   ```bash
   # Configure Poetry to create the venv in the project
   poetry config virtualenvs.in-project true --local
   
   # Install dependencies
   poetry install
   
   # Activate the virtual environment (two options)
   source $(poetry env info --path)/bin/activate  # Option 1: direct activation
   # Or
   poetry env use python  # Option 2: using poetry env
   ```

## Usage

```bash
# Inside the activated virtual environment
python -m momentario.cli <source_directory> <destination_directory> <original_videos_directory>
```

### Example

```bash
python -m momentario.cli ~/Downloads/photos ~/Photos/organized ~/Videos/originals
```

## Docker Usage

1. Build the image
   ```bash
   docker build -t momentario .
   ```

2. Run with Docker mounting volumes
   ```bash
   docker run --rm \
             -e PUID=$(id -u) \
             -e PGID=$(getent group users | cut -d: -f3) \
             -v /ruta/origen:/data/origen \
             -v /ruta/destino:/data/destino \
             -v /ruta/videos_originales:/data/videos_originales \
             momentario
   ```

   Example:
   ```bash
   docker run --rm \
             -e PUID=$(id -u) \
             -e PGID=$(getent group users | cut -d: -f3) \
             -v ~/Downloads/photos:/data/origen \
             -v ~/Photos/organized:/data/destino \
             -v ~/Videos/originals:/data/videos_originales \
             momentario
   ```

   > **Important:**
   > The mounted directories must be writable by the `users` group inside the container. If you are using Linux, you can ensure this by running on the host:
   >
   > ```bash
   > sudo chown -R :users /path/to/source /path/to/destination /path/to/original_videos
   > sudo chmod -R 775 /path/to/source /path/to/destination /path/to/original_videos
   > ```
   >
   > This ensures that the container can write and modify files correctly using the `users` group.

   Notes:
   - The `PUID` and `PGID` variables define the user and group that will run the process inside the container (by default `users`)
   - Files created/moved will have the permissions of the specified user/group
   - The `--rm` option automatically removes the container when finished
   - Files are processed directly, without using temporary storage
   - You can customize the paths by changing the values before the `:`
