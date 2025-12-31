from core.headers import HeaderGenerator

def get_payload(username, password):
    return {
        "params": f'{{"client_input_params":{{"username":"{username}","password":"{password}"}}}}',
        "bk_client_context": '{"bloks_version":"..."}'
    }

def get_config():
    return {
        "url": "https://i.instagram.com/api/v1/accounts/login/",
        "platform": "instagram"
    }
