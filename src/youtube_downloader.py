#!/usr/bin/env python3
"""
YouTube Downloader - Application Desktop
Interface graphique locale avec Tkinter
Compatible: Linux, Windows, macOS
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pytube import YouTube, Playlist
import os
import sys
from pathlib import Path
import platform

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("800x500")  # Fenêtre plus compacte
        self.root.configure(bg="#f5f5f5")
        self.show_advanced = False  # Options avancées masquées par défaut
        
        # Détection du système
        self.system = platform.system()
        
        # Configuration des polices selon le système
        if self.system == "Linux":
            self.font_family = "DejaVu Sans"
            self.mono_font = "DejaVu Sans Mono"
        elif self.system == "Darwin":  # macOS
            self.font_family = "SF Pro"
            self.mono_font = "Monaco"
        else:  # Windows
            self.font_family = "Segoe UI"
            self.mono_font = "Consolas"
        
        # Variables
        self.url_var = tk.StringVar()
        self.download_type = tk.StringVar(value="video")
        self.quality_var = tk.StringVar(value="720p")
        self.format_var = tk.StringVar(value="mp4")
        
        # Dossier par défaut selon le système
        if self.system == "Linux":
            default_path = Path.home() / "Videos"
            if not default_path.exists():
                default_path = Path.home() / "Downloads"
        else:
            default_path = Path.home() / "Downloads"
        
        self.output_path = tk.StringVar(value=str(default_path))
        self.playlist_var = tk.BooleanVar(value=False)
        self.subtitles_var = tk.BooleanVar(value=False)
        self.downloading = False
        
        # Créer le dossier s'il n'existe pas
        default_path.mkdir(parents=True, exist_ok=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        # === HEADER ===
        header_frame = tk.Frame(self.root, bg="#dc2626", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎬 YouTube Downloader Pro",
            font=(self.font_family, 24, "bold"),
            bg="#dc2626",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # === MAIN CONTAINER ===
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === URL SECTION ===
        url_frame = tk.LabelFrame(
            main_frame,
            text="  URL YouTube  ",
            font=(self.font_family, 11, "bold"),
            bg="white",
            fg="#333",
            relief=tk.FLAT,
            bd=2
        )
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        url_entry = tk.Entry(
            url_frame,
            textvariable=self.url_var,
            font=(self.font_family, 11),
            relief=tk.FLAT,
            bg="#f9f9f9",
            fg="#333"
        )
        url_entry.pack(fill=tk.X, padx=15, pady=15, ipady=8)
        url_entry.insert(0, "https://www.youtube.com/watch?v=...")
        url_entry.bind("<FocusIn>", lambda e: url_entry.delete(0, tk.END) if url_entry.get().startswith("https://www.youtube.com/watch?v=...") else None)
        
        # === OPTIONS SECTION ===
        options_frame = tk.LabelFrame(
            main_frame,
            text="  Options de téléchargement  ",
            font=(self.font_family, 11, "bold"),
            bg="white",
            fg="#333",
            relief=tk.FLAT,
            bd=2
        )
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Type de téléchargement
        type_frame = tk.Frame(options_frame, bg="white")
        type_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(
            type_frame,
            text="Type:",
            font=(self.font_family, 10, "bold"),
            bg="white",
            fg="#555"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        video_radio = tk.Radiobutton(
            type_frame,
            text="📹 Vidéo",
            variable=self.download_type,
            value="video",
            font=(self.font_family, 10),
            bg="white",
            fg="#333",
            activebackground="white",
            command=self.toggle_quality
        )
        video_radio.pack(side=tk.LEFT, padx=10)
        
        audio_radio = tk.Radiobutton(
            type_frame,
            text="🎵 Audio uniquement",
            variable=self.download_type,
            value="audio",
            font=(self.font_family, 10),
            bg="white",
            fg="#333",
            activebackground="white",
            command=self.toggle_quality
        )
        audio_radio.pack(side=tk.LEFT, padx=10)
        
        # Qualité et Format
        quality_frame = tk.Frame(options_frame, bg="white")
        quality_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Qualité
        self.quality_label = tk.Label(
            quality_frame,
            text="Qualité:",
            font=(self.font_family, 10, "bold"),
            bg="white",
            fg="#555"
        )
        self.quality_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.quality_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=["2160p (4K)", "1440p (2K)", "1080p (Full HD)", "720p (HD)", "480p (SD)", "360p"],
            state="readonly",
            width=15,
            font=(self.font_family, 9)
        )
        self.quality_combo.pack(side=tk.LEFT, padx=(0, 30))
        
        # Format
        tk.Label(
            quality_frame,
            text="Format:",
            font=(self.font_family, 10, "bold"),
            bg="white",
            fg="#555"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        format_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.format_var,
            values=["mp4", "webm", "mkv"],
            state="readonly",
            width=10,
            font=(self.font_family, 9)
        )
        format_combo.pack(side=tk.LEFT)
        
        # Bouton pour afficher/masquer les options avancées
        advanced_toggle_frame = tk.Frame(options_frame, bg="white")
        advanced_toggle_frame.pack(fill=tk.X, padx=15, pady=(5, 15))
        
        self.advanced_toggle_btn = tk.Button(
            advanced_toggle_frame,
            text="▼ Options avancées",
            command=self.toggle_advanced,
            font=(self.font_family, 9),
            bg="#f0f0f0",
            fg="#555",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.advanced_toggle_btn.pack(side=tk.LEFT)
        
        # === ADVANCED OPTIONS ===
        self.advanced_frame = tk.LabelFrame(
            main_frame,
            text="  Options avancées  ",
            font=(self.font_family, 11, "bold"),
            bg="white",
            fg="#333",
            relief=tk.FLAT,
            bd=2
        )
        # Ne pas afficher par défaut
        
        # Dossier de destination
        path_frame = tk.Frame(self.advanced_frame, bg="white")
        path_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(
            path_frame,
            text="Destination:",
            font=(self.font_family, 10, "bold"),
            bg="white",
            fg="#555"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        path_entry = tk.Entry(
            path_frame,
            textvariable=self.output_path,
            font=(self.font_family, 9),
            relief=tk.FLAT,
            bg="#f9f9f9"
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            path_frame,
            text="📁 Parcourir",
            command=self.browse_folder,
            font=(self.font_family, 9),
            bg="#e5e5e5",
            fg="#333",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2"
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Checkboxes
        check_frame = tk.Frame(self.advanced_frame, bg="white")
        check_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        playlist_check = tk.Checkbutton(
            check_frame,
            text="📋 Télécharger playlist complète",
            variable=self.playlist_var,
            font=(self.font_family, 10),
            bg="white",
            fg="#333",
            activebackground="white"
        )
        playlist_check.pack(side=tk.LEFT, padx=(0, 20))
        
        subtitles_check = tk.Checkbutton(
            check_frame,
            text="📝 Inclure les sous-titres",
            variable=self.subtitles_var,
            font=(self.font_family, 10),
            bg="white",
            fg="#333",
            activebackground="white"
        )
        subtitles_check.pack(side=tk.LEFT)
        
        # === BUTTONS (Toujours visibles) ===
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        self.download_btn = tk.Button(
            button_frame,
            text="⬇️  TÉLÉCHARGER",
            command=self.start_download_thread,
            font=(self.font_family, 12, "bold"),
            bg="#dc2626",
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor="hand2",
            activebackground="#b91c1c"
        )
        self.download_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        clear_btn = tk.Button(
            button_frame,
            text="🗑️  Effacer",
            command=self.clear_log,
            font=(self.font_family, 11),
            bg="#6b7280",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=15,
            cursor="hand2",
            activebackground="#4b5563"
        )
        clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # === LOG SECTION (Compact) ===
        log_frame = tk.LabelFrame(
            main_frame,
            text="  Journal d'activité  ",
            font=(self.font_family, 11, "bold"),
            bg="white",
            fg="#333",
            relief=tk.FLAT,
            bd=2
        )
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=6,  # Hauteur réduite
            font=(self.mono_font, 9),
            bg="#1e1e1e",
            fg="#00ff00",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.config(state=tk.DISABLED)
    
    def toggle_advanced(self):
        """Affiche/masque les options avancées"""
        if self.show_advanced:
            # Masquer
            self.advanced_frame.pack_forget()
            self.advanced_toggle_btn.config(text="▼ Options avancées")
            self.root.geometry("800x500")
            self.show_advanced = False
        else:
            # Afficher
            self.advanced_frame.pack(fill=tk.X, after=self.advanced_toggle_btn.master.master, pady=(0, 15))
            self.advanced_toggle_btn.config(text="▲ Masquer les options avancées")
            self.root.geometry("800x650")
            self.show_advanced = True
        
    def toggle_quality(self):
        """Active/désactive les options de qualité selon le type"""
        if self.download_type.get() == "audio":
            self.quality_combo.config(state=tk.DISABLED)
            self.quality_label.config(fg="#999")
        else:
            self.quality_combo.config(state="readonly")
            self.quality_label.config(fg="#555")
    
    def browse_folder(self):
        """Ouvre le dialogue de sélection de dossier"""
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
    
    def log(self, message, color="green"):
        """Ajoute un message au journal"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_log(self):
        """Efface le journal"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def start_download_thread(self):
        """Lance le téléchargement dans un thread séparé"""
        if not self.downloading:
            thread = threading.Thread(target=self.download, daemon=True)
            thread.start()
    
    def download(self):
        """Fonction principale de téléchargement"""
        url = self.url_var.get().strip()
        
        if not url or url.startswith("https://www.youtube.com/watch?v=..."):
            messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube valide!")
            return
        
        self.downloading = True
        self.download_btn.config(state=tk.DISABLED, text="⏳ Téléchargement en cours...")
        
        try:
            output_dir = self.output_path.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.log(f"✓ Dossier créé: {output_dir}")
            
            if self.playlist_var.get() and "playlist" in url:
                self.download_playlist(url, output_dir)
            else:
                self.download_video(url, output_dir)
            
            self.log("\n" + "="*50)
            self.log("✓ TÉLÉCHARGEMENT TERMINÉ AVEC SUCCÈS!")
            self.log("="*50 + "\n")
            messagebox.showinfo("Succès", "Téléchargement terminé avec succès!")
            
        except Exception as e:
            self.log(f"\n✗ ERREUR: {str(e)}\n", "red")
            messagebox.showerror("Erreur", f"Une erreur s'est produite:\n{str(e)}")
        
        finally:
            self.downloading = False
            self.download_btn.config(state=tk.NORMAL, text="⬇️  TÉLÉCHARGER")
    
    def download_video(self, url, output_dir):
        """Télécharge une vidéo unique"""
        self.log(f"→ Connexion à YouTube...")
        yt = YouTube(url, on_progress_callback=self.on_progress)
        
        self.log(f"→ Titre: {yt.title}")
        self.log(f"→ Durée: {yt.length // 60}m {yt.length % 60}s")
        self.log(f"→ Vues: {yt.views:,}")
        
        if self.download_type.get() == "audio":
            self.log("→ Recherche du meilleur flux audio...")
            stream = yt.streams.filter(only_audio=True).first()
            self.log(f"→ Audio trouvé: {stream.abr}")
        else:
            quality = self.quality_var.get().split()[0]  # Extrait "720p" de "720p (HD)"
            self.log(f"→ Recherche de la qualité {quality}...")
            
            stream = yt.streams.filter(
                progressive=True,
                file_extension=self.format_var.get(),
                resolution=quality
            ).first()
            
            if not stream:
                self.log("⚠ Qualité non disponible, utilisation de la meilleure qualité...")
                stream = yt.streams.get_highest_resolution()
            
            self.log(f"→ Vidéo trouvée: {stream.resolution} - {stream.mime_type}")
        
        self.log(f"→ Téléchargement vers: {output_dir}")
        self.log("→ Téléchargement en cours...")
        stream.download(output_path=output_dir)
        self.log("✓ Fichier téléchargé!")
        
        # Sous-titres
        if self.subtitles_var.get():
            self.download_subtitles(yt, output_dir)
    
    def download_playlist(self, url, output_dir):
        """Télécharge une playlist complète"""
        self.log("→ Récupération de la playlist...")
        pl = Playlist(url)
        
        self.log(f"→ Playlist: {pl.title}")
        self.log(f"→ Nombre de vidéos: {len(pl.video_urls)}")
        self.log("="*50 + "\n")
        
        for i, video_url in enumerate(pl.video_urls, 1):
            self.log(f"\n[{i}/{len(pl.video_urls)}] Traitement de la vidéo {i}...")
            try:
                self.download_video(video_url, output_dir)
            except Exception as e:
                self.log(f"✗ Erreur sur la vidéo {i}: {str(e)}")
                continue
    
    def download_subtitles(self, yt, output_dir):
        """Télécharge les sous-titres si disponibles"""
        try:
            self.log("→ Recherche de sous-titres...")
            if yt.captions:
                caption = yt.captions.get_by_language_code('fr') or \
                         yt.captions.get_by_language_code('en') or \
                         list(yt.captions.values())[0]
                
                srt = caption.generate_srt_captions()
                subtitle_path = os.path.join(output_dir, f"{yt.title}_subtitles.srt")
                
                with open(subtitle_path, "w", encoding="utf-8") as f:
                    f.write(srt)
                
                self.log(f"✓ Sous-titres sauvegardés: {caption.code}")
            else:
                self.log("⚠ Aucun sous-titre disponible")
        except Exception as e:
            self.log(f"⚠ Erreur sous-titres: {str(e)}")
    
    def on_progress(self, stream, chunk, bytes_remaining):
        """Callback pour afficher la progression"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        
        # Mettre à jour tous les 10%
        if int(percentage) % 10 == 0 and int(percentage) != 100:
            self.log(f"  → Progression: {int(percentage)}%")

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    
    # Centrer la fenêtre
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()