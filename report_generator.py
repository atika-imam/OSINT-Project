import os
import re
import html
from datetime import datetime
from colorama import Fore, Style
import tempfile

# ---------------- Memory Storage for OSINT Results ---------------- #
CHECKED_EMAILS = []
CHECKED_DOMAINS = []
CHECKED_USERNAMES = []

# ---------------- Utility Functions ---------------- #
def make_clickable(text):
    """Convert URLs in text to clickable HTML links."""
    url_pattern = r'(https?://[^\s]+)'
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)

# ---------------- Report Generation ---------------- #
def generate_html_report():
    """Generate HTML report in memory and print browser link with download button."""
    if not (CHECKED_EMAILS or CHECKED_DOMAINS or CHECKED_USERNAMES):
        print(f"{Fore.YELLOW}⚠ No data to generate report.{Style.RESET_ALL}")
        return None

    html_content = f"""
<html>
<head>
    <title>CyberEye OSINT Report</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background:#f5f5f5; }}
        h1 {{ color: #2b5797; }}
        h3 {{ color: #333; }}
        pre {{ background:#eee; padding:10px; border-radius:5px; overflow:auto; white-space: pre-wrap; word-wrap: break-word; }}
        .box {{ border:1px solid #ccc; padding:10px; margin-bottom:15px; background:white; }}
        a {{ color: #1a0dab; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .download-btn {{ display:inline-block; margin:10px 0; padding:8px 12px; background:#2b5797; color:white; border-radius:5px; text-decoration:none; }}
        .download-btn:hover {{ background:#1a3e70; }}
    </style>
</head>
<body>
    <h1>CyberEye — OSINT Report</h1>
    <small>Generated: {datetime.now()}</small>
    <hr>
    <a class="download-btn" id="downloadBtn">⬇ Download Report</a>
    <div id="reportContent">
"""

    # ---------------- Emails ---------------- #
    for idx, data in enumerate(CHECKED_EMAILS, 1):
        email_val = data.get("email") or data.get("searched_email")
        if not email_val:
            continue
        html_content += f"<div class='box'><h3>Email {idx}: {html.escape(email_val)}</h3><pre>"
        html_content += format_terminal_style_report(data)
        html_content += "</pre></div>"

    # ---------------- Domains ---------------- #
    for idx, data in enumerate(CHECKED_DOMAINS, 1):
        domain_val = data.get("domain")
        if not domain_val:
            continue
        html_content += f"<div class='box'><h3>Domain {idx}: {html.escape(domain_val)}</h3><pre>"
        html_content += format_terminal_style_report(data)
        html_content += "</pre></div>"

    # ---------------- Usernames ---------------- #
    for idx, data in enumerate(CHECKED_USERNAMES, 1):
        username_val = data.get("username") or data.get("searched_username")
        if not username_val:
            continue
        html_content += f"<div class='box'><h3>Username {idx}: {html.escape(username_val)}</h3><pre>"
        html_content += format_terminal_style_report(data)
        html_content += "</pre></div>"

    html_content += """
    </div>
    <script>
    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.addEventListener('click', function() {
        const content = document.getElementById('reportContent').innerHTML;
        const blob = new Blob([content], { type: 'text/html' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'cybereye_report.html';
        a.click();
    });
    </script>
</body>
</html>
"""

    with tempfile.NamedTemporaryFile('w', delete=False, suffix=".html", encoding="utf-8") as tmp:
        tmp.write(html_content)
        temp_path = tmp.name

    print(f"\n✅ Report generated")
    print(f"Open this link in browser to view: file://{os.path.abspath(temp_path)}")
    print("Click '⬇ Download Report' in browser to save the file.\n")
    return temp_path

# ---------------- Format terminal style ---------------- #
def format_terminal_style_report(data):
    """Formats a single OSINT result dict like terminal output with ✔ / ❌ and clickable links."""
    output = ''

    if 'profiles' in data and data['profiles']:
        for item in data['profiles']:
            platform = item.get('platform', 'Unknown')
            found = item.get('found', False)
            url = item.get('url')
            status = '✅ FOUND' if found else '❌ Not Found'
            url_display = f": {make_clickable(html.escape(url))}" if url else ''
            output += f"{status} | {platform}{url_display}\n"

        # Total found count
        total_found = data.get('total_found', 0)
        output += '\n--------------------------------\n'
        output += f'Total Profiles Found: {total_found}\n'

    elif 'report' in data:
        # fallback for emails/domains
        output += data['report'] + '\n'

    else:
        output += 'No data available.\n'

    return output

# ---------------- Add results safely ---------------- #
def add_email_result(result, force=False):
    if force:
        CHECKED_EMAILS.clear()
    if result:
        CHECKED_EMAILS.append(result)

def add_domain_result(result, force=False):
    if force:
        CHECKED_DOMAINS.clear()
    if result:
        CHECKED_DOMAINS.append(result)

def add_username_result(result, force=False):
    if force:
        CHECKED_USERNAMES.clear()
    if result:
        CHECKED_USERNAMES.append(result)

