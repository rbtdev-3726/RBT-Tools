RBT Toolkit is a multi-purpose Python-based console utility designed for educational, testing, automation, and OSINT-oriented workflows. The toolkit combines multiple modules into a single terminal interface, allowing users to perform network analysis, metadata inspection, automation tasks, encoding utilities, and public-information gathering from multiple sources. The project is intended for educational and research environments, cybersecurity learning labs, local testing and debugging, OSINT workflows, network and infrastructure analysis, and metadata inspection experiments.

The repository contains two main files: Rbt.py, which is the main application, and setup.py, which automatically installs the environment and dependencies. The toolkit supports Windows, Linux, and macOS, and Python 3.10 or newer is recommended.

To install the project, place both files in the same folder and run “python setup.py” inside the project directory. The setup script creates a local virtual environment, installs all required Python packages, configures the environment automatically, and keeps dependencies isolated from the system installation. After installation, the toolkit can be launched using the virtual environment on Windows, Linux, or macOS systems.

The toolkit is divided into several categories including Discord Tools, OSINT Tools, Utilities, and Website Tools. Each section contains independent modules accessible through the terminal menu.

The Discord Tools section includes multiple utilities. The IP Grabber Script Generator creates configurable scripts for webhook-based networking experiments and controlled testing environments. It supports Python and Batch output formats, webhook configuration, and custom filename generation. This module is intended only for controlled lab testing, webhook integration experiments, and educational networking demonstrations where all participants have explicitly authorized the test.

The Webhook Spammer is a threaded webhook stress-testing utility that includes multi-thread support, delay controls, connection validation, runtime controls, and pause, resume, and stop functionality. It is intended for load testing, webhook reliability checks, and local automation testing only. It should never be used against third-party infrastructure without authorization.

The Auto Spammer is an automated variant of the webhook testing module and supports automated payload rotation, threaded delivery, and timing controls. It is intended strictly for internal testing environments.

The Discord Bot Sender is a basic Discord bot messaging utility that supports bot tokens, channel targeting, and custom message delivery. It is useful for automation testing, bot development, and API familiarization.

The IP Grabber & Crasher module for Windows is experimental and no production stability should be expected.

The OSINT Tools section contains several analysis utilities. The IP Information Tool displays publicly available information associated with an IP address, including country, ASN, ISP, region, and host information. It is useful for infrastructure research, debugging, and network analysis.

The Phone Information Tool performs analysis on phone numbers using public metadata and parsing libraries. It supports international formatting, carrier lookup, country detection, validation checks, and timezone information. It is useful for contact verification, OSINT workflows, and data formatting validation.

The IP Generator is a networking utility for generating and analyzing IP ranges. Features include ASN range lookup, public IP retrieval, subnet calculations, and CIDR analysis. It is useful for network labs, routing analysis, and infrastructure studies.

The Instagram OSINT module attempts to collect publicly available profile information from Instagram such as usernames, biographies, follower counts, profile visibility, and other public metadata. Only publicly accessible information should be analyzed.

The Photo Metadata Tool extracts metadata from image files. Features include EXIF extraction, camera information, GPS coordinate detection, hash generation, and image property analysis. It is useful for digital forensics learning, metadata analysis, and file inspection.

The Username Tracker searches for publicly accessible usernames across multiple platforms. It supports multi-platform checks, public profile discovery, URL generation, and basic account validation. It is useful for brand monitoring, username availability checks, and OSINT workflows.

The Email Tracker performs email formatting and domain analysis. Features include syntax validation, MX record checks, domain inspection, and provider identification. It is useful for email verification, infrastructure research, and mail configuration checks.

The Utilities section currently includes a Base64 Encoder used for data conversion, API testing, and payload formatting.

The Website Tools section includes several experimental modules. The Site Cloner is intended for web structure testing, frontend analysis, and local learning environments. The Website Scanner is a website inspection and information gathering utility that may support header analysis, technology fingerprinting, and infrastructure discovery. The Vulnerability Scanner is an experimental security analysis module intended strictly for authorized testing, local development environments, and educational labs. Systems should never be scanned without explicit authorization.

The setup script automatically installs several dependencies including requests, pillow, whois, discord.py, phonenumbers, and dnspython. Additional optional libraries may be required depending on platform compatibility and future updates.

The toolkit uses ANSI terminal coloring, ASCII banners, threaded operations, external API requests, and OS-specific behavior. Some modules may behave differently depending on the operating system, installed packages, network configuration, firewall settings, and API availability.

This project is provided strictly for educational, research, debugging, automation, and authorized security-testing purposes. By using this software, users agree that they are fully responsible for their own actions, will comply with local laws and regulations, will only interact with systems and services they own or are explicitly authorized to test, and understand that misuse may violate laws, platform policies, or terms of service.

The author of the project is not responsible for illegal usage, unauthorized access attempts, abuse of third-party services, damage caused by misuse, account suspensions or bans, data loss, network disruptions, or any direct or indirect consequences resulting from the use of the software. Users operate the project entirely at their own risk. Anyone who does not understand the legal implications of cybersecurity tooling should not use the software.

The toolkit emphasizes responsible and ethical usage. Users should always obtain permission before testing systems, respect privacy and platform rules, avoid collecting data without consent, use isolated environments whenever possible, and keep activities transparent and documented.

The toolkit is currently in beta and under active development. Some modules may be incomplete, change behavior between updates, produce unstable results, require additional dependencies, or stop functioning if external services modify their APIs. Contributions, improvements, and bug reports are always appreciated.
