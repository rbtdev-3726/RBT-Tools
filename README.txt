# RBT Toolkit

## Overview

RBT Toolkit is a multi-purpose Python-based console utility designed for educational, testing, automation, and OSINT-oriented workflows. The project combines several modules into a single terminal interface, allowing users to perform network analysis, metadata inspection, basic automation tasks, encoding utilities, and public-information gathering from multiple sources.

The toolkit is intended for:

* Educational and research environments
* Cybersecurity learning labs
* Local testing and debugging
* Open-source intelligence (OSINT) workflows
* Network and infrastructure analysis
* Metadata inspection and automation experiments

This repository contains:

* `Rbt.py` → Main application
* `setup.py` → Automatic environment and dependency installer

---

# Requirements

## Supported Platforms

The project was designed to run on:

* Windows
* Linux
* macOS

Python 3.10 or newer is recommended.

---

# Installation

## Step 1 — Download the Files

Place both files in the same folder:

* `Rbt.py`
* `setup.py`

---

## Step 2 — Run the Setup Script

Open a terminal or command prompt inside the project folder and execute:

```bash
python setup.py
```

The setup script will:

* Create a local virtual environment
* Install all required Python packages
* Configure the environment automatically
* Keep dependencies isolated from your system installation

---

## Step 3 — Launch the Toolkit

After installation is complete:

### Windows

```bash
.venv\Scripts\python.exe Rbt.py
```

or activate the environment first:

```bash
.venv\Scripts\activate
python Rbt.py
```

### Linux / macOS

```bash
source .venv/bin/activate
python3 Rbt.py
```

---

# Project Structure

## Main Menu Categories

The toolkit is divided into multiple sections:

* Discord Tools
* OSINT Tools
* Utilities
* Website Tools

Each category contains independent modules accessible from the terminal menu.

---

# Tool Breakdown

## Discord Tools

### 01 — IP Grabber Script Generator

Generates configurable scripts intended for webhook-based networking experiments and controlled testing environments.

Features:

* Python output format
* Batch output format
* Webhook configuration
* Custom filename generation

Intended Use:

* Controlled lab testing
* Webhook integration experiments
* Educational networking demonstrations

This module should only be used in environments where every participant has explicitly authorized the test.

---

### 02 — Webhook Spammer

A threaded webhook stress-testing utility.

Features:

* Multi-thread support
* Delay control
* Connection validation
* Runtime controls
* Pause / Resume / Stop functionality

Intended Use:

* Load testing
* Webhook reliability checks
* Local automation testing

Do not use this module against third-party infrastructure without permission.

---

### 03 — Auto Spammer

Automated variant of the webhook testing module.

Features:

* Automated payload rotation
* Threaded delivery
* Timing controls

Intended strictly for internal testing environments.

---

### 04 — Discord Bot Sender

Basic Discord bot messaging utility.

Features:

* Bot token support
* Channel targeting
* Custom message delivery

Useful for:

* Automation testing
* Bot development
* API familiarization

---

### 05 — IP Grabber & Crasher (Windows)

shhhhh

No production stability should be expected.

---

# OSINT Tools

## 06 — IP Information Tool

Displays publicly available information associated with an IP address.

Potential Data:

* Country
* ASN
* ISP
* Region
* Host information

Useful for:

* Infrastructure research
* Debugging
* Network analysis

---

## 07 — Phone Information Tool

Performs analysis on phone numbers using public metadata and parsing libraries.

Features:

* International formatting
* Carrier lookup
* Country detection
* Validation checks
* Timezone information

Useful for:

* Contact verification
* OSINT workflows
* Data formatting validation

---

## 08 — IP Generator

Networking utility for generating and analyzing IP ranges.

Features:

* ASN range lookup
* Public IP retrieval
* Subnet calculations
* CIDR analysis

Useful for:

* Network labs
* Routing analysis
* Infrastructure studies

---

## 09 — Instagram OSINT

Attempts to collect publicly available profile information from Instagram.

Possible Data:

* Username
* Biography
* Followers
* Profile visibility
* Public metadata

Important:

Only publicly accessible information should be analyzed.

---

## 10 — Photo Metadata Tool

Extracts metadata from image files.

Features:

* EXIF extraction
* Camera information
* GPS coordinate detection
* Hash generation
* Image properties

Useful for:

* Digital forensics learning
* Metadata analysis
* File inspection

---

## 11 — Username Tracker

Searches for publicly accessible usernames across multiple platforms.

Features:

* Multi-platform checks
* Public profile discovery
* URL generation
* Basic account validation

Useful for:

* Brand monitoring
* Username availability checks
* OSINT workflows

---

## 12 — Email Tracker

Performs email formatting and domain analysis.

Features:

* Syntax validation
* MX record checks
* Domain inspection
* Provider identification

Useful for:

* Email verification
* Infrastructure research
* Mail configuration checks

---

# Utilities

## 15 — Base64 Encoder

Simple Base64 encoding utility.

Useful for:

* Data conversion
* API testing
* Payload formatting

---

# Website Tools

## 16 — Site Cloner

Experimental module currently under development.

Intended for:

* Web structure testing
* Frontend analysis
* Local learning environments

---

## 17 — Website Scanner

Website inspection and information gathering utility.

Potential Features:

* Header analysis
* Technology fingerprinting
* Basic infrastructure discovery

Still under development.

---

## 18 — Vulnerability Scanner

Experimental security analysis module.

Intended strictly for:

* Authorized testing
* Local development environments
* Educational labs

Never scan systems without explicit authorization.

---

# Dependency Information

The setup script automatically installs:

* requests
* pillow
* whois
* discord.py
* phonenumbers
* dnspython

Additional optional libraries may be required for some modules depending on platform and future updates.

---

# Important Notes

## Console Behavior

The toolkit uses:

* ANSI terminal coloring
* ASCII banners
* Threaded operations
* External API requests
* OS-specific behavior

Some modules may behave differently depending on:

* Operating system
* Installed packages
* Network configuration
* Firewall settings
* API availability

---

# Legal Notice

This project is provided strictly for educational, research, debugging, automation, and authorized security-testing purposes.

By using this software, you agree that:

* You are fully responsible for your own actions
* You will comply with local laws and regulations
* You will only interact with systems and services you own or are explicitly authorized to test
* You understand that misuse may violate laws, platform policies, or terms of service

The author of this project is not responsible for:

* Illegal usage
* Unauthorized access attempts
* Abuse of third-party services
* Damage caused by misuse
* Account suspensions or bans
* Data loss
* Network disruptions
* Any direct or indirect consequences resulting from the use of this software

Use this project entirely at your own risk.

If you do not understand the legal implications of cybersecurity tooling, do not use this software.

---

# Security & Ethics

A tool is not inherently malicious — misuse is.

Always:

* Obtain permission before testing systems
* Respect privacy and platform rules
* Avoid collecting data without consent
* Use isolated environments whenever possible
* Keep activities transparent and documented

Responsible use matters.

---

# Final Notes

This toolkit is currently in beta and under active development.

Some modules may:

* Be incomplete
* Change behavior between updates
* Produce unstable results
* Require additional dependencies
* Stop functioning if external services change APIs

Contributions, improvements, and bug reports are always appreciated.
