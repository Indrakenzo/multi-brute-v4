def get_config():
    url = input("[INPUT] Masukkan URL Login (Tipe Username/ID): ")
    return {"url": url, "platform": "web_generic"}

def get_payload(username, password):
    return {
        "username": username, # Field umum: username, user, id, login_id
        "password": password,
        "submit": "true"
    }
