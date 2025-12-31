def get_config():
    return {
        "url": "https://m.facebook.com/login/device-based/login/async/",
        "platform": "facebook"
    }

def get_payload(username, password):
    # Payload standar untuk m.facebook
    return {
        "email": username,
        "pass": password,
        "login": "Log In",
        "format": "json"
    }
