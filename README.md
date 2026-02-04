Automated Router Rebooter & Network Monitor (Designed and built for myself by myself)

This utility automates the process of rebooting a specific router (Orange Flybox 4G) via its web interface using Python and Selenium. Following the reboot, it cycles the local Wi-Fi adapter, monitors network recovery via ping, and performs a speed test to verify connection quality.

It is designed for Ubuntu 24.04 (Wayland) but can be adapted for other Linux distributions.

Prerequisites
System Requirements
OS: Ubuntu 24.04 (or compatible Linux distro)

Browser: Google Chrome or Chromium

Driver: Chromium Driver

Network Manager: nmcli (standard on Ubuntu)

Installation
Update System & Install Drivers Ensure your package list is updated and install the necessary browser drivers.

Bash
sudo apt update
sudo apt install python3-pip chromium-browser chromium-chromedriver
Install Python Dependencies Install the required Python libraries. Note that on Ubuntu 24.04+, you may need --break-system-packages if not using a virtual environment.

Bash
pip install selenium speedtest-cli --break-system-packages
Add Local Binaries to PATH If speedtest-cli is not found after installation, add the local bin directory to your path:

Bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
Configuration
Open the script (reboot-orange.py) and modify the Configuration section at the top:

Python
# --- CONFIGURATION ---
ROUTER_IP = "http://192.168.0.1" 
USERNAME = "admin"
PASSWORD = "YOUR_PASSWORD_HERE"
Adapting for Different Router Models
If you are using a non-Orange Flybox router, the HTML structure will differ. You will need to inspect your router's web page (Right-click -> Inspect) and update the XPath selectors in the script:

Login Fields: Update the XPath for the username and password input fields.

Menu Navigation: Update the click targets for opening the settings menu.

Reboot Button: Locate the specific ID, Class, or Text for the final reboot button.

Usage
Manual Execution
Run the script directly from the terminal:

Bash
python3 reboot-orange.py
Creating a Terminal Alias (Optional)
To run the script from anywhere using a single command (e.g., reboot-wifi):

Open your bash configuration:

Bash
nano ~/.bashrc
Add the following line to the end of the file:

Bash
alias reboot-wifi='python3 /path/to/your/reboot-orange.py'
Save and apply changes:

Bash
source ~/.bashrc
Scheduled Reboot (Cron Job)
To schedule the reboot automatically (e.g., daily at 4:00 AM):

Open the crontab editor:

Bash
crontab -e
Add the following line:

Bash
0 4 * * * /usr/bin/python3 /home/user/Documents/reboot-orange.py >/dev/null 2>&1
Troubleshooting
selenium.common.exceptions.WebDriverException: Ensure chromium-chromedriver is installed and the path in the script (/usr/bin/chromedriver) matches your system path.

Script hangs at "Waiting for router shutdown": This is a visual countdown. If the script crashes here, ensure you have permissions to run nmcli.

ElementNotInteractableException: The script is trying to click an element that is hidden (e.g., inside a dropdown). Ensure the ActionChains hover logic is correctly targeting the parent menu.

Disclaimer
This script handles network credentials and automates hardware power cycles. Ensure you have administrative access to the network equipment before running this tool.