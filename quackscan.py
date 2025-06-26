import asyncio
import sys
import os
from colorama import init, Fore, Style

from modules.resolver import resolve_subdomains
from modules.scanner import scan_http
from modules.takeover import detect_takeover
from modules.exporter import export_results

init(autoreset=True)

ASCII = r'''
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣉⡥⠶⢶⣿⣿⣿⣿⣷⣆⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⢡⡞⠁⠀⠀⠤⠈⠿⠿⠿⠿⣿⠀⢻⣦⡈⠻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⠘⡁⠀⢀⣀⣀⣀⣈⣁⣐⡒⠢⢤⡈⠛⢿⡄⠻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠉⠐⠄⡈⢀⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠇⢠⣿⣿⣿⣿⡿⢿⣿⣿⣿⠁⢈⣿⡄⠀⢀⣀⠸⣿⣿⣿⣿ 
⣿⣿⣿⣿⡿⠟⣡⣶⣶⣬⣭⣥⣴⠀⣾⣿⣿⣿⣶⣾⣿⣧⠀⣼⣿⣷⣌⡻⢿⣿
⣿⣿⠟⣋⣴⣾⣿⣿⣿⣿⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⣷⠄⢻
⡏⠰⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢂⣭⣿⣿⣿⣿⣿⠇⠘⠛⠛⢉⣉⣠⣴⣾
⣿⣷⣦⣬⣍⣉⣉⣛⣛⣉⠉⣤⣶⣾⣿⣿⣿⣿⣿⣿⡿⢰⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡘⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣿⣿⣿⣿⣿⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿ Made by No Corazón
'''

async def main():
    print(Fore.CYAN + ASCII + Style.RESET_ALL)

    domain = input(Fore.YELLOW + "Enter target domain (ex: example.com): ").strip()
    if not domain:
        print(Fore.RED + "[!] No domain provided, exiting.")
        sys.exit(1)

    wordlist_path = 'wordlists/subdomains.txt'
    if not os.path.isfile(wordlist_path):
        print(Fore.RED + f"[!] Wordlist file not found: {wordlist_path}")
        sys.exit(1)

    threads = 100
    output_file = 'results.json'

    print(Fore.GREEN + f"[+] Starting scan for domain: {domain}")
    print(Fore.GREEN + f"[+] Using wordlist: {wordlist_path}")
    print(Fore.GREEN + f"[+] Concurrency level: {threads}")

    try:
        subs = await resolve_subdomains(domain, wordlist_path, threads)
        print(Fore.GREEN + f"[+] Resolved {len(subs)} subdomains.")
        subs = await scan_http(subs, threads)
        print(Fore.GREEN + "[+] HTTP scan completed.")
        subs = await detect_takeover(subs)
        print(Fore.GREEN + "[+] Takeover detection completed.")
        export_results(subs, output_file)
        print(Fore.GREEN + f"[+] Results exported to {output_file}")
    except Exception as e:
        print(Fore.RED + f"[!] Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted by user")
        sys.exit(1)
