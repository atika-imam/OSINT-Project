👁️ CyberEye OSINT MachineThe CyberEye OSINT Machine is a command-line utility built in Python for performing quick Open Source Intelligence (OSINT) investigations across multiple domains: social media, email breach detection, and website reconnaissance.🚀 FeaturesThis tool provides the following core functionalities:FeatureDescriptionUsername InvestigationScans over 17 popular social media, coding, and gaming platforms to check for the existence of a given username. Uses aiohttp for fast, asynchronous checks.Email Breach CheckQueries public data breach APIs to determine if an email address has been compromised in a known data leak. Reports the number of sources and the exposed data fields.Domain ReconnaissanceGathers technical information about a target domain, including WHOIS data, DNS Records (A, MX, TXT, etc.), SSL Certificate details, and HTTP Headers.HTML Report GenerationConsolidates all results from the last scan session (Username, Email, and Domain) into a single, comprehensive, and clean HTML report for easy viewing and sharing.Help (Option 5)Displays detailed instructions on how to use each module of the tool.💻 Installation and SetupFollow these steps to set up and run the OSINT Machine.1. PrerequisitesYou must have Python 3 installed on your system.2. Install DependenciesNavigate to the root directory of the project (OSINT-Project-main) in your terminal and install all required Python packages.Bash# It is recommended to use a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all required libraries
pip install -r requirements.txt
3. Run the ToolAfter installing the dependencies, you can start the program using the run.sh script (Linux/macOS) or by directly executing main.py:Bash# Option 1: Using the included run script
./run.sh

# Option 2: Direct execution (recommended on Windows or if run.sh fails)
python3 main.py
📋 How to UseThe tool operates via a simple command-line interface (CLI) menu.Main MenuUpon running the script, you will be presented with the following menu:================================================================================
 ... [Banner Text] ...
  OSINT Machine (Social + Email + Domain)
================================================================================

1) Username Investigation
2) Email Breach Check
3) Domain Reconnaissance
4) Generate HTML Report from Last Results
5) Help (Istemal ki Rahnumai)
6) Exit

Enter your choice:
1. Running an Investigation (Options 1, 2, 3)Enter the corresponding number for the investigation you want to run.The tool will then prompt you for the required input (username, email, or domain).The results will be displayed directly in your terminal.2. Generating the Report (Option 4)The tool saves the results of your last investigation run into memory. Select Option 4 to compile these results into an HTML file.The program will print a local file path to your terminal, starting with file:///.Copy this entire path and paste it directly into your web browser's address bar to view the full, formatted report.3. Help (Option 5)Select Option 5 to view a detailed, step-by-step guide in Roman Urdu explaining the purpose and usage of each of the core modules.4. Exit (Option 6)Closes the program.
