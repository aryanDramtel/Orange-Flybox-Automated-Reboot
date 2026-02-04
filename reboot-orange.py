import time
import sys
import subprocess
import speedtest  # Run 'pip install speedtest-cli' if not already done
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --- CONFIGURATION ---
ROUTER_IP = "http://192.168.0.1" 
USERNAME = "admin"
PASSWORD = "<your_password_here>"

# --- ANSI COLORS ---
G, Y, R, W = '\033[92m', '\033[93m', '\033[91m', '\033[0m'

def check_ping():
    """Checks if the internet is reachable."""
    try:
        # Pings Google DNS
        subprocess.check_output(["ping", "-c", "1", "-W", "1", "8.8.8.8"])
        return True
    except:
        return False

def run_speed_test():
    """Measures and displays internet metrics."""
    print(f"{Y}[*] Measuring network performance...{W}")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000 
        upload = st.upload() / 1_000_000      
        latency = st.results.ping
        
        print(f"\n{G}--- INTERNET STATUS REPORT ---{W}")
        print(f"Download: {download:.2f} Mbps")
        print(f"Upload:   {upload:.2f} Mbps")
        print(f"Latency:  {latency:.2f} ms")
        print(f"{G}-------------------------------{W}\n")
    except Exception as e:
        print(f"{R}[!] Speedtest failed: {e}{W}")

# --- BROWSER AUTOMATION (VISIBLE) ---
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("detach", True) 

service = Service(executable_path="/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print(f"{Y}[*] Starting Visible Reboot Sequence...{W}")
    driver.get(ROUTER_IP)
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)

    # 1. LOGIN
    user_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//main[@class='modal-body']//input[@type='text']")))
    user_field.send_keys(USERNAME)
    pass_field = driver.find_element(By.XPATH, "//main[@class='modal-body']//input[@type='password']")
    pass_field.send_keys(PASSWORD)
    pass_field.send_keys(Keys.TAB)
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[contains(text(), 'Ok')]").click()

    # 2. NAVIGATE TO REBOOT
    menu_wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "menu-wrapper")))
    actions.move_to_element(menu_wrapper).perform()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Settings')]"))).click()
    
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='Settings-section-left']//li[text()='Reboot']"))).click()
    time.sleep(1.5) 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='Settings-section-right']//a[contains(., 'Reboot')]"))).click()

    # 3. CONFIRM REBOOT
    wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='modal-main page-box']//a[text()='Confirm']"))).click()
    print(f"{G}[+] Reboot command sent successfully.{W}")
    time.sleep(3) # Let user see the confirmation

except Exception as e:
    print(f"{R}[!] Automation Error: {e}{W}")

finally:
    driver.quit() # Closes the browser

# --- WI-FI ADAPTER RESTART ---
print(f"{Y}[*] Browser closed. Initiating Wi-Fi Cycle...{W}")

# LIVE COUNTDOWN (20 Seconds)
for i in range(20, 0, -1):
    sys.stdout.write(f"\r{Y}[*] Waiting for router shutdown... {i}s {W}")
    sys.stdout.flush()
    time.sleep(1)
print() # New line after countdown finishes

print(f"{Y}[*] Restarting local Wi-Fi adapter to flush connection...{W}")
try:
    # Turns Wi-Fi OFF
    subprocess.run(["nmcli", "radio", "wifi", "off"])
    time.sleep(2)
    # Turns Wi-Fi ON
    subprocess.run(["nmcli", "radio", "wifi", "on"])
    print(f"{G}[+] Local Wi-Fi adapter restarted.{W}")
except Exception as e:
    print(f"{R}[!] Could not restart Wi-Fi (nmcli missing?): {e}{W}")


# --- RECOVERY MONITOR ---
print(f"{Y}[*] Watching for pings (this may take 2-3 minutes)...{W}")

start_time = time.time()
while True:
    if check_ping():
        uptime = time.time() - start_time
        print(f"\n{G}[SUCCESS] Your internet is back online!{W}")
        print(f"{G}[INFO] Recovery took approximately {int(uptime)} seconds.{W}")
        break
    else:
        # Dynamic loading text
        sys.stdout.write(f"\r{Y}[-] Searching for signal...{W}")
        sys.stdout.flush()
        time.sleep(2)

# FINAL SPEED STATS
run_speed_test()