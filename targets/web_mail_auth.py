def get_config():
    url = input("[INPUT] Masukkan URL Login (Tipe Email): ")
    return {"url": url, "platform": "web_generic"}

def get_payload(username, password):
    # Memastikan format email valid sebelum mengirim
    if "@" not in username:
        print(f"[WARN] Target {username} bukan format email! Menambahkan @gmail.com dummy...")
        username = f"{username}@gmail.com"
        
    return {
        "email": username,  # Field umum: email, user_email, mail
        "password": password,
        "login": "submit"
    }
