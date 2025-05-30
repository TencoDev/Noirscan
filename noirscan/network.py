
import requests, socket

# Sets SOCKS5H port path
def get_tor_proxies(port: str):
    return {
        'http': f'socks5h://127.0.0.1:{port}',
        'https': f'socks5h://127.0.0.1:{port}',
    }
    
# Checks if TOR is running, defaults to port 9050
def is_tor_running(host='127.0.0.1', port=9050, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

# Fetches ip_address of the target url if not an .onion website
def get_ip_address(url: str):
    try:
        domain = url.split('/')[2]
        if domain.endswith(".onion"):
            return "N/A"
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except Exception:
        return "N/A"
 
# Fetches geolocation of the target if ip_address exists   
def get_geolocation(ip_address: str):
    if not ip_address or ip_address == "N/A":
        return "N/A"

    try:
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url)

        if response.status_code != 200:
            return "N/A"

        data = response.json()
        location = {
            'ip': data.get('ip', 'Not Found'),
            'city': data.get('city', 'Not Found'),
            'region': data.get('region', 'Not Found'),
            'country': data.get('country', 'Not Found'),
            'location': data.get('loc', 'Not Found') 
        }

        return location
    except requests.exceptions.RequestException:
        return "N/A"