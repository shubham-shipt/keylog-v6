
<h1 align="center">🔐 Keylog-v6</h1>
<p align="center">
  Advanced Python Keylogger with GUI, Encryption, Email Alerts, and Real-time Monitoring
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/License-For%20Educational%20Use-orange?style=flat-square" />
  <img src="https://img.shields.io/github/stars/shubham-shipt/keylog-v6?style=social" />
</p>

---

## 📌 Overview
**Keylog-v6** is a feature-rich keylogger built in Python with a sleek Tkinter GUI. It logs keystrokes, mouse clicks, takes screenshots, and sends encrypted logs via email—all with stealth mode and customizable themes.

---

## 🎯 Features
- 🔐 **AES-Encrypted Logs**: Securely store logs with encryption.
- 🎛 **Modern GUI**: Intuitive interface with multiple themes (`dark`, `mr_robot`, `hacker`, etc.).
- 📃 **Real-Time Preview**: View logs as they are captured.
- 📩 **Email Alerts**: Send logs via SMTP at set intervals.
- 📷 **Auto Screenshots**: Capture on `ENTER` or `CTRL+V`.
- 👻 **Stealth Mode**: Hide with `F12`, pause with `F11`.
- 📁 **Session Management**: Organized session folders with summaries.
- 🔍 **Log Search**: Search logs by keywords.
- 🧹 **Auto-Cleanup**: Delete logs older than 7 days.
- 🖱 **Mouse Tracking**: Log mouse clicks with timestamps.

---

## 🖥️ Screenshots


 
   <p align="center">
     <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/1.png" width="80%" />
   </p>

 
   <p align="center">
     <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/2.png" width="80%" />
   </p>

 
   <p align="center">
     <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/3.png" width="80%" />
   </p>

 
   <p align="center">
     <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/4.png" width="80%" />
   </p>

   <p align="center">
     <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/5.png" width="80%" />
   </p>


## ⚙️ How to Run

### 1. Install Dependencies
```bash
pip install pynput pyperclip pygame cryptography Pillow psutil
```

### 2. Run the Tool
```bash
python keylogger_v6.py
```

---

### 3. Output Structure
```plaintext
📦 keylogs/
    └── log_2025-06-12.txt       # Encrypted logs
    └── summary_2025-06-12.txt   # Session summary
📦 screenshots/
    └── screenshot_2025-06-12_14-20-55.png
🔑 encryption_key.key
```

---

### 4. Hotkeys & Controls

| Action            | Hotkey       |
|-------------------|--------------|
| Toggle Stealth    | F12          |
| Pause/Resume      | F11          |
| Take Screenshot   | ENTER / CTRL+V |

---

### 5. GUI Settings
- Change log folder
- Enable/disable email alerts
- Set screenshot intervals
- Adjust log frequency
- Switch themes
- Enable auto-delete for old logs

---

## 🧠 Technologies Used
- **Python 3.10+**
- Libraries: `Tkinter`, `pynput`, `pygame`, `cryptography`, `psutil`, `pyperclip`, `Pillow`, `smtplib`

---

## 🛡 Disclaimer
⚠️ **For Educational Use Only**  
Do not use this tool on any system without explicit permission. Unauthorized use may be illegal and unethical.

---

## 🙋‍♂️ Author
**Shubham Singh**  
🎓 BCA Student | 🔐 Cybersecurity Enthusiast  
📧 Email: shubham.singh.bca.2023@asb.edu.in  
🔗 GitHub: [@shubham-shipt](https://github.com/shubham-shipt)

---

## ⭐ 
```bash
⭐ Star this repo
🍴 Fork it
👀 Share with friends
```

---





### 📌
```txt
pynput==1.7.6
pyperclip==1.8.2
pygame==2.5.2
cryptography==42.0.5
Pillow==10.3.0
psutil==5.9.8
```
- ✅ **Performance Tip**: `optimize_performance()` is great! Consider adding optional CPU usage limit via `psutil`.

---

## 🚧 Tool Status: Under Maintenance

⚠️ **Note:** This tool is currently under development and maintenance.

- The **Gmail auto-emailing feature** (keyword-based or interval-based sending) is **not fully functional** or deployed correctly yet.
- If you face any issues with **email delivery or keyword alerts**, please don't assume it's broken — .

    💻!

---
