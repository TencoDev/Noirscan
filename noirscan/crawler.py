from config import USER_AGENTS, DEFAULT_TIMEOUT
from models import ScrapedPage
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import is_onion, clean_title
from network import get_ip_address, get_geolocation

class Crawler:
    def __init__(
        self,
        tor_proxies: dict,
        user_agent: str = None,
        max_depth: int = 0,
        ignore_robots: bool = False
        ):
        
        self.tor_proxies = tor_proxies
        self.user_agent = user_agent or random.choice(USER_AGENTS)
        self.max_depth = max_depth
        self.ignore_robots = ignore_robots
        self.visited = set()

    def scrape(self, url: str):
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(
                url, proxies=self.tor_proxies, headers=headers, timeout=DEFAULT_TIMEOUT
            )
            status_code = response.status_code
            soup = BeautifulSoup(response.text, "html.parser")

            raw_title = soup.title.string if soup.title else "NONE"
            title = clean_title(raw_title)
            html = str(soup.body) if soup.body else str(soup)
            links = [urljoin(url, tag['href']) for tag in soup.find_all("a", href=True)]
            ip_address = "N/A"
            geolocation = "N/A"
            if not is_onion(url):
                ip_address = get_ip_address(url)
                geolocation = get_geolocation(ip_address)

            return ScrapedPage(url, title, html, status_code, links, ip_address, geolocation)

        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None

    def crawl(self, url: str, depth: int = 0):
        if depth > self.max_depth or url in self.visited:
            return []

        self.visited.add(url)
        result = []

        page = self.scrape(url)
        if page:
            result.append(page)
            if depth < self.max_depth:
                for link in page.get_links():
                    if link.startswith("http"):
                        result.extend(self.crawl(link, depth + 1))
        return result