# CyberEye — Open-Source OSINT Machine

## Overview

CyberEye is an open-source OSINT (Open-Source Intelligence) machine designed to automate information gathering from publicly available sources. It assists cybersecurity learners, analysts, and investigators in collecting data ethically, efficiently, and in a structured manner.
CyberEye brings together essential OSINT capabilities—such as email leak investigation, username lookups, and domain reconnaissance—into one unified tool. Instead of manually checking multiple websites, users can perform these tasks seamlessly and quickly, with results presented through a clean and easy-to-understand HTML report. This makes CyberEye both a time-saving and educational OSINT companion.

---

## Authors
1. Aiman Nasir
2. Atika Imam
3. Soha Haider
4. Maheen Jamali
5. Syed Muhammad Faizan hyder

## Key Features
1. Automated OSINT data collection from multiple open data sources
2. Modular and extendable architecture
3. CLI-based interface for easy usage
4. Clean output formatting, including HTML reports
5. Legally and ethically aligned data collection approach

## Technologies Used
CyberEye is built using modern and reliable technologies to ensure performance, compatibility, and ease of use:

- **Python 3.x** – Core programming language  
- **Requests / HTTP libraries** — for making web/API calls to public OSINT sources 
- **JSON & CSV Handling** – For structured result processing  
- **CLI** — for command line interface and input handling  
- **Standard OSINT APIs & Public Data Sources** — Uses only public and legally accessible OSINT sources.
- **Virtual Environment (venv)** – For dependency isolation  

These technologies make CyberEye lightweight, fast, and easy to extend for beginners, investigators and researchers.

## Installation & Setup
### Step 1: Clone the Repository
- git clone https://github.com/<your-username>/<your-repo-name>.git
- cd CyberEye
### Step 2: Create a Virtual Environment
- python3 -m venv .venv
### Step 3: Activate the Virtual Environment
#### Linux / MacOS
- source .venv/bin/activate
#### Windows
- .venv\Scripts\activate
### Step 4: Install Dependencies
- pip install -r requirements.txt
### Step 5: Run the Tool
- python main.py
#### OR using the provided shell script:
- chmod +x run.sh
- ./run.sh

## Usage Instructions
1. Run the tool using the command above
2. Provide your target input when prompted (Username Investigation, Domain Reconnaisance, Email Breach Check, Generate HTML Report from Last Results, Exit, Help)
3. Allow CyberEye to fetch data from supported OSINT sources
4. View the generated output in the terminal or stored output files
5. Use results strictly for educational or lawful purposes

## Dependencies & Configuration
CyberEye depends on the following:
- Python 3.x
- Required libraries listed in requirements.txt
- Internet access (for OSINT data retrieval)

## Future Enhancements
- **Threat Intelligence Integration** — Feed OSINT data into platforms like OpenCTI, MISP, or SIEM.  
- **AI-powered Insights** — Incorporate AI analysis for pattern detection and data correlation.  
- **Secure API Integration** — Support for user-provided API keys and secure credential storage.  
- **GUI & Dashboard** — Web or desktop interface showing past investigations and saved reports.  
- **Ethics & Compliance** — Built-in checklist, legal compliance report for all used sources.  
- **Expand OSINT Modules** — Add more data sources like social media, breach databases, and advanced reconnaissance.
- **Report Improvements** — Enhanced HTML reports with charts, PDF export, and customizable templates.  
- **Credential Monitoring** — Real-time alerts for email/domain leaks using breach-notification APIs.  

## Legal & Ethical Compliance
CyberEye is built strictly for:
- Cybersecurity education
- Research and academic purposes
- Awareness training
The tool does NOT exploit or hack any system. It only collects publicly available information, aligning with:
- Ethical OSINT investigation practices
- International cyber laws and responsible disclosure guidelines
- Privacy and data protection norms
Users are responsible for ensuring their actions comply with applicable laws in their region.

## License
This project is open-source and available under the MIT License.

## Contribution
Contributions are welcome!
Feel free to submit issues, feature requests, or pull requests to improve CyberEye.

---

# Shine a light on public data — with CyberEye.
