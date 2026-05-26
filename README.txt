╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                         RBT  - Setup & Usage Guide                                                    ║
║                             @Rbt                                                                      ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════╝


CONTENTS
========
• RbtNew.py          - Main application with all tools
• setup.bat          - Dependency installation script
• RUN_TOOL.bat       - Quick launcher for the tool
• output/            - Folder where downloaded websites are saved
• README.txt         - This file


SYSTEM REQUIREMENTS
===================
✓ Every Linux distro
✓ Windows 10/11 (64-bit recommended)
✓ Python 3.8 or higher (https://www.python.org/downloads/)
✓ 2GB+ free disk space
✓ Internet connection

INSTALLATION
=============

1. FIRST TIME SETUP:
   
   a) Open setup.py by double-clicking it
   b) Wait for Python packages to install
   c) Press Enter when complete
   
   This will:
   ✓ Create a virtual environment (venv/)
   ✓ Install all required dependencies
   ✓ Prepare the tool for use


2. STARTING THE TOOL:
   
   After setup, you can start the tool in 2 ways:
   
   Method 1 (Easy):
   - Double-click RUN_TOOL.bat
   
   Method 2 (Manual):
   - Open Command Prompt/PowerShell
   - Navigate to this folder
   - Run: venv\Scripts\activate.bat
   - Run: python RbtNew.py


DEPENDENCIES INSTALLED
======================

Core Dependencies:
• requests           - HTTP library for web requests
• dnspython          - DNS resolution (Email Tracker)
• phonenumbers       - Phone number parsing
• beautifulsoup4     - HTML parsing (Website Copier)
• lxml               - XML/HTML parsing

Optional Packages:
• pillow             - Image processing
• whois              - WHOIS lookups
• discord.py         - Discord integration
• selenium           - Browser automation


AVAILABLE TOOLS
===============

Tool 01 - IP Grabber Script
    Create a script that captures IP addresses

Tool 02 - Webhook Spammer
    Send bulk messages to Discord webhooks

Tool 03 - Auto Spammer
    Automated messaging system

Tool 04 - Bot Sender
    Send messages via Discord bots (under development)

Tool 05 - IP Info
    Get detailed information about any IP address

Tool 06 - Phone Info
    Look up phone number information

Tool 07 - IP Generator
    Generate valid IP addresses

Tool 08 - Instagram OSINT
    Gather open-source intelligence on Instagram profiles

Tool 09 - Photo Metadata
    Extract metadata from photos

Tool 10 - Username Tracker ⭐ ENHANCED
    Search for usernames across 35+ platforms
    Features:
    ✓ Real-time account detection
    ✓ Platform validation
    ✓ Multiple social networks

Tool 11 - Email Tracker ⭐ ENHANCED
    Check if emails are in databreach incidents
    Features:
    ✓ 5 breach databases (HIBP, EmailRep, HackerTarget, Rapid7, Google)
    ✓ Domain validation
    ✓ MX record lookup
    ✓ Security recommendations
    ✓ Account registration detection

Tool 12 - IP Grabber & Crasher (Discord)
    Windows-specific tool for Discord

Tool 13 - [Coming Soon]

Tool 14 - [Coming Soon]

Tool 15 - Base64 Encoder/Decoder
    Encode and decode Base64 strings

Tool 16 - Website Copier ⭐ NEW
    Copy entire websites locally for offline viewing
    Features:
    ✓ Downloads HTML, CSS, JS, images
    ✓ Auto-rebuilds directory structure
    ✓ Fixes internal links automatically
    ✓ Saves to output/ folder
    ✓ Max 500 files per website

Tool 17 - Website Info Scanner
    Detailed intelligence on websites
    Features:
    ✓ DNS lookup
    ✓ WHOIS information
    ✓ Server detection
    ✓ Technology identification

Tool 18 - Vulnerability Scanner
    Scan websites for security vulnerabilities


TROUBLESHOOTING
================

Problem: "Python not found"
Solution: Install Python from https://www.python.org/downloads/
          Make sure to CHECK "Add Python to PATH"

Problem: "Virtual environment not found"
Solution: Run setup.bat first to create and activate it

Problem: "Module not found" error
Solution: Delete venv/ folder and run setup.bat again

Problem: "Connection timeout"
Solution: Check internet connection, try again later

Problem: "Website copier not downloading files"
Solution: Check if website blocks automated access
          Try a different website for testing


API NOTES
=========

Email Tracker uses these free APIs:
✓ HaveIBeenPwned.com - Breach database
✓ EmailRep.io - Email reputation
✓ HackerTarget.com - Leak database
✓ Rapid7 Sonarss - Compromise detection
✓ Google Search - Public exposure check

No API keys required - all calls are direct

DISCLAIMER
==========

This tool is for educational and authorized security research only.

✗ ILLEGAL USES:
  • Unauthorized access to systems
  • Harassment or spam
  • Data theft
  • Violation of Terms of Service

✓ LEGAL USES:
  • Personal security research
  • Website archiving
  • Breach monitoring
  • OSINT for authorized purposes


UPDATES & SUPPORT
==================

Visit: https://discord.gg/xDgCa7HJV3
Author: RBT


VERSION INFO
=============

RBT v1.0
Release: May 2026
Status: Active Development


═══════════════════════════════════════════════════════════════════════════

Questions? Problems? Join the Discord community above!

═══════════════════════════════════════════════════════════════════════════
