import tkinter as tk
from tkinter import filedialog
import pygame
import os
import sys

# Initialize pygame mixer
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing pygame mixer: {e}")
    sys.exit(1)

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x400")

        self.playlist = []
        self.current_song_index = 0
        self.is_paused = False
        self.is_playing = False  # Track if the song is playing

        # Load playlist button
        self.load_button = tk.Button(self.root, text="Load Songs Folder", command=self.load_songs)
        self.load_button.pack(pady=10)

        # Playlist display
        self.playlist_box = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.playlist_box.pack(pady=10, fill=tk.BOTH, expand=True)

        # Playback Controls
        self.play_button = tk.Button(self.root, text="Play", command=self.play_song)
        self.play_button.pack(pady=5, side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_song)
        self.pause_button.pack(pady=5, side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_song)
        self.stop_button.pack(pady=5, side=tk.LEFT, padx=10)

        self.prev_button = tk.Button(self.root, text="Prev", command=self.prev_song)
        self.prev_button.pack(pady=5, side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_song)
        self.next_button.pack(pady=5, side=tk.LEFT, padx=10)

        # Volume control slider
        self.volume_slider = tk.Scale(self.root, from_=0, to_=1, orient=tk.HORIZONTAL, resolution=0.01, label="Volume")
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=10)

        # Set volume based on slider value
        self.volume_slider.bind("<Motion>", self.set_volume)

    def load_songs(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.playlist = [f for f in os.listdir(folder_selected) if f.endswith(".mp3")]
            self.playlist_box.delete(0, tk.END)
            for song in self.playlist:
                self.playlist_box.insert(tk.END, song)
            self.playlist_folder = folder_selected

    def play_song(self):
        if self.playlist:
            song_path = os.path.join(self.playlist_folder, self.playlist[self.current_song_index])

            # If music is already playing, just unpause
            if self.is_playing:
                if self.is_paused:
                    pygame.mixer.music.unpause()
                    self.is_paused = False
                    self.update_buttons("playing")
            else:
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                self.is_playing = True
                self.update_buttons("playing")

    def pause_song(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.update_buttons("paused")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.update_buttons("stopped")

    def prev_song(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.stop_and_play_next()

    def next_song(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.stop_and_play_next()

    def stop_and_play_next(self):
        pygame.mixer.music.stop()  # Ensure current song stops first
        self.is_playing = False
        self.is_paused = False
        self.play_song()  # Play the next song immediately

    def set_volume(self, event=None):
        pygame.mixer.music.set_volume(self.volume_slider.get())

    def update_buttons(self, state):
        if state == "playing":
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
        elif state == "paused":
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

# Set up root window and start app
root = tk.Tk()

try:
    app = MusicPlayerApp(root)
    root.mainloop()
except Exception as e:
    print(f"An error occurred while starting the app: {e}")
    sys.exit(1)
