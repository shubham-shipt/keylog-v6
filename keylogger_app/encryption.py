from cryptography.fernet import Fernet
import os
from tkinter import messagebox

class Encryption:
    def __init__(self):
        self.key_file = "encryption_key.key"
        self.encryption_key = None
        self.cipher = None
        self.setup_encryption()

    def setup_encryption(self):
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, "rb") as f:
                    self.encryption_key = f.read()
            else:
                self.encryption_key = Fernet.generate_key()
                with open(self.key_file, "wb") as f:
                    f.write(self.encryption_key)
            self.cipher = Fernet(self.encryption_key)
        except Exception as e:
            messagebox.showerror("Error", f"Encryption setup failed: {str(e)}")