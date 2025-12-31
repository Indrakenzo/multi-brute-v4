import httpx
import random

class ProxyManager:
    def __init__(self, proxy_list):
        self.proxies = proxy_list
        self.current_index = 0
        self.attempts = 0

    def get_proxy(self):
        # Logika Otomatis Ganti tiap 3 percobaan
        if self.attempts >= 3:
            self.current_index = (self.current_index + 1) % len(self.proxies)
            self.attempts = 0
            print(f"[!] SYSTEM: Rotating IP to -> {self.proxies[self.current_index]}")
        
        proxy_url = self.proxies[self.current_index]
        return {"http://": proxy_url, "https://": proxy_url}

    def mark_attempt(self):
        self.attempts += 1
