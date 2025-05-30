from config import USER_AGENTS, DEFAULT_TIMEOUT
from models import ScrapedPage
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import is_onion, clean_title
from network import get_ip_address, get_geolocation
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

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
        self.robots_cache = {}
    
    # To check if given URL is ethically safe to crawl based on robots.txt
    def is_allowed_by_robots(self, url: str) -> bool:
        if self.ignore_robots:
            return True

        parsed = urlparse(url)
        domain = parsed.netloc
        robots_url = urljoin(f"{parsed.scheme}://{domain}", "/robots.txt")
        if domain in self.robots_cache:
            rp = self.robots_cache[domain]
        else:
            rp = RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
            except Exception as e:
                print(f"robots.txt fetch failed for {robots_url}: {e}")
                self.robots_cache[domain] = rp  # Cache anyway (default allows all)
                return True
            self.robots_cache[domain] = rp
        return rp.can_fetch(self.user_agent, url)

    # Handles scraping of one single page
    def scrape(self, url: str):
        if not self.is_allowed_by_robots(url):
            print(f"Blocked by robots.txt: {url}")
            return None
        
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

    # Handles scraping of multiple pages using recursion
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