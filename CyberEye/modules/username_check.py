import requests
from colorama import Fore, Style

SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Medium": "https://medium.com/@{}",
}

HEADERS = {"User-Agent": "CyberEye/1.0 (+https://example.local)"}

def check_site(url):
    try:
        r = requests.head(url, headers=HEADERS, allow_redirects=True, timeout=8)
        return r.status_code
    except Exception:
        try:
            r = requests.get(url, headers=HEADERS, allow_redirects=True, timeout=8)
            return r.status_code
        except Exception:
            return None

def search_username(username):
    print(f"\nSearching username: {username}\n")
    found_any = False
    for name, pattern in SITES.items():
        url = pattern.format(username)
        status = check_site(url)
        if isinstance(status, int) and status == 200:
            print(f"{Fore.GREEN}✅ {name}: {url} (status {status}){Style.RESET_ALL}")
            found_any = True
        elif isinstance(status, int) and status in (301,302):
            print(f"{Fore.YELLOW}➡ {name}: redirect (status {status}) {url}{Style.RESET_ALL}")
        elif status is None:
            print(f"{Fore.RED}❌ {name}: request failed{Style.RESET_ALL}")
        else:
            print(f"❌ {name}: not found (status {status})")
    if not found_any:
        print("\nNo public profile found on the sites checked. Try different username variants.\n")
