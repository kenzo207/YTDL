# 🔧 Résolution de problèmes

## 🐛 Problèmes courants et solutions

### ❌ Erreur : "pytube module not found"

**Cause** : La bibliothèque pytube n'est pas installée.

**Solution** :
```bash
pip3 install pytube
# ou
pip3 install --user pytube
```

---

### ❌ Erreur : "No module named 'tkinter'"

**Cause** : Tkinter n'est pas installé.

**Solution selon la distribution** :
```bash
# Debian/Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

---

### ❌ Erreur : "HTTP Error 403: Forbidden"

**Cause** : YouTube a bloqué la requête ou pytube est obsolète.

**Solution** :
```bash
# Mettre à jour pytube
pip3 install --upgrade pytube
```

---

### ❌ Erreur : "Video unavailable"

**Causes possibles** :
- Vidéo privée ou supprimée
- Restriction géographique
- Âge limité

**Solution** :
- Vérifier que la vidéo est publique sur YouTube
- Essayer avec une autre vidéo

---

### ❌ L'application ne se lance pas

**Vérifications** :

1. **Python est-il installé ?**
```bash
python3 --version
# Doit afficher 3.8 ou supérieur
```

2. **Le script est-il exécutable ?**
```bash
chmod +x src/youtube_downloader.py
```

3. **Lancer avec des logs d'erreur** :
```bash
python3 src/youtube_downloader.py 2>&1 | tee error.log
```

---

### ⚠️ Téléchargement très lent

**Causes** :
- Connexion Internet lente
- Serveur YouTube surchargé
- Qualité trop élevée

**Solutions** :
- Choisir une qualité inférieure (480p ou 360p)
- Télécharger à un autre moment
- Vérifier votre connexion Internet

---

### ⚠️ Qualité demandée non disponible

**Symptôme** : Message "Qualité non disponible, utilisation de la meilleure qualité"

**Explication** : La vidéo n'est pas disponible dans la qualité demandée.

**Solution** : L'application télécharge automatiquement la meilleure qualité disponible. Aucune action nécessaire.

---

### ❌ Erreur : "Permission denied"

**Cause** : Pas de permission d'écriture dans le dossier de destination.

**Solution** :
```bash
# Changer les permissions du dossier
chmod 755 ~/Videos

# Ou choisir un autre dossier (Downloads par exemple)
```

---

### ❌ L'icône ne s'affiche pas

**Solution Linux** :
```bash
# Mettre à jour le cache des icônes
gtk-update-icon-cache ~/.local/share/icons/
update-desktop-database ~/.local/share/applications/
```

---

### ❌ Command 'youtube-downloader' not found

**Cause** : `~/.local/bin` n'est pas dans le PATH.

**Solution** :
```bash
# Vérifier le PATH
echo $PATH | grep ".local/bin"

# Si absent, ajouter au PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Ou utiliser le chemin complet
~/.local/share/youtube-downloader/youtube_downloader.py
```

---

### ⚠️ Playlist : Certaines vidéos échouent

**Comportement normal** : Certaines vidéos d'une playlist peuvent être :
- Privées
- Supprimées
- Restreintes

**Solution** : L'application continue avec les vidéos suivantes. Les erreurs sont affichées dans le journal.

---

### ❌ Sous-titres non téléchargés

**Causes** :
- Vidéo sans sous-titres
- Sous-titres auto-générés non disponibles

**Vérification** :
- Aller sur YouTube et vérifier si la vidéo a des sous-titres (icône CC)

---

## 🔍 Diagnostic avancé

### Vérifier l'installation complète
```bash
# Vérifier Python
python3 --version

# Vérifier pip
pip3 --version

# Vérifier pytube
pip3 show pytube

# Tester Tkinter
python3 -c "import tkinter; print('Tkinter OK')"

# Vérifier les permissions
ls -la ~/.local/share/youtube-downloader/
```

### Logs détaillés

Pour obtenir des logs détaillés :
```bash
# Lancer avec mode debug
python3 -v src/youtube_downloader.py 2>&1 | tee debug.log
```

### Tester pytube manuellement
```bash
python3
>>> from pytube import YouTube
>>> yt = YouTube('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
>>> print(yt.title)
>>> exit()
```

---

## 🆘 Signaler un bug

Si le problème persiste :

1. **Vérifier les problèmes existants** sur GitHub
2. **Créer un nouveau problème** avec :
   - Votre système d'exploitation et version
   - Version de Python (`python3 --version`)
   - Version de pytube (`pip3 show pytube`)
   - Message d'erreur complet
   - Étapes pour reproduire le problème

---

## 🔄 Réinstallation propre

Si rien ne fonctionne, réinstallation complète :
```bash
# 1. Désinstaller
~/.local/share/youtube-downloader/uninstall.sh

# 2. Nettoyer
rm -rf ~/.local/share/youtube-downloader
rm -f ~/.local/bin/youtube-downloader
rm -f ~/.local/share/applications/youtube-downloader.desktop

# 3. Supprimer pytube
pip3 uninstall pytube

# 4. Réinstaller
cd youtube-downloader-pro
./install.sh
```

---

## 📚 Ressources utiles

- [Documentation pytube](https://pytube.io/)
- [Documentation Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Python.org](https://www.python.org/)

---

## ⚡ Optimisations

### Améliorer les performances
```bash
# Utiliser un dossier SSD pour les téléchargements
# Éviter les dossiers synchronisés (Dropbox, Google Drive)
# Fermer les autres applications gourmandes
```

### Téléchargements multiples

Pour télécharger plusieurs vidéos, lancez plusieurs instances de l'application (déconseillé pour les playlists).

---

**Besoin d'aide supplémentaire ?** Ouvrez une issue sur GitHub !