import socket
import requests
import subprocess

def get_whois_info(domain):
    try:
        import whois
        data = whois.whois(domain)
        if data and (data.get("registrar") or data.get("creation_date")):
            return {
                "Registrar": data.get("registrar", "N/A"),
                "Creation Date": str(data.get("creation_date")),
                "Expiration Date": str(data.get("expiration_date")),
                "Registrant": data.get("org", "N/A"),
                "Country": data.get("country", "N/A"),
            }
    except Exception:
        pass
    try:
        raw = subprocess.check_output(["whois", domain], text=True, timeout=10)
        result = {}
        for line in raw.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                if any(k in key.lower() for k in ["registrar", "creation", "expiry", "organization", "country"]):
                    result[key.strip()] = val.strip()
        return result if result else {"raw": raw[:1000]}
    except Exception as e:
        return {"error": str(e)}

def domain_recon(domain):
    print(f"\n🌐 Domain reconnaissance for: {domain}\n")
    try:
        ip = socket.gethostbyname(domain)
        print(f"IP A records: {ip}")
    except Exception as e:
        print(f"Error getting IP: {e}")
    whois_data = get_whois_info(domain)
    if whois_data:
        print("\nWHOIS Information:")
        for k, v in whois_data.items():
            print(f"{k}: {v}")
    else:
        print("WHOIS data not found or restricted.")
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        print(f"\nHTTP(s) response status: {response.status_code}")
        print(f"Server header: {response.headers.get('server', 'N/A')}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
    except Exception as e:
        print(f"HTTP request failed: {e}")
