import pyttsx3
import tkinter as tk
import pygame
from datetime import datetime
import os


class TTS:
    def __init__(self):
        pygame.mixer.init()
        self.tts_engine = pyttsx3.init()
        self.default_settings()
        self.audio_file = self.generate_audio_file_name()

    def default_settings(self):
        self.set_volume(1)
        self.set_voices(0)
        self.set_rate(150)

    def save_settings(self):
        self.get_volume()
        self.get_voice_index()
        self.get_rate()
        # Working on this

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def get_volume(self):
        return pygame.mixer.music.get_volume()

    def set_rate(self, rate):
        self.tts_engine.setProperty("rate", rate)

    def get_rate(self):
        return self.tts_engine.getProperty("rate")

    def set_voices(self, voice_index):
        voices = self.tts_engine.getProperty("voices")
        self.tts_engine.setProperty("voice", voices[voice_index].id)

    def get_voice_index(self):
        voices = self.tts_engine.getProperty("voices")
        current_voice_id = self.tts_engine.getProperty("voice")
        for index, voice in enumerate(voices):
            if voice.id == current_voice_id:
                return index
        return 0

    def get_voice_names(self):
        voices = self.tts_engine.getProperty("voices")
        return [voice.name for voice in voices]

    def generate_audio_file_name(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_dir = "audio_files"
        os.makedirs(audio_dir, exist_ok=True)
        return os.path.join(audio_dir, f"speech_{timestamp}.wav")

    def save_speech(self, text):
        self.audio_file = self.generate_audio_file_name()
        self.tts_engine.save_to_file(text, self.audio_file)
        self.tts_engine.runAndWait()

    def play_audio(self):
        if os.path.exists(self.audio_file):
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()

    def is_audio_playing(self):
        return pygame.mixer.music.get_busy()

    def get_text_to_speak(self, text_input):
        text = text_input.get("1.0", tk.END).strip()
        if text and text != "Enter text here...":
            self.stop_audio()
            self.save_speech(text)
            self.play_audio()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def pause_audio(self):
        pygame.mixer.music.pause()

    def resume_audio(self):
        pygame.mixer.music.unpause()


class TTS_GUI():
    def __init__(self):
        self.tts = TTS()
        self.is_playing = False
        self.is_paused = False
        self.init_tkinter()

    def init_tkinter(self):
        root = tk.Tk()
        root.geometry("1920x1080")
        root.state('zoomed')
        root.title("QuickTTS")

        # Title Label
        title = tk.Label(root, text="QuickTTS", font=('Segoe UI', 30))
        title.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")

        # Text Input
        def add_placeholder(event=None):
            if text_input.get("1.0", "end-1c") == "":
                text_input.insert("1.0", placeholder_text)
                text_input.config(fg="grey")

        def remove_placeholder(event=None):
            if text_input.get("1.0", "end-1c") == placeholder_text:
                text_input.delete("1.0", "end")
                text_input.config(fg="black")

        placeholder_text = "Enter text here..."

        text_input = tk.Text(root, font=('Segoe UI', 15), wrap=tk.WORD)
        text_input.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")

        text_input.insert("1.0", placeholder_text)
        text_input.config(fg="grey")

        text_input.bind("<FocusIn>", remove_placeholder)
        text_input.bind("<FocusOut>", add_placeholder)

        # Play/Stop Button
        def toggle_play_stop():
            if not self.is_playing:
                self.is_playing = True
                self.is_paused = False
                play_stop_button.config(text="Stop")
                pause_resume_button.config(state="normal", text="Pause")
                self.tts.get_text_to_speak(text_input)
                check_audio_status()
            else:
                self.is_playing = False
                play_stop_button.config(text="Play")
                pause_resume_button.config(state="normal", text="Pause")
                pause_resume_button.config(state="disabled")
                self.tts.stop_audio()

        play_stop_button = tk.Button(
            root,
            font=('Segoe UI', 15),
            text="Play",
            command=toggle_play_stop
        )
        play_stop_button.grid(row=3, column=0, padx=20, pady=5, sticky="e")

        # Pause/Resume Button
        def toggle_pause_resume():
            if self.is_playing:
                if not self.is_paused:
                    self.is_paused = True
                    pause_resume_button.config(text="Resume")
                    self.tts.pause_audio()
                else:
                    self.is_paused = False
                    pause_resume_button.config(text="Pause")
                    self.tts.resume_audio()

        pause_resume_button = tk.Button(
            root,
            font=('Segoe UI', 15),
            text="Pause",
            command=toggle_pause_resume,
            state="disabled"
        )
        pause_resume_button.grid(row=3, column=1, padx=20, pady=5, sticky="w")

        # Volume Slider
        volume_slider = tk.Scale(
            root,
            from_=0,
            to=1,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            label="Volume",
            command=lambda v: self.tts.set_volume(float(v))
        )
        volume_slider.set(self.tts.get_volume())
        volume_slider.grid(row=5, column=0, padx=20, pady=5, sticky="e")

        # Speed Slider
        speed_slider = tk.Scale(
            root,
            from_=0,
            to=1000,
            orient=tk.HORIZONTAL,
            label="Speed (words per minute)",
            command=lambda v: self.tts.set_rate(int(v))
        )
        speed_slider.set(self.tts.get_rate())
        speed_slider.grid(row=5, column=1, padx=20, pady=5, sticky="w")

        # Voice Selector
        voice_var = tk.StringVar(value="Select Voice")
        voices = self.tts.get_voice_names()
        voice_menu = tk.OptionMenu(root, voice_var, *voices,
                                   command=lambda voice: self.tts.set_voices(voices.index(voice)))
        voice_var.set(voices[self.tts.get_voice_index()])
        voice_menu.grid(row=6, column=0, columnspan=2, pady=(10, 20))

        # Configuring grid to expand elements with window resizing
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        def check_audio_status():
            if self.tts.is_audio_playing() or self.is_paused:
                root.after(100, check_audio_status)
            else:
                self.is_playing = False
                play_stop_button.config(text="Play")
                pause_resume_button.config(state="disabled")

        check_audio_status()

        # Running the GUI
        root.mainloop()


def main():
    tts_gui = TTS_GUI()


if __name__ == "__main__":
    main()
