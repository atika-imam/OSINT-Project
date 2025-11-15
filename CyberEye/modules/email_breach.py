import os
import re
import json
import time
import requests
from datetime import datetime
from colorama import Fore, Style

USER_AGENT = "CyberEye-EmailCheck/1.0"
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def is_valid_email(email: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email) is not None

def save_report(data: dict):
    safe_email = re.sub(r"[^a-zA-Z0-9]", "_", data['email'])
    path = os.path.join(REPORTS_DIR, f"email_{safe_email}.json")
    redacted = {
        "email": data["email"],
        "checked_at": data["checked_at"],
        "provider": data["provider"],
        "status": data["status"],
        "breaches": [
            {"name": b.get("name"), "date": b.get("date")} for b in data.get("breaches", [])
        ],
    }
    with open(path, "w") as f:
        json.dump(redacted, f, indent=2)
    print(f"{Fore.CYAN}📁 Saved report: {path}{Style.RESET_ALL}")

def breachdirectory_lookup(email: str):
    api_key = os.getenv("BREACHDIR_RAPIDAPI_KEY") or os.getenv("BREACHDIR_API_KEY")
    if not api_key:
        print(f"{Fore.YELLOW}⚠ No BreachDirectory API key found — using simulated result.{Style.RESET_ALL}")
        return {
            "email": email,
            "checked_at": datetime.utcnow().isoformat(),
            "provider": "BreachDirectory (SIMULATED)",
            "status": "not_found",
            "breaches": [],
            "raw_response": {},
        }

    url = "https://breachdirectory.p.rapidapi.com/"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "breachdirectory.p.rapidapi.com",
        "User-Agent": USER_AGENT,
    }

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(f"{url}?func=auto&term={email}", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                breaches = []
                for item in data.get("result", []):
                    breaches.append({
                        "name": item.get("name") or item.get("source") or "Unknown",
                        "date": item.get("date") or item.get("breach_date") or "N/A",
                        "extra": {"line": item.get("line")[:80] if item.get("line") else None}
                    })
                status = "found" if breaches else "not_found"
                return {
                    "email": email,
                    "checked_at": datetime.utcnow().isoformat(),
                    "provider": "BreachDirectory",
                    "status": status,
                    "breaches": breaches,
                    "raw_response": {k: v for k, v in data.items() if k != "result"},
                }

            elif response.status_code in (401, 403):
                print(f"{Fore.RED}❌ Unauthorized or Forbidden — check your API key.{Style.RESET_ALL}")
                break
            elif response.status_code == 404:
                print(f"{Fore.YELLOW}⚠ No data found for {email}.{Style.RESET_ALL}")
                return {
                    "email": email,
                    "checked_at": datetime.utcnow().isoformat(),
                    "provider": "BreachDirectory",
                    "status": "not_found",
                    "breaches": [],
                    "raw_response": {},
                }
            elif response.status_code == 429:
                wait = (2 ** attempt)
                print(f"{Fore.YELLOW}⚠ Rate limit hit. Retrying in {wait}s...{Style.RESET_ALL}")
                time.sleep(wait)
                continue
            else:
                print(f"{Fore.RED}⚠ Error {response.status_code}: {response.text[:100]}{Style.RESET_ALL}")
                break
        except requests.exceptions.Timeout:
            print(f"{Fore.YELLOW}⚠ Timeout. Retrying...{Style.RESET_ALL}")
            time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}❌ Request error: {e}{Style.RESET_ALL}")
            break

    return {
        "email": email,
        "checked_at": datetime.utcnow().isoformat(),
        "provider": "BreachDirectory",
        "status": "error",
        "breaches": [],
        "raw_response": {},
    }

def check_email(email: str):
    print(f"\n{Fore.CYAN}🔍 Checking possible breaches for: {email}{Style.RESET_ALL}\n")
    if not is_valid_email(email):
        print(f"{Fore.RED}❌ Invalid email format.{Style.RESET_ALL}")
        return
    result = breachdirectory_lookup(email)
    if result["status"] == "found":
        print(f"{Fore.RED}⚠ Breach FOUND in {len(result['breaches'])} sources!{Style.RESET_ALL}")
        for b in result["breaches"]:
            print(f"   • {b['name']} ({b['date']})")
    elif result["status"] == "not_found":
        print(f"{Fore.GREEN}✅ No breach found for {email}.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠ Error or simulated result.{Style.RESET_ALL}")
    save_report(result)
    return result

def self_test():
    test_email = "example@gmail.com"
    print(f"\nRunning self-test with {test_email}\n")
    check_email(test_email)

if __name__ == "__main__":
    self_test()
