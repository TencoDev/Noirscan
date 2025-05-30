# main.py - modified version
import argparse
from datetime import datetime
from colorama import Fore, Style, init
from crawler import Crawler
from utils import *
from network import *

def main():
    
    # Parser object to handle CLI
    parser = argparse.ArgumentParser(
        prog='Dark Web Crawler',
        description='Crawls surface web and dark web using TOR and SOCKS5H',
        epilog='⚠️ You are responsible for what you do with this tool.'
    )

    # Handles flag inputs from CLI
    parser.add_argument('--url', '-u', required=True, help='URL of the site you want to crawl (REQUIRED)')
    parser.add_argument('--save', '-s', action='store_true', help='Save output to .json file')
    parser.add_argument('--depth', '-d', type=int, default=0, help='Depth of crawling (default: 0)')
    parser.add_argument('--tor-port', '-tp', type=int, default=9050, help='Tor SOCKS5 proxy port (default: 9050)')
    parser.add_argument('--user-agent', '-ua', type=str, help='Manually set user agent (default: chosen automatically)')
    parser.add_argument('--ignore-robots', type=bool, default=False, help='Toggle interaction with robot.txt (default: False)')

    args = parser.parse_args()
    init(autoreset=True)
    
    # Store CLI arguments
    url = args.url
    max_depth = args.depth
    save_files = args.save
    tor_port = args.tor_port
    user_agent = args.user_agent
    ignore_robots = args.ignore_robots

    # Check if TOR is running
    if not is_tor_running(port=tor_port):
        print(f"❌ Tor is not running on default port {tor_port}! Please start Tor or specify the correct port using --tor-port.")
        exit(1)
        
    tor_proxies = get_tor_proxies(tor_port)
    
    # Start crawling and store it as list[ScrapedPage]
    crawler = Crawler(
    tor_proxies=tor_proxies,
    user_agent=user_agent,
    max_depth=max_depth,
    ignore_robots=ignore_robots,
    )
    page_results = crawler.crawl(url)
    
    results_displayed = print_page_results(page_results)
    
    files_saved = False
    if save_files and results_displayed:
        files_saved = save_pages(page_results)

    print(Fore.MAGENTA + "Dark web crawl finished at: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    if files_saved:
        print(Fore.GREEN + "✅ All files saved successfully in './output/<date>/' folder.")
    print(Fore.BLUE + Style.BRIGHT + "\n✔️  Dark web crawler execution completed.\n")

if __name__ == "__main__":
    main()