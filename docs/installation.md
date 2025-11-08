# 📦 Guide d'installation

## Linux

### Installation automatique
```bash
chmod +x install.sh
./install.sh
```

### Installation manuelle
```bash
# 1. Installer les dépendances
sudo apt install python3 python3-pip python3-tk  # Debian/Ubuntu
# OU
sudo dnf install python3 python3-pip python3-tkinter  # Fedora
# OU
sudo pacman -S python python-pip tk  # Arch

# 2. Installer pytube
pip3 install pytube

# 3. Rendre le script exécutable
chmod +x src/youtube_downloader.py

# 4. Lancer l'application
./src/youtube_downloader.py
```

## Windows

1. Installer Python depuis python.org
2. Ouvrir CMD et exécuter:
```cmd
pip install pytube
python src\youtube_downloader.py
```

## macOS
```bash
brew install python-tk
pip3 install pytube
python3 src/youtube_downloader.py
```