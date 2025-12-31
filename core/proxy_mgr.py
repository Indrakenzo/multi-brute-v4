class ProxyManager:
    def __init__(self, proxy_list):
        self.proxies = proxy_list
        self.index = 0
        self.hit_count = 0

    def get_proxy(self):
        if not self.proxies: return None
        
        # Rotasi otomatis setiap 3 kali percobaan
        if self.hit_count >= 3:
            self.index = (self.index + 1) % len(self.proxies)
            self.hit_count = 0
            print(f"\n[!] SYSTEM: Rotasi IP ke -> {self.proxies[self.index]}")
            
        return {"http://": self.proxies[self.index], "https://": self.proxies[self.index]}

    def increment(self):
        self.hit_count += 1
