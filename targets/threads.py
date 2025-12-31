def get_config():
    return {
        "url": "https://www.threads.net/api/v1/bloks/apps/com.bloks.www.bloks.threads.login/",
        "platform": "threads"
    }

def get_payload(username, password):
    # Struktur JSON params yang dibungkus string (Bloks Framework)
    return {
        "params": f'{{"client_input_params":{{"username":"{username}","password":"{password}"}}, "server_params":{{"credential_type":"password"}}}}',
        "bk_client_context": '{"bloks_version":"85f67073f15598696803272995250493608144081395804550742514120286d5"}'
    }
