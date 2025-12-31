import random
from fake_useragent import UserAgent

class HeaderGenerator:
    @staticmethod
    def get_headers(platform):
        ua = UserAgent()
        base_headers = {
            "User-Agent": ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }
        
        configs = {
            "instagram": {
                "X-IG-App-ID": "936619743392459",
                "X-IG-WWW-Claim": "0",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "threads": {
                "X-IG-App-ID": "238280545333740", # App ID Threads berbeda
                "X-ASBD-ID": "129477",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "facebook": {
                "X-FB-LSD": "AVpHp_0E",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://m.facebook.com/"
            },
            "gmail": {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest" # Simulasi AJAX request
            },
            "web_generic": {
                "Cache-Control": "max-age=0",
                "Upgrade-Insecure-Requests": "1"
            }
        }
        return {**base_headers, **configs.get(platform, {})}
