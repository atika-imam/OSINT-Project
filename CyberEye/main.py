import os
from modules import username_check, email_breach, domain_info, metadata_extract
def banner():
    print("="*60)
    print("CyberEye — OSINT Machine (Social + Email + Domain)")
    print("="*60)

def menu():
    print("\n1) Username Investigation")
    print("2) Email Breach Check")
    print("3) Domain Reconnaissance")
    print("4) File Metadata Extraction (PDF/DOCX)")
    print("5) Generate simple HTML report from last results (not implemented)")
    print("6) Exit")

def main():
    banner()
    while True:
        menu()
        choice = input("\nEnter your choice: ").strip()
        if choice == '1':
            username = input("Enter username to search: ").strip()
            if username:
                username_check.search_username(username)
        elif choice == '2':
            email = input("Enter email to check (example@domain.com): ").strip()
            if email:
                email_breach.check_email(email)
        elif choice == '3':
            domain = input("Enter domain (example.com): ").strip()
            if domain:
                domain_info.domain_recon(domain)
        elif choice == '4':
            path = input("Enter file path (PDF or DOCX): ").strip()
            if path:
                metadata_extract.extract_metadata(path)
        elif choice == '6' or choice.lower() == 'exit':
            print("Exiting. Good luck with your demo! 👋")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
