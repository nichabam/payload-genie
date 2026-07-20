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


def get_template(entry):
    if "template" in entry:
        return entry["template"]
    if "path" in entry:
        path = PAYLOADS_PATH.parent / entry["path"]
        if not path.is_file():
            raise FileNotFoundError(f"Template file not found: {path}")
        return path.read_text(encoding="utf-8")
    raise ValueError(f"Payload '{entry.get('name', 'unknown')}' has no template or path")


def requires_target(entry, template):
    if "requires_target" in entry:
        return entry["requires_target"]
    return LHOST_TOKEN in template or LPORT_TOKEN in template


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
    try:
        template = get_template(entry)
    except (FileNotFoundError, ValueError) as exc:
        print(exc)
        return

    if requires_target(entry, template):
        ip, port = get_target()
        payload = inject(template, ip, port)
    else:
        payload = template

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
