#!/usr/bin/env python3
import socket
import requests
import subprocess
import ssl
import dns.resolver
import datetime

TOP_N_SUBDOMAINS = 50

# ----------------- DOMAIN RECON FUNCTIONS -----------------
def get_whois_info(domain):
    try:
        import whois
        data = whois.whois(domain)
        return {
            "Registrar": data.get("registrar", "N/A"),
            "Creation Date": str(data.get("creation_date")),
            "Expiration Date": str(data.get("expiration_date")),
            "Registrant": data.get("org", "N/A"),
            "Country": data.get("country", "N/A"),
            "Name Servers": data.get("name_servers", "N/A"),
            "Status": data.get("status", "N/A"),
        }
    except Exception:
        try:
            raw = subprocess.check_output(["whois", domain], text=True, timeout=10)
            lines = raw.splitlines()
            filtered = [line for line in lines if line.strip()][:20]
            return {"raw": "\n".join(filtered)}
        except Exception as e:
            return {"error": str(e)}

def get_dns_records(domain):
    records = {}
    rtypes = ["A", "AAAA", "CNAME", "MX", "NS", "TXT"]
    for rtype in rtypes:
        try:
            answers = dns.resolver.resolve(domain, rtype, lifetime=5)
            records[rtype] = [str(a.to_text()) for a in answers]
        except Exception:
            records[rtype] = []
    return records

def reverse_dns(ip):
    try:
        name, _, _ = socket.gethostbyaddr(ip)
        return name
    except Exception:
        return None

def parse_spf_dmarc(txt_records):
    spf = []
    dmarc = []
    for t in txt_records:
        t = t.strip('"')
        if t.lower().startswith("v=spf1") or "spf1" in t.lower():
            spf.append(t)
        if "_dmarc" in t.lower() or "v=dmarc1" in t.lower():
            dmarc.append(t)
    return {"SPF": spf, "DMARC": dmarc}

def get_subdomains(domain):
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        subs = set()
        for entry in data:
            name = entry.get('name_value', '')
            for n in name.split('\n'):
                n = n.strip()
                if n and domain in n:
                    subs.add(n)
        return sorted(subs)
    except Exception:
        return []

def get_ssl_info(domain):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
            issuer = dict(x[0] for x in cert.get('issuer', [])) if cert.get('issuer') else None
            subject = dict(x[0] for x in cert.get('subject', [])) if cert.get('subject') else None
            return {
                "issuer": issuer or cert.get('issuer'),
                "subject": subject or cert.get('subject'),
                "valid_from": cert.get('notBefore'),
                "valid_to": cert.get('notAfter')
            }
    except Exception:
        return {}

def check_security_headers(domain):
    try:
        resp = requests.head(f"https://{domain}", timeout=6, allow_redirects=True)
    except Exception:
        try:
            resp = requests.get(f"http://{domain}", timeout=6, allow_redirects=True)
        except Exception:
            return {}
    headers = resp.headers
    security = {
        "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
        "Content-Security-Policy": headers.get("Content-Security-Policy"),
        "X-Frame-Options": headers.get("X-Frame-Options"),
        "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
        "Referrer-Policy": headers.get("Referrer-Policy"),
        "Permissions-Policy": headers.get("Permissions-Policy"),
    }
    return security

def fetch_robots_sitemap(domain):
    out = {}
    for path in ["/robots.txt", "/sitemap.xml"]:
        try:
            url = f"https://{domain}{path}"
            r = requests.get(url, timeout=6)
            if r.status_code == 200:
                out[path] = r.text[:4000]
            else:
                url = f"http://{domain}{path}"
                r = requests.get(url, timeout=6)
                out[path] = r.text[:4000] if r.status_code == 200 else None
        except Exception:
            out[path] = None
    return out

# ----------------- DOMAIN RECON WRAPPER -----------------
def domain_recon(domain):
    print(f"\n🌐 Recon for domain: {domain}\n")
    report = { "dns": "", "whois": "", "spf_dmarc": "", "subdomains": "", "ssl": "", "headers": "", "extras": "" }

    dns_records = get_dns_records(domain)
    report["dns"] = f"A: {dns_records.get('A')}\nAAAA: {dns_records.get('AAAA')}\nAll: {dns_records}"
    if dns_records.get("A"):
        rdns = reverse_dns(dns_records["A"][0])
        print(f"PTR: {rdns}")

    whois_data = get_whois_info(domain)
    report["whois"] = "\n".join([f"{k}: {v}" for k, v in whois_data.items()])

    txts = dns_records.get("TXT", [])
    spf_dmarc = parse_spf_dmarc(txts)
    report["spf_dmarc"] = f"SPF: {spf_dmarc.get('SPF')}\nDMARC: {spf_dmarc.get('DMARC')}"

    subs = get_subdomains(domain)
    report["subdomains"] = "\n".join(subs[:TOP_N_SUBDOMAINS]) if subs else "None"

    ssl_info = get_ssl_info(domain)
    report["ssl"] = "\n".join([f"{k}: {v}" for k, v in ssl_info.items()]) if ssl_info else "Could NOT fetch"

    sec = check_security_headers(domain)
    report["headers"] = "\n".join([f"{k}: {v}" for k, v in sec.items()])

    extras = fetch_robots_sitemap(domain)
    report["extras"] = f"robots.txt: {bool(extras.get('/robots.txt'))}\nsitemap.xml: {bool(extras.get('/sitemap.xml'))}"

    return report

