import httpx
import asyncio

class JarvisEngine:
    def __init__(self, proxy_mgr):
        self.proxy_mgr = proxy_mgr

    async def execute_audit(self, url, payload, headers):
        proxy = self.proxy_mgr.get_proxy()
        self.proxy_mgr.increment()
        
        async with httpx.AsyncClient(proxies=proxy, http2=True, timeout=15) as client:
            try:
                response = await client.post(url, data=payload, headers=headers)
                return response
            except Exception as e:
                return None
