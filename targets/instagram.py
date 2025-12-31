def get_config():
    return {
        "url": "https://i.instagram.com/api/v1/accounts/login/",
        "platform": "instagram"
    }

# [FIX] Nama fungsi diubah dari 'get_ig_payload' menjadi 'get_payload'
# agar dikenali oleh main.py
def get_payload(username, password):
    return {
        "params": f'{{"client_input_params":{{"username":"{username}","password":"{password}"}}}}',
        "bk_client_context": '{"bloks_version":"85f67073f15598696803272995250493608144081395804550742514120286d5"}'
    }

def get_config():
    return {
        "url": "https://i.instagram.com/api/v1/accounts/login/",
        "platform": "instagram"
    }
