import tkinter as tk
from tkinter import ttk
import random
import string
import time
import threading

class Themes:
    def __init__(self):
        self.theme = "mr_robot"
        self.themes = {
            "dark": {"bg": "#1c2526", "fg": "#00ff00", "button_bg": "#2e2e2e", "button_fg": "#00ff00", "hover_bg": "#3a3a3a"},
            "light": {"bg": "#ffffff", "fg": "#000000", "button_bg": "#e0e0e0", "button_fg": "#000000", "hover_bg": "#d0d0d0"},
            "hacker": {"bg": "#000000", "fg": "#00ff00", "button_bg": "#1a1a1a", "button_fg": "#00ff00", "hover_bg": "#2a2a2a"},
            "mr_robot": {"bg": "#000000", "fg": "#ff0000", "button_bg": "#1a1a1a", "button_fg": "#ff0000", "hover_bg": "#2a2a2a", "glitch": True},
            "green": {"bg": "#003300", "fg": "#00ff00", "button_bg": "#006600", "button_fg": "#00ff00", "hover_bg": "#008000"},
            "purple": {"bg": "#2a0033", "fg": "#cc00ff", "button_bg": "#4d0066", "button_fg": "#cc00ff", "hover_bg": "#660099"},
            "red": {"bg": "#330000", "fg": "#ff0000", "button_bg": "#660000", "button_fg": "#ff0000", "hover_bg": "#990000"}
        }

    def apply_theme(self, root, main_frame, preview_text):
        style = ttk.Style()
        style.configure("TFrame", background=self.themes[self.theme]["bg"])
        style.configure("TLabel", background=self.themes[self.theme]["bg"], foreground=self.themes[self.theme]["fg"], font=("Consolas", 10))
        style.configure("TButton", background=self.themes[self.theme]["button_bg"], foreground=self.themes[self.theme]["button_fg"], font=("Consolas", 10, "bold"))
        style.configure("Hover.TButton", background=self.themes[self.theme]["hover_bg"], foreground=self.themes[self.theme]["button_fg"], font=("Consolas", 10, "bold"))
        style.configure("TEntry", fieldbackground=self.themes[self.theme]["bg"], foreground=self.themes[self.theme]["fg"], font=("Consolas", 10))
        style.configure("TCheckbutton", background=self.themes[self.theme]["bg"], foreground=self.themes[self.theme]["fg"], font=("Consolas", 10))
        root.configure(bg=self.themes[self.theme]["bg"])
        main_frame.configure(style="TFrame")
        preview_text.configure(bg=self.themes[self.theme]["bg"], fg=self.themes[self.theme]["fg"])
        if self.themes[self.theme].get("glitch", False):
            self.apply_glitch_effect(preview_text)

    def apply_glitch_effect(self, preview_text):
        def glitch():
            while self.theme == "mr_robot" and self.app.is_logging:
                if random.random() < 0.1:
                    preview_text.configure(state="normal")
                    preview_text.insert(tk.END, random.choice(string.ascii_letters) + " ")
                    preview_text.see(tk.END)
                    preview_text.configure(state="disabled")
                    preview_text.after(50, lambda: preview_text.delete("end-2c", "end"))
                time.sleep(0.1)
        threading.Thread(target=glitch, daemon=True).start()

    def toggle_theme(self):
        theme_list = list(self.themes.keys())
        self.theme = theme_list[(theme_list.index(self.theme) + 1) % len(theme_list)]