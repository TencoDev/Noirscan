# main.py - modified version
import argparse
import time
from datetime import datetime
from colorama import Fore, Style, init
from models import ScrapedPage
from crawler import crawl
from utils import clear_screen, print_crawl_start, print_page_results, save_pages

def main():
    parser = argparse.ArgumentParser(
        prog='Dark Web Crawler',
        description='Crawls surface web and dark web using TOR and SOCKS5H',
        epilog='⚠️ You are responsible for what you do with this tool.'
    )

    parser.add_argument('--url', '-u', required=True, help='URL of the site you want to crawl (REQUIRED)')
    parser.add_argument('--save', '-s', action='store_true', help='Save output to .json file')
    parser.add_argument('--depth', '-d', type=int, default=0, help='Depth of crawling (default: 0)')

    args = parser.parse_args()
    init(autoreset=True)
    
    url = args.url
    max_depth = args.depth
    save_files = args.save

    print("Booting program...")
    time.sleep(0.5)

    start_time = datetime.now()
    print_crawl_start(url, start_time.strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(0.5)

    page_results = crawl(url, depth=0, max_depth=max_depth)

    print("Crawling finished. Clearing screen...")
    time.sleep(0.5)
    clear_screen()

    results_displayed = print_page_results(page_results)
    
    files_saved = False
    if save_files and results_displayed:
        files_saved = save_pages(page_results)

    print("=" * 130)
    print(Fore.MAGENTA + "Dark web crawl finished at: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    if files_saved:
        print(Fore.GREEN + "✅ All files saved successfully in './output/<date>/' folder.")
    print(Fore.BLUE + Style.BRIGHT + "\n✔️  Dark web crawler execution completed.\n")

if __name__ == "__main__":
    main()