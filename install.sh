#!/bin/bash
#
# Script d'installation automatique pour YouTube Downloader Pro
# Compatible: Debian/Ubuntu, Fedora/RHEL, Arch Linux
# Auto-contenu et robuste
#

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher des messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Bannière
echo -e "${RED}"
cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║    YouTube Downloader Pro - Installation Script      ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Détection de la distribution
print_info "Détection de la distribution Linux..."

if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    print_success "Distribution détectée: $PRETTY_NAME"
else
    print_error "Impossible de détecter la distribution"
    exit 1
fi

# Installation des dépendances selon la distribution
print_info "Installation des dépendances système..."

case "$OS" in
    ubuntu|debian|linuxmint|pop)
        print_info "Installation avec APT..."
        # Ignorer les erreurs de apt update (dépôts tiers cassés)
        sudo apt update 2>&1 | grep -v "spotify\|torproject" || true
        
        if sudo apt install -y python3 python3-pip python3-tk 2>&1 | grep -v "spotify\|torproject"; then
            print_success "Dépendances système installées"
        else
            print_warning "Certaines dépendances existent déjà"
        fi
        ;;
    
    fedora|rhel|centos)
        print_info "Installation avec DNF..."
        sudo dnf install -y python3 python3-pip python3-tkinter
        print_success "Dépendances système installées"
        ;;
    
    arch|manjaro)
        print_info "Installation avec Pacman..."
        sudo pacman -Sy --noconfirm python python-pip tk
        print_success "Dépendances système installées"
        ;;
    
    *)
        print_warning "Distribution non reconnue, tentative d'installation générique..."
        if command -v apt &> /dev/null; then
            sudo apt update 2>&1 | grep -v "spotify\|torproject" || true
            sudo apt install -y python3 python3-pip python3-tk 2>&1 | grep -v "spotify\|torproject" || true
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip python3-tkinter
        elif command -v pacman &> /dev/null; then
            sudo pacman -Sy --noconfirm python python-pip tk
        else
            print_error "Gestionnaire de paquets non supporté"
            exit 1
        fi
        print_success "Dépendances système installées"
        ;;
esac

# Installation de pytubefix (plus stable que pytube)
print_info "Installation de pytubefix (bibliothèque YouTube)..."

# Essayer différentes méthodes d'installation selon l'environnement Python
install_pytubefix() {
    # Méthode 1: Installation avec --user (préféré)
    if pip3 install --user pytubefix --upgrade 2>/dev/null; then
        return 0
    fi
    
    # Méthode 2: --break-system-packages (Ubuntu 24.04+)
    if pip3 install --break-system-packages pytubefix --upgrade 2>/dev/null; then
        return 0
    fi
    
    # Méthode 3: Installation standard (anciennes versions)
    if pip3 install pytubefix --upgrade 2>/dev/null; then
        return 0
    fi
    
    # Méthode 4: Avec sudo (dernier recours)
    if sudo pip3 install pytubefix --upgrade 2>/dev/null; then
        return 0
    fi
    
    return 1
}

if install_pytubefix; then
    print_success "pytubefix installé avec succès"
else
    print_error "Impossible d'installer pytubefix"
    print_info "Essayez manuellement: pip3 install --break-system-packages pytubefix"
    exit 1
fi

# Déterminer le chemin d'installation
INSTALL_DIR="$HOME/.local/share/youtube-downloader"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons"

# Créer les dossiers nécessaires
print_info "Création des dossiers d'installation..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Vérifier la structure du projet
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/src/youtube_downloader.py" ]; then
    PYTHON_SCRIPT="$SCRIPT_DIR/src/youtube_downloader.py"
elif [ -f "$SCRIPT_DIR/youtube_downloader.py" ]; then
    PYTHON_SCRIPT="$SCRIPT_DIR/youtube_downloader.py"
else
    print_error "Le fichier youtube_downloader.py n'a pas été trouvé!"
    print_info "Structure attendue: src/youtube_downloader.py ou ./youtube_downloader.py"
    exit 1
fi

# Modifier le script Python pour utiliser pytubefix au lieu de pytube
print_info "Adaptation du script pour pytubefix..."
sed 's/from pytube import/from pytubefix import/g' "$PYTHON_SCRIPT" > "$INSTALL_DIR/youtube_downloader.py"
chmod +x "$INSTALL_DIR/youtube_downloader.py"
print_success "Script adapté et copié"

# Créer un lien symbolique dans ~/.local/bin
ln -sf "$INSTALL_DIR/youtube_downloader.py" "$BIN_DIR/youtube-downloader"
print_success "Lien symbolique créé"

# Créer une icône SVG simple
print_info "Installation de l'icône..."

# Vérifier si l'icône existe dans assets/
if [ -f "$SCRIPT_DIR/assets/icon.svg" ]; then
    print_info "Utilisation de l'icône depuis assets/icon.svg"
    cp "$SCRIPT_DIR/assets/icon.svg" "$ICON_DIR/youtube-downloader.svg"
    ICON_PATH="$ICON_DIR/youtube-downloader.svg"
elif [ -f "$SCRIPT_DIR/assets/icon.png" ]; then
    print_info "Utilisation de l'icône depuis assets/icon.png"
    cp "$SCRIPT_DIR/assets/icon.png" "$ICON_DIR/youtube-downloader.png"
    ICON_PATH="$ICON_DIR/youtube-downloader.png"
else
    # Créer une icône SVG par défaut si aucune n'existe
    print_warning "Aucune icône trouvée dans assets/, création d'une icône par défaut..."
    cat > "$ICON_DIR/youtube-downloader.svg" << 'SVGEOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="128" height="128" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#dc2626;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#b91c1c;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="24" fill="url(#bg)"/>
  <path d="M 45 35 L 45 93 L 90 64 Z" fill="white" opacity="0.95"/>
  <g transform="translate(64, 45)">
    <line x1="0" y1="0" x2="0" y2="35" stroke="white" stroke-width="6" stroke-linecap="round"/>
    <path d="M -12 28 L 0 40 L 12 28" stroke="white" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  </g>
  <rect x="20" y="100" width="88" height="8" rx="4" fill="white" opacity="0.9"/>
  <rect x="20" y="100" width="60" height="8" rx="4" fill="#22c55e" opacity="0.9"/>
</svg>
SVGEOF
    ICON_PATH="$ICON_DIR/youtube-downloader.svg"
fi

print_success "Icône installée"

# Créer le fichier .desktop
print_info "Création du lanceur d'application..."
cat > "$DESKTOP_DIR/youtube-downloader.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=YouTube Downloader Pro
Comment=Télécharger des vidéos et audios depuis YouTube
Exec=$INSTALL_DIR/youtube_downloader.py
Icon=$ICON_PATH
Terminal=false
Categories=AudioVideo;Video;Network;
Keywords=youtube;download;video;audio;
StartupNotify=true
EOF

chmod +x "$DESKTOP_DIR/youtube-downloader.desktop"
print_success "Lanceur créé"

# Mettre à jour le cache des applications
if command -v update-desktop-database &> /dev/null; then
    print_info "Mise à jour du cache des applications..."
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# Vérifier si ~/.local/bin est dans le PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    print_warning "~/.local/bin n'est pas dans votre PATH"
    print_info "Ajout de ~/.local/bin au PATH..."
    
    # Déterminer le fichier de configuration du shell
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    # Ajouter au PATH si pas déjà présent
    if [ -f "$SHELL_RC" ] && ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC"; then
        echo '' >> "$SHELL_RC"
        echo '# Ajouté par YouTube Downloader installer' >> "$SHELL_RC"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        print_success "PATH mis à jour dans $SHELL_RC"
        print_warning "Redémarrez votre terminal ou exécutez: source $SHELL_RC"
    fi
fi

# Créer un script de désinstallation
print_info "Création du script de désinstallation..."
cat > "$INSTALL_DIR/uninstall.sh" << 'UNINSTALLEOF'
#!/bin/bash
echo "Désinstallation de YouTube Downloader Pro..."
rm -rf "$HOME/.local/share/youtube-downloader"
rm -f "$HOME/.local/bin/youtube-downloader"
rm -f "$HOME/.local/share/applications/youtube-downloader.desktop"
rm -f "$HOME/.local/share/icons/youtube-downloader.svg"
rm -f "$HOME/.local/share/icons/youtube-downloader.png"
pip3 uninstall -y pytubefix 2>/dev/null || pip3 uninstall --break-system-packages -y pytubefix 2>/dev/null || true
echo "✓ Désinstallation terminée!"
UNINSTALLEOF
chmod +x "$INSTALL_DIR/uninstall.sh"

# Créer un wrapper script pour gérer l'environnement Python
print_info "Création du script wrapper..."
cat > "$INSTALL_DIR/youtube_downloader_wrapper.sh" << 'WRAPPEREOF'
#!/bin/bash
# Wrapper pour gérer les différentes configurations Python

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Essayer d'exécuter le script Python
if python3 "$SCRIPT_DIR/youtube_downloader.py" "$@" 2>/dev/null; then
    exit 0
fi

# Si échec, vérifier et installer pytubefix si nécessaire
echo "Vérification de pytubefix..."
if ! python3 -c "import pytubefix" 2>/dev/null; then
    echo "Installation de pytubefix..."
    pip3 install --break-system-packages pytubefix 2>/dev/null || \
    pip3 install --user pytubefix 2>/dev/null || \
    pip3 install pytubefix 2>/dev/null
fi

# Réessayer
python3 "$SCRIPT_DIR/youtube_downloader.py" "$@"
WRAPPEREOF
chmod +x "$INSTALL_DIR/youtube_downloader_wrapper.sh"

# Résumé de l'installation
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗"
echo -e "║                                                       ║"
echo -e "║          ✓ Installation terminée avec succès!        ║"
echo -e "║                                                       ║"
echo -e "╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
print_info "Comment lancer l'application:"
echo ""
echo "  1. Depuis le menu d'applications:"
echo -e "     ${BLUE}Cherchez 'YouTube Downloader Pro'${NC}"
echo ""
echo "  2. Depuis le terminal:"
echo -e "     ${BLUE}youtube-downloader${NC}"
echo ""
echo "  3. Depuis le chemin complet:"
echo -e "     ${BLUE}$INSTALL_DIR/youtube_downloader.py${NC}"
echo ""
print_info "Pour désinstaller:"
echo -e "     ${BLUE}$INSTALL_DIR/uninstall.sh${NC}"
echo ""
print_success "Profitez bien de YouTube Downloader Pro! 🎬"
echo ""
print_warning "Note: pytubefix est utilisé (plus stable que pytube)"
echo ""