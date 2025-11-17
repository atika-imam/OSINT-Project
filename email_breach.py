import re
import requests
import json
import os
from datetime import datetime
from colorama import Fore, Style

USER_AGENT = "CyberEye-EmailCheck/1.0"
LEAKCHECK_API = "https://leakcheck.io/api/public"

# File to store the last result
LAST_RESULT_FILE = "last_result.json"
REPORT_FILE = "report.html"


# ---------------------------
#  Email Validation
# ---------------------------
def is_valid_email(email: str) -> bool:
    """Check if email is valid format"""
    return re.match(r"^[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", email) is not None


# ---------------------------
#  LeakCheck Lookup
# ---------------------------
def leakcheck_lookup(query: str):
    """Query LeakCheck.io public API"""
    try:
        response = requests.get(
            LEAKCHECK_API,
            params={"check": query},
            headers={"User-Agent": USER_AGENT},
            timeout=10
        )
        data = response.json()

        if not data.get("success"):
            return {
                "email": query,
                "checked_at": datetime.utcnow().isoformat(),
                "provider": "LeakCheck.io",
                "status": "not_found",
                "found": 0,
                "fields": [],
                "sources": []
            }

        return {
            "email": query,
            "checked_at": datetime.utcnow().isoformat(),
            "provider": "LeakCheck.io",
            "status": "found" if data.get("found", 0) > 0 else "not_found",
            "found": data.get("found", 0),
            "fields": data.get("fields", []),
            "sources": data.get("sources", [])
        }

    except Exception as e:
        print(f"{Fore.RED}❌ LeakCheck request failed: {e}{Style.RESET_ALL}")
        return {
            "email": query,
            "checked_at": datetime.utcnow().isoformat(),
            "provider": "LeakCheck.io",
            "status": "error",
            "found": 0,
            "fields": [],
            "sources": []
        }


# ---------------------------
#  Save Last Result
# ---------------------------
def save_last_result(result):
    """Save only the last checked email result"""
    try:
        with open(LAST_RESULT_FILE, "w") as f:
            json.dump(result, f, indent=4)
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to save last result: {e}{Style.RESET_ALL}")


# ---------------------------
#  Generate HTML Report
# ---------------------------
def generate_report():
    """Generate human-readable report from last_result.json"""
    if not os.path.exists(LAST_RESULT_FILE):
        print(f"{Fore.YELLOW}⚠ No last result found to generate report.{Style.RESET_ALL}")
        return

    with open(LAST_RESULT_FILE, "r") as f:
        data = json.load(f)

    if data.get("status") != "found":
        print(f"{Fore.YELLOW}⚠ No breaches found or error occurred. Nothing to report.{Style.RESET_ALL}")
        return

    email = data.get("email")
    checked_at = data.get("checked_at")
    provider = data.get("provider")
    found = data.get("found")
    sources = data.get("sources", [])

    html = f"""
    <html>
    <head>
        <title>Breach Report for {email}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.5; }}
            h1 {{ color: #b22222; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Breach Report: {email}</h1>
        <p><strong>Checked at:</strong> {checked_at}</p>
        <p><strong>Provider:</strong> {provider}</p>
        <p><strong>Total Sources Found:</strong> {found}</p>

        <h2>Sources:</h2>
        <table>
            <tr><th>#</th><th>Source</th><th>Date</th></tr>
    """

    for idx, src in enumerate(sources, 1):
        date = src.get("date") if src.get("date") else "Unknown"
        html += f"<tr><td>{idx}</td><td>{src.get('name')}</td><td>{date}</td></tr>"

    html += """
        </table>
    </body>
    </html>
    """


# ---------------------------
#  Check Email CLI
# ---------------------------
def check_email(email: str):
    """Check email and display results in CLI"""
    print(f"\n{Fore.CYAN}🔍 Checking possible breaches for: {email}{Style.RESET_ALL}\n")

    if not is_valid_email(email):
        print(f"{Fore.RED}❌ Invalid email format.{Style.RESET_ALL}")
        return

    result = leakcheck_lookup(email)

    if result["status"] == "found":
        print(f"{Fore.RED}⚠ Breach FOUND in {result['found']} sources!{Style.RESET_ALL}\n")

        if result["fields"]:
            print(f"{Fore.YELLOW}📌 Exposed Fields: {', '.join(result['fields'])}{Style.RESET_ALL}")

        print("\n📂 Sources:")
        for idx, src in enumerate(result["sources"], 1):
            date = src.get('date', 'Unknown') or "Unknown"
            print(f"{idx}. {src['name']} - {date}")

    elif result["status"] == "not_found":
        print(f"{Fore.GREEN}✅ No breach found for {email}.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠ Could not check {email} due to API error.{Style.RESET_ALL}")

    # Save and generate report
    save_last_result(result)
    generate_report()

    return result


# ---------------------------
#  Main
# ---------------------------
if __name__ == "__main__":
    email_to_check = input("Enter email to check: ").strip()
    check_email(email_to_check)

