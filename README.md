<h1 align="center">🦉 Keylogger Tool V12</h1>

<p align="center">
  <img src="Images/1.png" alt="Keylogger Main UI" width="480" style="border-radius:12px;box-shadow:0 4px 24px #0002"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-22223B?style=plastic&logo=python&logoColor=FFD343" height="22">
  <img src="https://img.shields.io/badge/Windows-Full-0078D6?style=plastic&logo=windows&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/Linux-Partial-22223B?style=&logo=linux&logoColor=FCC624" height="22">
  <img src="https://img.shields.io/badge/MacOS-Partial-000000?style=&logo=apple&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/Stealth-F12_Instant-6e40c9?style=plastic&logo=ghost&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/Clipboard-Logger-44C767?style=plastic&logo=clipboard&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/Screenshots-Manual-3B8EEA?style=plastic&logo=image&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/Mouse-Clicks/Scrolls-27ae60?style=plastic&logo=mouse&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/AI_Summaries-Yes-00B2FF?style=plastic&logo=openai&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/Logs-Encrypted-8d71e3?style=plastic&logo=lock&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/GUI-Tkinter+Icons-5E81AC?style=plastic&logo=windowsterminal&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/Themes-7%2B_Hacker-1eaaae?style=plastic&logo=artstation&logoColor=white" height="22">
  <img src="https://img.shields.io/badge/Offline-100%25-lightgray?style=plastic&logo=cloud&logoColor=gray" height="22">
  <img src="https://visitor-badge.laobi.icu/badge?page_id=shubham-shipt.keylog-v6&left_color=gray&right_color=1eaaae&style=plastic" alt="Repo Visitors" height="22">
</p>

---

<details>
<summary>⚡ <b>Quick Install</b> <i>(click)</i></summary>

```bash
git clone https://github.com/shubham-shipt/keylog-v6.git
cd keylog-v6

# Install all required libraries
pip install pynput pillow cryptography pygame pyperclip tk

# (Or, for all dependencies at once)
pip install -r requirements.txt

# Run the script
python keylogger_v12.py
```
</details>


<details>
<summary>🔎 <b>Info & Usage</b> <i>(click)</i></summary>

- **Category:** <span style="color:#FF5E57"><b>Tool (Only!)</b></span>
- **Logs:** Keystrokes, clipboard, screenshots, mouse, Application used by users with time, AI summaries
- **Platforms:** Windows (full), Linux/Mac (partial)
- **No cloud, no email alerts, 100% offline, encrypted logs**
- **For legal, ethical, and educational research only. Unauthorized use is illegal and unethical.**

</details>

<details>
<summary>🛡️ <b>How to Decrypt Fernet Encrypted Strings</b> <i>(click)</i></summary>


```python
from cryptography.fernet import Fernet

# Replace with your key and token
key = b'YOUR_KEY_HERE'
token = b'YOUR_ENCRYPTED_STRING_HERE'

fernet = Fernet(key)
decrypted = fernet.decrypt(token)
print(decrypted.decode())
```

**How it works:**  
- Install the cryptography library:  
  `pip install cryptography`
- Paste your key and token into the script above.
- Run the script.  
- **The output will be printed in your terminal as plain text after decryption.**

</details>
<details>
<summary>📝 <b>Example Keylogger Output Summary</b> <i>(click to expand)</i></summary>

```text
───────────── KEYLOGGER SUMMARY ─────────────
Session Start: 2025-07-30 09:12:01
Session End  : 2025-07-30 14:45:17
Total Duration: 5 hours 33 mins

[🟢 WhatsApp]
 - 09:14:20 → 09:16:05
 - Typed: "Hey, are we meeting at 5pm? 👍"
 - Copied: "Location: Cafe Coffee Day"

[🔵 Telegram]
 - 09:20:40 → 09:23:12
 - Typed: "Sending the project files now."
 - Screenshot taken at 09:21:18

[🌐 Chrome]
 - 10:05:10 → 11:27:58
 - Typed: "github copilot documentation"
 - Copied: "https://github.com/features/copilot"
 - Mouse: 14 clicks, 6 scrolls
 - Screenshot taken at 10:10:44

[📝 Notepad]
 - 12:00:33 → 12:25:01
 - Typed: 
    "Todo:
    - Finish report
    - Email John
    - Backup files"
 - Clipboard: "Confidential: Salary.xlsx"

[🗂️ Explorer]
 - 13:55:09 → 14:07:44
 - Actions: 4 files renamed, 2 files deleted
 - Screenshot taken at 14:00:00

───────────── END OF SUMMARY ─────────────
```

</details>
---

## 🧩 Feature Grid

<table align="center">
<tr>
  <th>🕵️ Stealth</th>
  <th>📋 Clipboard</th>
  <th>🖼️ Screenshots</th>
  <th>🖱️ Mouse</th>
  <th>🔒 Encrypted</th>
  <th>🎨 Themes</th>
  <th>🤖 AI Logs</th>
  <th>🖥️ GUI</th>
</tr>
<tr>
  <td align="center"><img src="https://img.icons8.com/fluency/22/spy.png"/> F12</td>
  <td align="center"><img src="https://img.icons8.com/fluency/22/clipboard.png"/> Text/Image</td>
  <td align="center"><img src="https://img.icons8.com/fluency/22/screenshot.png"/> Manual</td>
  <td align="center"><img src="https://img.icons8.com/fluency/22/mouse.png"/> Click/Scroll</td>
  <td align="center"><img src="https://img.icons8.com/fluency/22/lock.png"/> Fernet</td>
  <td align="center"><img src="https://img.icons8.com/fluency/22/art-prices.png"/> 7+</td>
  <td align="center"><img src="https://img.icons8.com/color/22/artificial-intelligence.png"/> AI</td>
  <td align="center"><img src="https://img.icons8.com/fluency/22/monitor.png"/> Tkinter</td>
</tr>
</table>

---

## 🏗️ Architecture

<p align="center">
  <img src="Images/6.png" alt="Keylogger Architecture" width="680" style="border-radius:10px;box-shadow:0 2px 12px #0002"/>
</p>

---

## 🌌 Visual Gallery

<p align="center">
  <img src="Images/7.png" alt="Log Preview" width="220" style="margin:0 10px; border-radius:10px; box-shadow:0 2px 8px #0002"/>
  <img src="Images/4.png" alt="Clipboard Logging" width="210" style="margin:0 10px; border-radius:10px; box-shadow:0 2px 8px #0002"/>
  <img src="Images/3.png" alt="File Explorer" width="180" style="margin:0 10px; border-radius:10px; box-shadow:0 2px 8px #0002"/>
  <img src="Images/5.png" alt="File Explorer" width="180" style="margin:0 10px; border-radius:10px; box-shadow:0 2px 8px #0002"/>
 <img src="Images/2.png" alt="File Explorer" width="180" style="margin:0 10px; border-radius:10px; box-shadow:0 2px 8px #0002"/>
</p>

---

## 📦 Tech Stack

**Python Libraries Used:**  
`pynput`, `pillow`, `cryptography`, `pygame`, `pyperclip`, `tkinter`

---


>
> 🟢 **Manual Run:** Open the script, understand the code, and execute it as per your custom needs.

---

> ⚠️ **Legal Notice:**  
> This tool is for **educational, Purpose 😁**.  

---

<p align="center">
  <a href="https://github.com/shubham-shipt/keylog-v6">
    <img src="https://img.shields.io/badge/GitHub-View%20Source-181717?style=plastic&logo=github&logoColor=white" alt="View Source on GitHub" height="26">
  </a>
</p>
