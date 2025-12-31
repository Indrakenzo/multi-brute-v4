import asyncio
import httpx
from .proxy_mgr import ProxyManager

class JarvisEngine:
    def __init__(self, proxy_list):
        self.pm = ProxyManager(proxy_list)

    async def send_request(self, target_url, payload, headers):
        proxy = self.pm.get_proxy()
        async with httpx.AsyncClient(proxies=proxy, verify=False, http2=True) as client:
            try:
                response = await client.post(target_url, data=payload, headers=headers)
                self.pm.mark_attempt() # Hitung attempt untuk rotasi IP
                return response
            except Exception as e:
                print(f"[ERROR] Connection Failed: {e}")
                self.pm.mark_attempt()
                return None
