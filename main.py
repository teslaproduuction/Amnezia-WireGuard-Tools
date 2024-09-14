# main.py
import base64
import random
import re
import socket
from io import BytesIO
import qrcode
from nicegui import ui
import json
def load_config(file_content):
    return file_content

def generate_random_params():
    return [
        f"Jc = {random.randint(10, 40)}",
        f"Jmin = {random.randint(5, 15)}",
        f"Jmax = {random.randint(35, 45)}",
        "S1 = 0",
        "S2 = 0",
        "H1 = 1",
        "H2 = 2",
        "H3 = 3",
        "H4 = 4"
    ]

def extract_params(config):
    interface_match = re.search(r'\[Interface\](.*?)(?=\[Peer\]|\Z)', config, re.DOTALL)
    peer_match = re.search(r'\[Peer\](.*)', config, re.DOTALL)

    interface = interface_match.group(1) if interface_match else ""
    peer = peer_match.group(1) if peer_match else ""

    wgListenPort = re.search(r'ListenPort\s*=\s*(\d+)', interface)
    wgIP = re.search(r'Endpoint\s*=\s*([0-9a-fA-F.]+)', peer)
    wgPORT = re.search(r':(\d+)', peer)

    return {
        'wgListenPort': int(wgListenPort.group(1)) if wgListenPort else None,
        'wgIP': wgIP.group(1) if wgIP else None,
        'wgPORT': int(wgPORT.group(1)) if wgPORT else None
    }


def convert_to_amnezia(config):
    # Проверяем, является ли входной конфиг JSON
    try:
        json_config = json.loads(config)
        # Если это JSON, преобразуем его в обычный WireGuard конфиг
        config = json_to_wireguard(json_config)
    except json.JSONDecodeError:
        # Если это не JSON, продолжаем с исходным конфигом
        pass

    interface_match = re.search(r'\[Interface\](.*?)(?=\[Peer\]|\Z)', config, re.DOTALL)
    peer_match = re.search(r'\[Peer\](.*)', config, re.DOTALL)

    interface = interface_match.group(1) if interface_match else ""
    peer = peer_match.group(1) if peer_match else ""

    additional_params = generate_random_params()
    params_dict = {param.split('=')[0].strip(): param for param in additional_params}

    interface_lines = interface.split('\n')
    new_interface_lines = []
    found_params = set()

    for line in interface_lines:
        if any(line.startswith(param_name) for param_name in params_dict.keys()):
            param_name = line.split('=')[0].strip()
            new_interface_lines.append(params_dict[param_name])
            found_params.add(param_name)
        else:
            new_interface_lines.append(line)

    for param_name, param_line in params_dict.items():
        if param_name not in found_params:
            new_interface_lines.append(param_line)

    interface = '\n'.join(new_interface_lines)

    if not re.search(r'AllowedIPs\s*=', peer):
        peer += '\nAllowedIPs = 0.0.0.0/1, 128.0.0.0/1, ::/1, 8000::/1'

    if 'PersistentKeepalive' not in peer:
        peer += '\nPersistentKeepalive = 25\n'

    return f'[Interface]\n{interface.strip()}\n[Peer]\n{peer.strip()}'


def json_to_wireguard(json_config):
    """Преобразует JSON-конфигурацию в формат WireGuard."""
    wireguard_config = "[Interface]\n"
    outbound = json_config.get("outbounds", [{}])[0]
    wireguard_config += f"PrivateKey = {outbound.get('private_key', '')}\n"
    wireguard_config += f"Address = {outbound.get('local_address', '')}\n"
    wireguard_config += f"DNS = 1.1.1.1 \n"
    wireguard_config += "\n[Peer]\n"
    wireguard_config += f"PublicKey = {outbound.get('peer_public_key', '')}\n"
    wireguard_config += f"Endpoint = {outbound.get('server', '')}:{outbound.get('server_port', '')}\n"
    wireguard_config += "AllowedIPs = 0.0.0.0/0, ::/0\n"

    return wireguard_config

def send_udp_message(config):
    params = extract_params(config)
    if not all(params.values()):
        ui.notify('Параметры не найдены в конфигурации', type='warning')
        return

    wgListenPort = params['wgListenPort']
    wgIP = params['wgIP']
    wgPORT = params['wgPORT']

    try:
        endpoint = (wgIP, wgPORT)
        message = b':)'
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', wgListenPort))
            sock.sendto(message, endpoint)
        ui.notify('Сообщение отправлено успешно', type='success')
    except Exception as e:
        ui.notify(f'Ошибка при отправке сообщения: {e}', type='error')

def add_random_listen_port(config):
    interface_match = re.search(r'\[Interface\](.*?)(?=\[Peer\]|\Z)', config, re.DOTALL)

    if interface_match:
        interface = interface_match.group(1)
        if 'ListenPort' not in interface:
            random_port = random.randint(1024, 65535)
            updated_interface = f'\n{interface.strip()}\nListenPort = {random_port}\n'
            config = config.replace(interface, updated_interface)
            ui.notify(f'Сгенерирован и добавлен ListenPort = {random_port}', type='success')
        else:
            ui.notify('ListenPort уже существует в секции [Interface]', type='info')
    else:
        ui.notify('Секция [Interface] не найдена в конфигурации', type='warning')

    return config

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def convert_to_json(config):
    interface_match = re.search(r'\[Interface\](.*?)(?=\[Peer\]|\Z)', config, re.DOTALL)
    peer_match = re.search(r'\[Peer\](.*)', config, re.DOTALL)

    if not interface_match or not peer_match:
        return None

    interface = interface_match.group(1)
    peer = peer_match.group(1)

    private_key = re.search(r'PrivateKey\s*=\s*(\S+)', interface)
    address = re.search(r'Address\s*=\s*(\S+)', interface)
    endpoint = re.search(r'Endpoint\s*=\s*(\S+)', peer)
    public_key = re.search(r'PublicKey\s*=\s*(\S+)', peer)

    if not all([private_key, address, endpoint, public_key]):
        return None

    server, port = endpoint.group(1).split(':')
    local_address = address.group(1)

    json_config = {
        "outbounds": [
            {
                "type": "wireguard",
                "tag": "WARP § 0",
                "local_address": local_address,
                "private_key": private_key.group(1),
                "server": server,
                "server_port": int(port),
                "peer_public_key": public_key.group(1),
                "mtu": 1420,
                "fake_packets": "40-80",
                "fake_packets_size": "40-100",
                "fake_packets_delay": "4-8",
                "fake_packets_mode": "m4"
            }
        ]
    }

    return json.dumps(json_config, ensure_ascii=False, indent=2)