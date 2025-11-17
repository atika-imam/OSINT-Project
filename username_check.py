import aiohttp
import asyncio
import random
from colorama import Fore, Style, init
from modules import report_generator

# Initialize colorama
init(autoreset=True)

# ============================
#          SITES LIST
# ============================
SITES = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}", 
    "LeetCode": "https://leetcode.com/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "TryHackMe": "https://tryhackme.com/p/{}",
    "HackTheBox": "https://app.hackthebox.com/profile/{}",
    "Replit": "https://replit.com/@{}",  
    "Twitter / X": "https://x.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Facebook": "https://www.facebook.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",  
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Minecraft": "https://namemc.com/profile/{}",
    "Chess.com": "https://www.chess.com/member/{}",  
    "Keybase": "https://keybase.io/{}",
}

# ============================
#      USER AGENTS
# ============================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Linux; Android 12; SM-N986B)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
]

# ============================
#      NOT FOUND KEYWORDS
# ============================
NOT_FOUND_KEYWORDS = [
    "page not found",
    "not found",
    "does not exist",
    "no such",
    "unavailable",
    "user not found",
    "sorry, this",
]

# ============================
#      SINGLE SITE CHECK
# ============================
async def check_single_site(session, username, platform, url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "*/*",
        "Referer": "https://www.google.com/",
    }

    try:
        async with session.get(url, headers=headers, timeout=15) as response:
            text = (await response.text()).lower()
            status = response.status

            # Special platform rules
            if platform == "Reddit" and "reddit.com/user" in text:
                return platform, True, url
            if platform == "YouTube" and ("channel" in text or "videocount" in text):
                return platform, True, url
            if platform == "Twitter / X" and ("followers" in text or "following" in text):
                return platform, True, url
            if platform == "LinkedIn" and "public-profile" in text:
                return platform, True, url

            # 404 check
            if status == 404:
                return platform, False, None

            # Keyword-based NOT FOUND
            for key in NOT_FOUND_KEYWORDS:
                if key in text:
                    return platform, False, None

            # Assume exists
            return platform, True, url

    except:
        return platform, False, None

# ============================
#      ASYNC SCANNER
# ============================
async def search_username_async(username):
    print(f"\n🔍 Scanning username: {Fore.CYAN}{username}{Style.RESET_ALL}\n")

    async with aiohttp.ClientSession() as session:
        tasks = [
            check_single_site(session, username, platform, url.format(username))
            for platform, url in SITES.items()
        ]
        results = await asyncio.gather(*tasks)

    profiles = []
    found_count = 0
    formatted_profiles = ""

    # Terminal print
    for platform, exists, url in results:
        profiles.append({
            "platform": platform,
            "found": exists,
            "url": url if exists else None
        })

        if exists:
            status = f"{Fore.GREEN}✔ FOUND{Style.RESET_ALL}"
            found_count += 1
        else:
            status = f"{Fore.RED}❌ Not Found{Style.RESET_ALL}"

        url_display = f": {url}" if url else ""
        print(f"{status} | {platform}{url_display}")
        formatted_profiles += f"{status} | {platform}{url_display}\n"

    print("\n--------------------------------")
    print(f"Total Profiles Found: {Fore.GREEN}{found_count}{Style.RESET_ALL}")
    print("\n✅ Recon finished.\n")

    # Build final result
    username_result = {
        "searched_username": username,
        "total_found": found_count,
        "profiles": profiles
    }

    # CLEAN REPORT FOR HTML
    report_text = (
        f"Searched Username: {username}\n"
        f"Total Profiles Found: {found_count}\n\n"
        f"{formatted_profiles}\n"
    )

    report_generator.add_username_result(
        {"username": username, "report": report_text},
        force=True
    )

    return username_result

# ============================
#      WRAPPER FUNCTION
# ============================
def search_username(username):
    try:
        return asyncio.run(search_username_async(username))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(search_username_async(username))

if __name__ == "__main__":
    user_input = input("Enter username: ").strip()
    if user_input:
        search_username(user_input)

