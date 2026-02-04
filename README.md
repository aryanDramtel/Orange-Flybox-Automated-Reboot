```markdown
# 🚀 Orange Router Auto-Reboot & Monitor
A robust Python automation tool designed for **Ubuntu 24.04** to manage router instability. It handles the web-login, triggers a reboot, refreshes your local Wi-Fi, and verifies the connection with a speed test.

---

## 🛠 Features
* **Selenium Automation:** Handles the "Orange Flybox" web UI automatically.
* **Live Countdown:** A real-time terminal timer for the hardware cycle.
* **Network Self-Healing:** Restarts the local Linux Wi-Fi adapter using `nmcli`.
* **Post-Reboot Analytics:** Pings `8.8.8.8` until online, then runs a full speed test.

---

## 📦 Dependencies

You will need **Python 3.10+**, **Google Chrome**, and the **Chromium Driver**.

### 1. System Packages

```bash
sudo apt update
sudo apt install python3-pip chromium-browser chromium-chromedriver

```

### 2. Python Libraries

```bash
pip install selenium speedtest-cli --break-system-packages

```

### 3. Path Configuration

Ensure your local binaries are recognized by your terminal:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

```

---

## ⚙️ Configuration

Before running, open `reboot-orange.py` and update your credentials:

* **ROUTER_IP**: Usually `http://192.168.0.1`
* **USERNAME**: Default is usually `admin`
* **PASSWORD**: Your specific router management password

> **Note:** If you use a different router model, you may need to adjust the **XPath selectors** in the script to match your device's unique web interface.

---

## 🚀 How to Use

Simply run the script from your terminal:

```bash
python3 reboot-orange.py

```

### What happens next?

1. **Browser Opens:** You'll see Chrome navigate to the reboot settings.
2. **Countdown:** Once the reboot is confirmed, the browser closes and a **20s countdown** begins in the terminal.
3. **Wi-Fi Toggle:** The script disables and re-enables your Ubuntu Wi-Fi.
4. **Health Check:** It waits for a successful ping and then displays your **Upload/Download speeds**.

---

## ⚠️ Troubleshooting

* **Driver Mismatch:** If Chrome updates, you might need to update `chromium-chromedriver`.
* **Element Not Found:** If the router UI changes, use *Inspect Element* in Chrome to find the new XPaths for buttons.
* **Permissions:** Ensure your user has permission to run `nmcli` (standard on most Ubuntu desktop installs).

```

---