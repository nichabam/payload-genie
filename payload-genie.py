import base64
import json
from pathlib import Path

PAYLOADS_PATH = Path(__file__).with_name("payloads.json")
LHOST_TOKEN = "{{LHOST}}"
LPORT_TOKEN = "{{LPORT}}"
PAYLOAD_TOKEN = "{{PAYLOAD}}"


def load_payloads(path=PAYLOADS_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def print_payload(payload):
    print("============================================================================")
    print(payload)
    print("============================================================================")


def get_target():
    ip = input("Local Host IP: ").strip()
    port = input("Local Host Port: ").strip()
    return ip, port


def inject(template, ip, port):
    return template.replace(LHOST_TOKEN, ip).replace(LPORT_TOKEN, port)


def encode_payload(payload, encode=None):
    if encode == "powershell_utf16le":
        return base64.b64encode(payload.encode("utf-16le")).decode("ascii")
    return payload


def wrap_payload(payload, wrap=None):
    if not wrap:
        return payload
    return wrap.replace(PAYLOAD_TOKEN, payload)


def choose_option(options, prompt="Enter option number: "):
    for index, label in enumerate(options, start=1):
        print(f"{index}. {label}")
    choice = input(prompt).strip()
    if not choice.isdigit():
        return None
    index = int(choice)
    if index < 1 or index > len(options):
        return None
    return index - 1


def generate_payload(entry):
    ip, port = get_target()
    payload = inject(entry["template"], ip, port)
    payload = encode_payload(payload, entry.get("encode"))
    payload = wrap_payload(payload, entry.get("wrap"))
    print(f"Generating {entry['name']}...")
    print_payload(payload)


def select_payload(category):
    print(f"Selected {category['name']}!")
    payloads = category["payloads"]
    index = choose_option([p["name"] for p in payloads])
    if index is None:
        print("Unsupported option!")
        return
    generate_payload(payloads[index])


def loop(categories):
    print("Payload Options:")
    index = choose_option([c["name"] for c in categories] + ["Quit"])
    if index is None:
        print("Unsupported option!")
        return True
    if index == len(categories):
        return False
    select_payload(categories[index])
    return True


def main():
    art = r"""
    ⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢸⣿⠟⠋⣉⣉⠙⠻⣿⡇⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠉⢠⣾⣿⣿⣷⡄⠉⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⣀⣤⡄⠘⣿⣿⣿⣿⠃⢠⣤⣄⡀⠀⠀⠀
    ⠀⢀⣴⣿⣿⣿⣿⣦⣈⠉⠉⣁⣴⣿⣿⣿⣿⣷⣄⠀    ██████╗  █████╗ ██╗   ██╗██╗      ██████╗  █████╗ ██████╗        ██████╗ ███████╗███╗   ██╗██╗███████╗
    ⠀⣾⣿⣿⣿⡿⠛⠛⠛⠛⠛⠛⠛⠛⢿⣿⣿⣿⣿⣧    ██╔══██╗██╔══██╗╚██╗ ██╔╝██║     ██╔═══██╗██╔══██╗██╔══██╗      ██╔════╝ ██╔════╝████╗  ██║██║██╔════╝
    ⢸⣿⣿⣿⣿⣷⣤⣤⣤⡄⢠⣤⣤⣤⣾⣿⣿⣿⣿⣿    ██████╔╝███████║ ╚████╔╝ ██║     ██║   ██║███████║██║  ██║█████╗██║  ███╗█████╗  ██╔██╗ ██║██║█████╗
    ⠀⢻⣿⣿⣿⣿⣿⣿⡿⠁⠀⢻⣿⣿⣿⣿⣿⣿⣿⠏    ██╔═══╝ ██╔══██║  ╚██╔╝  ██║     ██║   ██║██╔══██║██║  ██║╚════╝██║   ██║██╔══╝  ██║╚██╗██║██║██╔══╝
    ⠀⠀⠙⠻⠿⠿⠟⠛⢁⣼⣷⣄⠙⠛⠿⠿⠿⠟⠁⠀    ██║     ██║  ██║   ██║   ███████╗╚██████╔╝██║  ██║██████╔╝      ╚██████╔╝███████╗██║ ╚████║██║███████╗
    ⠀⠀⠀⠀⠠⣤⣶⣾⣿⣿⣿⣿⣿⣶⣶⠀⠀⠀⠀⠀    ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝        ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚══════╝
    ⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣄⡀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⢿⣿⣿⣿⣿⣷⠄
    """
    print(art)
    categories = load_payloads()["categories"]
    while loop(categories):
        pass


if __name__ == "__main__":
    main()
