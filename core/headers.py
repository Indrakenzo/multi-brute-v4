import random
from fake_useragent import UserAgent

class HeaderGenerator:
    @staticmethod
    def get_headers(platform):
        ua = UserAgent()
        base_headers = {"User-Agent": ua.random, "Accept-Language": "en-US,en;q=0.9"}
        
        configs = {
            "instagram": {
                "X-IG-App-ID": "936619743392459",
                "X-ASBD-ID": "129477",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "facebook": {
                "X-FB-LSD": "AVpHp_0E",
                "X-ASBD-ID": "129477"
            },
            "web_generic": {
                "Referer": "https://google.com"
            }
        }
        return {**base_headers, **configs.get(platform, {})}
