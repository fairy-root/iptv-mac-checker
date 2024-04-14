# IPTV Mac Address Checker

## Overview
This Python script, `maccheck.py`, is designed to generate a list of IPTV Mac addresses and make requests to the server to retrieve information such as subscription expiry and the number of channels associated with each Mac address. It offers the functionality to provide a starting Mac address and continue checking the list from there.

## Features
- Generates Mac address combinations
- Makes HTTP requests to retrieve subscription and channel information
- Allows starting from a specific Mac address
- Handles interruptions gracefully

## Requirements
- Python 3.x
- requests library (`pip install requests`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/fairy-root/iptv-mac-checker.git
   cd iptv-mac-checker
   ```
2. Install dependencies:
   ```bash
   pip install requests
   ```

## Usage
1. Run the script:
   ```bash
   python maccheck.py
   ```
2. Follow the prompts to enter the IPTV link and optionally a starting Mac address.
3. The script will start generating Mac addresses, making requests, and displaying the results.

## Example
```bash
Enter IPTV link: http://example.com
Enter a full MAC address to start from or press Enter to start from beginning: 00:1A:79:01:23:45
```

## Note
- Ensure the IPTV link is accessible and correctly formatted.
- Starting from a specific Mac address is optional.
- Interrupting the script (e.g., with Ctrl+C) will gracefully exit the process.

## Donation

Your support is appreciated:

- USDt (TRC20): `TGCVbSSJbwL5nyXqMuKY839LJ5q5ygn2uS`
- BTC: `13GS1ixn2uQAmFQkte6qA5p1MQtMXre6MT`
- ETH (ERC20): `0xdbc7a7dafbb333773a5866ccf7a74da15ee654cc`
- LTC: `Ldb6SDxUMEdYQQfRhSA3zi4dCUtfUdsPou`


## Contributing

If you have suggestions or improvements, please fork the repository and create a pull request or open an issue.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.