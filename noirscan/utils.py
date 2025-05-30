# utils.py
import os
import re
from colorama import Fore, Style
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def sanitize_filename(filename):
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def print_crawl_start(url, timestamp):
    print(Fore.YELLOW + Style.BRIGHT + "Dark web crawler has booted up")
    print(f"Crawling started at: {timestamp}")
    print("Crawling given URL... 🌀")

def print_page_results(page_results):
    print(Fore.YELLOW + Style.BRIGHT + "Result Summary")
    print("=" * 130)

    if not isinstance(page_results, list) or not page_results:
        print(Fore.RED + "❌ No valid pages found or crawling failed.\n")
        print("Possible reasons:")
        print("- Invalid or unreachable URL")
        print("- TOR proxy not running")
        print("- Empty page or no links found")
        return False

    for page in page_results:
        print(Fore.GREEN + f"🌐 Page Title: {page.get_title()}")
        print(Fore.GREEN + f"🔗 URL: {page.get_url()}")
        print(Fore.GREEN + f"📡 Status Code: {page.get_status_code()}")
        print(Fore.GREEN + f"🔎 Links Found: {len(page.get_links())}")
        print(Fore.GREEN + f"🌍 IP Address: {page.get_ip_address()}")
        print(Fore.GREEN + f"📍 Geolocation: {page.get_geolocation()}")
        print("-" * 80)

    return True

def save_pages(page_results):
    if not page_results:
        return False

    date_folder = datetime.now().strftime('%Y-%m-%d')
    output_dir = os.path.join('./output', date_folder)
    os.makedirs(output_dir, exist_ok=True)

    for page in page_results:
        filename = sanitize_filename(f"{page.get_title()}_{page.get_timestamp().strftime('%H-%M-%S')}.json")
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding='utf-8') as file:
            file.write(page.to_json())

        print(Fore.YELLOW + f"📝 Saved: {filepath}")

    return True