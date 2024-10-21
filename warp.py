import json
import os

import httpx
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# Default SOCKS5 proxy configuration (not to be shown to the user)
DEFAULT_SOCKS5_PROXY = {
    'host': '161.97.163.52',
    'port': 60316,
    'username': 'vpn',
    'password': 'vpn'
}

# User-defined SOCKS5 proxy configuration
USER_SOCKS5_PROXY = {
    'host': '',
    'port': '',
    'username': '',
    'password': ''
}

def load_user_proxy_settings():
    if os.path.exists('user_proxy_settings.json'):
        with open('user_proxy_settings.json', 'r') as f:
            return json.load(f)
    return USER_SOCKS5_PROXY

def save_user_proxy_settings(settings):
    with open('user_proxy_settings.json', 'w') as f:
        json.dump(settings, f)

USER_SOCKS5_PROXY = load_user_proxy_settings()

def get_active_proxy():
    return {k: v for k, v in USER_SOCKS5_PROXY.items() if v} or DEFAULT_SOCKS5_PROXY

def create_socks5_client():
    active_proxy = get_active_proxy()
    proxies = {
        "http://": f"socks5://{active_proxy['username']}:{active_proxy['password']}@{active_proxy['host']}:{active_proxy['port']}",
        "https://": f"socks5://{active_proxy['username']}:{active_proxy['password']}@{active_proxy['host']}:{active_proxy['port']}"
    }
    client = httpx.Client(proxies=proxies)
    return client


def generate_wgcf_config() -> Optional[str]:
    api_version = "v0a884"
    api = f"https://api.cloudflareclient.com/{api_version}"
    reg_url = f"{api}/reg"

    def get_timestamp() -> str:
        timestamp = datetime.now(tz=timezone.utc).astimezone(None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        timestamp = timestamp[:-10] + timestamp[-6:]
        timestamp = timestamp[:-2] + ":" + timestamp[-2:]
        return timestamp

    def gen_keys() -> Dict[str, str]:
        private_key = subprocess.run(["wg", "genkey"], capture_output=True).stdout.decode('utf-8').strip()
        public_key = subprocess.run(["wg", "pubkey"], input=bytes(private_key, 'utf-8'),
                                    capture_output=True).stdout.decode('utf-8').strip()
        return {"private_key": private_key, "public_key": public_key}

    def register(pub_key: str, use_proxy: bool = False) -> Optional[Dict[str, Any]]:
        data = {
            "install_id": "",
            "tos": get_timestamp(),
            "key": pub_key,
            "fcm_token": "",
            "type": "Android",
            "model": "PC",
            "locale": "en_US"
        }
        headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1",
            "Content-Type": "application/json; charset=UTF-8"
        }

        try:
            if use_proxy:
                client = create_socks5_client()
                response = client.post(reg_url, json=data, headers=headers, timeout=10)
            else:
                response = httpx.post(reg_url, json=data, headers=headers, timeout=10)

            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            return None

    def get_config(account_id: str, access_token: str, use_proxy: bool = False) -> Optional[Dict[str, Any]]:
        headers = {
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1",
            "Authorization": f"Bearer {access_token}"
        }

        try:
            if use_proxy:
                client = create_socks5_client()
                response = client.get(f"{reg_url}/{account_id}", headers=headers, timeout=10)
            else:
                response = httpx.get(f"{reg_url}/{account_id}", headers=headers, timeout=10)

            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting config: {str(e)}")
            return None

    keys = gen_keys()

    # Try direct connection
    account_data = register(keys['public_key'])
    if account_data is None:
        # Try with proxy
        account_data = register(keys['public_key'], use_proxy=True)

    if account_data is None:
        return None  # Both attempts failed

    # Try direct connection for config
    config_data = get_config(account_data['id'], account_data['token'])
    if config_data is None:
        # Try with proxy
        config_data = get_config(account_data['id'], account_data['token'], use_proxy=True)

    if config_data is None:
        return None  # Both attempts failed

    addresses = config_data['config']['interface']['addresses']
    peer = config_data['config']['peers'][0]

    wireguard_conf = f"""
[Interface]
PrivateKey = {keys['private_key']}
DNS = 1.1.1.1
Address = {addresses['v4']}/24

[Peer]
PublicKey = {peer['public_key']}
AllowedIPs = 0.0.0.0/0
AllowedIPs = ::/0
Endpoint = 188.114.97.171:7152
"""

    return wireguard_conf  # Return the configuration
