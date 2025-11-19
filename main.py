#!/usr/bin/env python3
import os, json
from modules import username_check, email_breach, domain_info, report_generator

LAST_RESULTS_FILE = "last_results.json"

def banner():
    print("="*80)
    print(r"""
     _____          _                    
    / ____|  _   _ | |__   ___   _
    | |     | | | || _  \ / _ \ | |_
    | |___  | | | |||_) | | __/ |  _|
    \_____| \___  ||____/ \___| |_|     👁️   👁️       
                | | 
                |_|
                                            
    """)
    print("  OSINT Machine (Social + Email + Domain)")
    print("="*80)


# ============================
# 📌 USER HELP (for Help option)
# ============================
def instructions():
    print("\n📌 HOW TO USE THE CYBEREYE OSINT MACHINE:")
    print("-----------------------------------------")
    print("1. Username Investigation:")
    print("   • Checks digital footprint of any username.")
    print("   • Finds profiles on social platforms.")
    print("   • Enter any username to start.")
    print("")
    print("2. Email Breach Check:")
    print("   • Checks if the email was exposed in any data breach.")
    print("   • Shows breach names, dates, and leak counts.")
    print("   • Enter the email address.")
    print("")
    print("3. Domain Reconnaissance:")
    print("   • Collects WHOIS, DNS, IP, MX, SSL data.")
    print("   • Enter any domain (example: google.com).")
    print("")
    print("4. Generate HTML Report:")
    print("   • Creates a complete HTML report from last scan.")
    print("   • Report auto-saves and opens in browser.")
    print("")
    print("5. Help / Instructions:")
    print("   • Shows this help guide for users.")
    print("")
    print("6. Exit:")
    print("   • Close the tool safely.")
    print("-----------------------------------------")
    print("💡 Tip: Scan results auto-save in 'last_results.json'.")
    print("💡 Tip: Reports save inside the 'reports' folder.")
    print("-----------------------------------------\n")


def menu():
    print("\n1) Username Investigation")
    print("2) Email Breach Check")
    print("3) Domain Reconnaissance")
    print("4) Generate HTML Report from Last Results")
    print("5) Help / Instructions")
    print("6) Exit")


def save_last_results(data):
    with open(LAST_RESULTS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_last_results():
    if not os.path.exists(LAST_RESULTS_FILE):
        return None
    with open(LAST_RESULTS_FILE, "r") as f:
        return json.load(f)


def print_result(result, title):
    print(f"\n🌐 {title} Result:\n")
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:")
            for i in value:
                print(f"  - {i}")
        elif isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")
    print("\n✅ Recon finished.")


def main():
    while True:
        os.system('cls' if os.name=='nt' else 'clear')

        banner()
        menu()

        choice = input("\nEnter your choice: ").strip()

        # USERNAME
        if choice == '1':
            username = input("Enter username: ").strip()
            if username:
                result = username_check.search_username(username)
                save_last_results({"username_investigation": result})
                report_generator.add_username_result(result, force=True)

        # EMAIL
        elif choice == '2':
            email = input("Enter email: ").strip()
            if email:
                result = email_breach.check_email(email)
                save_last_results({"email_breach_check": result})

                report_generator.add_email_result({
                    "email": email,
                    "report": (
                        f"Status: {result['status']}\n"
                        f"Found in {result.get('found', 0)} sources\nSources:\n" +
                        "\n".join([
                            f"{s.get('name')} - {s.get('date', 'Unknown')}"
                            for s in result.get('sources', [])
                        ])
                    )
                }, force=True)

                print_result({
                    "email": email,
                    "status": result["status"],
                    "found": result.get("found", 0)
                }, "Email")

        # DOMAIN
        elif choice == '3':
            domain = input("Enter domain: ").strip()
            if domain:
                result = domain_info.domain_recon(domain)
                if "domain" not in result:
                    result["domain"] = domain

                save_last_results({"domain_recon": result})

                report_generator.add_domain_result({
                    "domain": domain,
                    "report": "\n".join([f"{k}: {v}" for k, v in result.items()])
                }, force=True)

                print_result({
                    "domain": domain,
                    "details": result
                }, "Domain")

        # REPORT
        elif choice == '4':
            data = load_last_results()
            if not data:
                print("\n⚠ No previous results found to generate report.")
                input("\nPress Enter to continue...")
                continue

            report_generator.CHECKED_EMAILS.clear()
            report_generator.CHECKED_DOMAINS.clear()
            report_generator.CHECKED_USERNAMES.clear()

            # EMAIL
            if "email_breach_check" in data:
                d = data["email_breach_check"]
                report_generator.add_email_result({
                    "email": d.get("email", "Unknown"),
                    "report": (
                        f"Status: {d['status']}\n"
                        f"Found in {d.get('found',0)} sources\nSources:\n" +
                        "\n".join([
                            f"{s.get('name')} - {s.get('date','Unknown')}"
                            for s in d.get('sources', [])
                        ])
                    )
                }, force=True)

            # DOMAIN
            if "domain_recon" in data:
                d = data["domain_recon"]
                report_generator.add_domain_result({
                    "domain": d.get("domain", "Unknown"),
                    "report": "\n".join([f"{k}: {v}" for k, v in d.items()])
                }, force=True)

            # USERNAME
            if "username_investigation" in data:
                report_generator.add_username_result(
                    data["username_investigation"], force=True
                )

            report_generator.generate_html_report()

        # HELP OPTION
        elif choice == '5':
            os.system('cls' if os.name=='nt' else 'clear')
            banner()
            instructions()
            input("Press Enter to go back...")

        # EXIT
        elif choice == '6' or choice.lower() == 'exit':
            break

        else:
            print("\nInvalid choice.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
