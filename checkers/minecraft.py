import json
import socket
import struct

def colorize_text(color, text):
    ansi_colors = {
        'black': '\033[30m',        # Black
        'dark_blue': '\033[34m',    # Dark Blue
        'dark_green': '\033[32m',   # Dark Green
        'dark_aqua': '\033[36m',    # Dark Aqua (Cyan)
        'dark_red': '\033[31m',     # Dark Red
        'dark_purple': '\033[35m',  # Dark Purple
        'gold': '\033[33m',         # Gold (Yellow)
        'gray': '\033[37m',         # Gray
        'dark_gray': '\033[90m',    # Dark Gray
        'blue': '\033[94m',         # Light Blue
        'green': '\033[92m',        # Light Green
        'aqua': '\033[96m',         # Aqua (Cyan)
        'red': '\033[91m',          # Light Red
        'light_purple': '\033[95m', # Light Purple (Magenta)
        'yellow': '\033[93m',       # Yellow
        'white': '\033[97m',        # White
        'reset': '\033[0m'          # Reset to default
    }
    return f"{ansi_colors.get(color, '')}{text}{ansi_colors['reset']}"

def format_mini_message(message, colorize=True):
    formatted_parts = []
    for part in message['extra']:
        color = part['color']
        text = part['text']
        if colorize:
            formatted_parts.append(colorize_text(color, text))
        else:
            formatted_parts.append(text)
    return ''.join(formatted_parts)

def get_minecraft_server_info(host='localhost', port=25565):
    def read_var_int():
        i = 0
        j = 0
        while True:
            k = sock.recv(1)
            if not k:
                return 0
            k = k[0]
            i |= (k & 0x7f) << (j * 7)
            j += 1
            if j > 5:
                raise ValueError('var_int too big')
            if not (k & 0x80):
                return i

    sock = socket.socket()
    sock.connect((socket.gethostbyname(host), port))
    try:
        host = socket.gethostbyname(host).encode('utf-8')
        data = b''  # wiki.vg/Server_List_Ping
        data += b'\x00'  # packet ID
        data += b'\x04'  # protocol variant
        data += struct.pack('>b', len(host)) + host
        data += struct.pack('>H', port)
        data += b'\x01'  # next state
        data = struct.pack('>b', len(data)) + data
        sock.sendall(data + b'\x01\x00')  # handshake + status ping
        length = read_var_int()  # full packet length
        if length < 10:
            if length < 0:
                raise ValueError('negative length read')
            else:
                raise ValueError('invalid response %s' % sock.read(length))

        sock.recv(1)  # packet type, 0 for pings
        length = read_var_int()  # string length
        data = b''
        while len(data) != length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                raise ValueError('connection abborted')

            data += chunk
        data = json.loads(data.decode())
        return data
    finally:
        sock.close()
