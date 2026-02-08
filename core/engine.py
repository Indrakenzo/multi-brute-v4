import httpx
import asyncio
from colorama import Fore

class JarvisEngine:
    def __init__(self, proxy_mgr):
        self.proxy_mgr = proxy_mgr
        # Konfigurasi client global untuk efisiensi
        self.limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)
        self.timeout = httpx.Timeout(20.0, connect=10.0)

    async def execute_audit(self, client, url, payload, headers):
        """
        Mengeksekusi request menggunakan client session yang sudah ada.
        """
        try:
            # Rotasi proxy dilakukan di level request jika perlu, 
            # tapi untuk session persistent, idealnya satu session = satu proxy.
            # Di sini kita gunakan proxy dari session client.
            
            response = await client.post(url, data=payload, headers=headers)
            return response
        except httpx.RequestError as e:
            # Silent fail untuk connection error agar tidak spam console
            return None
        except Exception as e:
            return None
