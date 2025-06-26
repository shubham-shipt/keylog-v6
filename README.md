<h1 align="center">🔐 Keylog-v6: Advanced Python Keylogger with GUI, Encryption & Email Alerts</h1>

<p align="center">
  A stealthy, feature-rich Python keylogger with GUI, encrypted logs, screenshot capture, email alerts, and real-time tracking — built for educational cybersecurity research.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/License-Educational%20Use-orange?style=flat-square" />
  <img src="https://img.shields.io/github/stars/shubham-shipt/keylog-v6?style=social" />
<!--   <img src="https://img.shields.io/github/forks/shubham-shipt/keylog-v6?style=flat-square" /> -->
  <img src="https://img.shields.io/github/issues/shubham-shipt/keylog-v6?style=flat-square" />
  <img src="https://visitor-badge.laobi.icu/badge?page_id=shubham-shipt.keylog-v6" />
</p>

---

## 📚 Table of Contents
- [📌 Overview](#-overview)
- [🎯 Features](#-features)
- [🖥️ Screenshots](#️-screenshots)
- [⚙️ How to Run](#️-how-to-run)
- [🧠 Technologies Used](#-technologies-used)
- [🛡 Disclaimer](#-disclaimer)
- [🙋‍♂️ Author](##-author)
- [⭐ Support](#-support)
- [🚧 Tool Status](#-tool-status)

---

## 📌 Overview
**Keylog-v6** is a powerful Python-based keylogger with a modern Tkinter GUI. It logs keystrokes, tracks mouse clicks, captures screenshots, and emails encrypted logs — all while running in stealth mode. Designed for learning and ethical hacking labs.

---

## 🎯 Features
- 🔐 AES-Encrypted Logs
- 🎛 GUI with Light/Dark Themes
- 📃 Real-Time Log Preview
- 📩 Email Alerts via SMTP
- 📷 Auto Screenshots on `ENTER` or `CTRL+V`
- 👻 Stealth Mode Toggle with `F12`, Pause with `F11`
- 📁 Organized Session Management
- 🔍 Log Search Feature
- 🧹 Auto Cleanup (7-day limit)
- 🖱 Mouse Click Logging

---

## 🖥️ Screenshots

<p align="center">
  <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/1.png" width="80%" />
  <br/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/2.png" width="80%" />
  <br/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/3.png" width="80%" />
  <br/><i>⚙️ Settings Panel</i>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/4.png" width="80%" />
  <br/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/shubham-shipt/keylog-v6/main/5.png" width="80%" />
  <br/>
</p>

---

## ⚙️ How to Run

### 1. Install Dependencies
```bash
pip install pynput pyperclip pygame cryptography Pillow psutil
```

### 2. Run the Tool
```bash
python keylogger_v6.py
```

### 3. Output Structure
```plaintext
📦 keylogs/
    └── log_YYYY-MM-DD.txt       # Encrypted log
    └── summary_YYYY-MM-DD.txt   # Summary file
📦 screenshots/
    └── screenshot_YYYY-MM-DD_HH-MM-SS.png
🔑 encryption_key.key
```

### 4. Hotkeys & Controls

| Action            | Hotkey       |
|-------------------|--------------|
| Toggle Stealth    | F12          |
| Pause/Resume      | F11          |
| Take Screenshot   | ENTER / CTRL+V |

---

### 5. GUI Settings
- 📂 Change log directory
- ✉️ Enable/disable email alerts
- 🕐 Set screenshot interval
- 📈 Adjust log frequency
- 🎨 Switch themes
- 🧹 Auto-delete old logs

---

## 🧠 Technologies Used
- **Python 3.10+**
- Libraries: `Tkinter`, `pynput`, `pygame`, `cryptography`, `psutil`, `pyperclip`, `Pillow`, `smtplib`

---

## 🛡 Disclaimer
> ⚠️ This project is for **educational purposes only**. Do **NOT** use this tool on unauthorized devices. Improper use may lead to legal consequences.

---

## 🙋‍♂️ Author
**Shubham Singh**  
🎓 BCA Student | 🛡️ Cybersecurity Enthusiast  
📧 Email: shubham.singh.bca.2023@asb.edu.in  
🔗 GitHub: [@shubham-shipt](https://github.com/shubham-shipt)

---

## ⭐ Support
If you find this helpful, please consider:

⭐ Starring the repo  
🍴 Forking the project  
📢 Sharing with friends  
🐞 Reporting issues [here](https://github.com/shubham-shipt/keylog-v6/issues)

---

## 🚧 Tool Status
🛠 **Under Active Development**

- Auto email alerts are currently in testing mode.  
- If keyword-based alerts or delivery fails, it may be due to ongoing updates.

---

## 📦 Dependency Versions
```txt
pynput==1.7.6
pyperclip==1.8.2
pygame==2.5.2
cryptography==42.0.5
Pillow==10.3.0
psutil==5.9.8
```

✅ Tip: Use `optimize_performance()` to manage CPU usage via `psutil`.

