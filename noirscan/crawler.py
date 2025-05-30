from config import TOR_PROXIES, USER_AGENTS, DEFAULT_TIMEOUT
from models import ScrapedPage
import requests
import socket
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def is_onion(url):
    return ".onion" in url

def clean_title(title):
    return re.sub(r'\s+', ' ', title).strip()

def get_ip_address(url):
    try:
        domain = url.split('/')[2]
        if domain.endswith(".onion"):
            return "N/A"
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except Exception:
        return None
    
def get_geolocation(ip_address):
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

# Single page scraping
def scrape(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, proxies=TOR_PROXIES, headers=headers, timeout=DEFAULT_TIMEOUT)
        status_code = response.status_code
        soup = BeautifulSoup(response.text, "html.parser")

        raw_title = soup.title.string if soup.title else "NONE"
        title = clean_title(raw_title)

        # Save HTML content (cleaned but retains structure)
        html = str(soup.body) if soup.body else str(soup)

        # Resolve all links (absolute or relative)
        links = [urljoin(url, tag['href']) for tag in soup.find_all("a", href=True)]

        ip_address = "N/A"
        geolocation = "N/A"

        if not is_onion(url):
            ip_address = get_ip_address(url)
            geolocation = get_geolocation(ip_address)

        page = ScrapedPage(url, title, html, status_code, links, ip_address, geolocation)
        return page

    except requests.RequestException as e:
        return None

visited = set()

def crawl(url, depth=0, max_depth=0):
    if depth > max_depth or url in visited:
        return []

    visited.add(url)
    result = []

    page = scrape(url)
    if page:
        result.append(page)

        if depth < max_depth:
            for link in page.get_links():
                if link.startswith("http") or link.startswith("https"):
                    result.extend(crawl(link, depth + 1, max_depth))

    return result
