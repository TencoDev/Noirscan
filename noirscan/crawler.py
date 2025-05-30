from config import USER_AGENTS, DEFAULT_TIMEOUT
from models import ScrapedPage
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import *
from network import *

# Single page scraping
def scrape(url: str, tor_proxies: dict):
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, proxies=tor_proxies, headers=headers, timeout=DEFAULT_TIMEOUT)
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
        print(e)

visited = set()

def crawl(url, tor_proxies, depth=0, max_depth=0):
    if depth > max_depth or url in visited:
        return []

    visited.add(url)
    result = []

    page = scrape(url, tor_proxies)
    if page:
        result.append(page)

        if depth < max_depth:
            for link in page.get_links():
                if link.startswith("http") or link.startswith("https"):
                    result.extend(crawl(link, depth + 1, max_depth))

    return result
