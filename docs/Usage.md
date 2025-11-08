# 📘 Guide d'utilisation

## 🚀 Lancer l'application

### Depuis le menu d'applications (Linux)
1. Ouvrir le menu d'applications
2. Rechercher "YouTube Downloader Pro"
3. Cliquer sur l'icône

### Depuis le terminal
```bash
youtube-downloader
```

### Directement
```bash
python3 src/youtube_downloader.py
```

## 🎯 Télécharger une vidéo simple

1. **Copier l'URL YouTube**
   - Aller sur YouTube
   - Copier l'URL de la vidéo (ex: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)

2. **Coller dans l'application**
   - Coller l'URL dans le champ "URL YouTube"

3. **Choisir le type**
   - 📹 **Vidéo** : Pour télécharger la vidéo complète
   - 🎵 **Audio** : Pour extraire uniquement le son

4. **Sélectionner la qualité** (pour les vidéos)
   - 2160p (4K)
   - 1440p (2K)
   - 1080p (Full HD)
   - 720p (HD) ⭐ Recommandé
   - 480p (SD)
   - 360p

5. **Cliquer sur TÉLÉCHARGER**

6. **Suivre la progression**
   - Le journal d'activité affiche la progression en temps réel

## 📋 Télécharger une playlist

1. Copier l'URL de la playlist YouTube
2. Coller dans le champ URL
3. **Cocher "📋 Télécharger playlist complète"**
4. Choisir les options (type, qualité)
5. Cliquer sur TÉLÉCHARGER

⚠️ Les playlists peuvent prendre du temps selon le nombre de vidéos !

## ⚙️ Options avancées

### Changer le dossier de destination

1. Cliquer sur **"📁 Parcourir"**
2. Sélectionner le dossier souhaité
3. Les fichiers seront téléchargés dans ce dossier

**Dossiers par défaut** :
- Linux : `~/Videos` ou `~/Downloads`
- Windows : `C:\Users\VotreNom\Downloads`
- macOS : `~/Downloads`

### Télécharger les sous-titres

1. Cocher **"📝 Inclure les sous-titres"**
2. Les sous-titres seront téléchargés au format `.srt`
3. Langues recherchées : Français → Anglais → Autre

### Changer le format vidéo

1. Dans "Options avancées"
2. Sélectionner le format :
   - **MP4** ⭐ Recommandé (compatible partout)
   - **WebM** (léger, bonne qualité)
   - **MKV** (haute qualité, gros fichiers)

## 🎵 Extraction audio

Pour télécharger uniquement l'audio d'une vidéo :

1. Sélectionner **🎵 Audio uniquement**
2. Le format qualité n'est plus nécessaire
3. L'audio sera extrait au meilleur débit disponible
4. Le fichier sera au format audio natif de YouTube

💡 **Astuce** : Pour convertir en MP3, utilisez un convertisseur audio après téléchargement.

## 📊 Comprendre le journal d'activité

Le journal affiche :
- ✓ Actions réussies (vert)
- → Informations (blanc)
- ⚠ Avertissements (jaune)
- ✗ Erreurs (rouge)

Exemple de téléchargement :
```
→ Connexion à YouTube...
→ Titre: Ma super vidéo
→ Durée: 3m 45s
→ Vues: 1,234,567
→ Recherche de la qualité 720p...
→ Vidéo trouvée: 720p - video/mp4
→ Téléchargement vers: /home/user/Videos
→ Téléchargement en cours...
  → Progression: 10%
  → Progression: 20%
  ...
  → Progression: 90%
✓ Fichier téléchargé!
==================================================
✓ TÉLÉCHARGEMENT TERMINÉ AVEC SUCCÈS!
==================================================
```

## 🗑️ Effacer le journal

Cliquer sur **"🗑️ Effacer le journal"** pour nettoyer l'affichage.

## ⚡ Raccourcis et astuces

### Raccourcis clavier
- `Ctrl+V` : Coller l'URL
- `Ctrl+A` : Tout sélectionner dans le champ URL
- `Tab` : Naviguer entre les options

### Astuces
- **Vérifier avant** : Regardez toujours la vidéo avant de télécharger
- **Qualité 720p** : Meilleur compromis qualité/taille
- **Audio uniquement** : Plus rapide et plus léger
- **Playlists** : Évitez les très longues playlists (>50 vidéos)

## 📱 Types d'URL supportées

### Vidéo unique
```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
```

### Playlist
```
https://www.youtube.com/playlist?list=PLAYLIST_ID
https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID
```

## ❓ Questions fréquentes

**Q : Pourquoi la qualité 4K n'est pas disponible ?**
A : Toutes les vidéos ne sont pas disponibles en 4K. L'application utilisera la meilleure qualité disponible.

**Q : Puis-je télécharger plusieurs vidéos en même temps ?**
A : Non, téléchargez une vidéo à la fois pour éviter les problèmes.

**Q : Où vont mes téléchargements ?**
A : Par défaut dans `~/Videos` (Linux) ou `~/Downloads`. Vous pouvez changer ce dossier.

**Q : Le téléchargement est lent, que faire ?**
A : Cela dépend de votre connexion Internet et de YouTube. Choisissez une qualité inférieure.

**Q : Puis-je télécharger des vidéos privées ?**
A : Non, seulement les vidéos publiques.

## ⚠️ Limitations

- Vidéos publiques uniquement
- Dépend de la disponibilité sur YouTube
- Nécessite une connexion Internet
- Respecte les limitations de débit de YouTube

## 📞 Support

En cas de problème, consultez [TROUBLESHOOTING.md](TROUBLESHOOTING.md)