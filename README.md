# Reco-Toolkit

Automated reconnaissance and OSINT workflow for bug bounty hunting and penetration testing. Orchestrates multiple security tools into a unified Python-based workflow.

## Overview

**Recon Toolkit** automates the initial reconnaissance phase of security assessments by executing and organizing results from multiple OSINT and scanning tools. Instead of manually running each tool separately, this toolkit orchestrates them into a single workflow with unified output.

### Why This Tool?

-  **Save Time** - Automate repetitive reconnaissance tasks
-  **Organized Output** - All results in structured folders with JSON summaries
-  **Consistent Methodology** - Follow the same recon process every time
-  **Extensible** - Easy to add new tools to the workflow

##  Features

- **Automated Subdomain Enumeration** - Discover subdomains using theHarvester
- **Port Scanning** - Identify open ports and services with Nmap
- **Technology Detection** - Fingerprint web technologies with WhatWeb
- **Email Harvesting** - Collect emails from public sources
- **Structured Reports** - JSON summaries for easy parsing
- **Modular Design** - Run all tools or select specific ones

## 🛠️ Tools Integrated

| Tool | Status |
|------|---------|
| **theHarvester** | ✅ Implemented |
| **Nmap** | ✅ Implemented |
| **WhatWeb** | ✅ Implemented |
| **Sherlock** | 🚧 Planned |
| **PhoneInfoga** | 🚧 Planned |


## Installation

### Pre-requisites

```bash
# Python 3.8 or higher
python3 --version

# Required tools (Debian/Ubuntu)
sudo apt update
sudo apt install nmap whatweb -y
pip3 install theHarvester colorama
```

### Clone Repository

```bash
git clone https://github.com/c4feina/reco-toolkit.git
cd reco-toolkit
pip install -r requirements.txt
```

## Usage

```bash
python recon.py -h

Options:
  -t, --target TARGET    Target domain (required)
  --full                 Run complete reconnaissance workflow
  --harvester            Run only theHarvester
  --nmap                 Run only Nmap scan
  --whatweb              Run only WhatWeb
  -o, --output DIR       Custom output directory
```

### Examples

```bash
# Full scan with all tools
python recon.py -t bugcrowd.com --full

# Only subdomain enumeration
python recon.py -t hackerone.com --harvester

# Only port scanning
python recon.py -t example.com --nmap

# Custom output directory
python recon.py -t target.com --full -o my_recon
```

# Output Structure

```
recon_example_com/
├── harvester_results.json    # Emails and subdomains
├── nmap_scan.txt             # Port scan results
├── whatweb_results.json      # Technology fingerprinting
└── summary.json              # Consolidated findings
```

### Example summary.json

```json
{
  "target": "example.com",
  "timestamp": "2025-9-12 T 23:45",
  "subdomains": [
    "www.example.com",
    "mail.example.com",
    "api.example.com"
  ],
  "open_ports": [
    "80/tcp open http",
    "443/tcp open https"
  ],
  "technologies": [
    "Apache/*.*.**",
    "PHP/*.*.*"
  ],
  "emails": [
    "example@example.com",
    "example@example.com"
  ]
}
```

## Reconnaissance Methodology

This toolkit follows a standard bug bounty reconnaissance workflow:

### Phase 1: Information Gathering
- Domain enumeration
- Email harvesting  
- Public records search via theHarvester

### Phase 2: Network Mapping
- Port scanning (common + custom ranges)
- Service identification
- Banner grabbing with Nmap

### Phase 3: Technology Detection
- Web server identification
- Framework detection
- CMS fingerprinting with WhatWeb

### Phase 4: Analysis & Reporting
- Consolidate findings into JSON
- Identify potential attack vectors
- Generate summary report

## Configuration

Edit `config.json` to customize:

```json
{
  "nmap": {
    "default_ports": "1-1000",
    "timing": "T4",
    "version_detection": true
  },
  "harvester": {
    "sources": "all",
    "limit": 500
  },
  "whatweb": {
    "aggression": 1
  }
}
```
**IMPORTANT: This tool is for authorized security testing only.**
