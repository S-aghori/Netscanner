# 🔴 NetScanner v1.0 — Red Team Network Recon Toolkit

> Built as part of OSCP preparation. A fully functional network reconnaissance and vulnerability identification toolkit written in Python from scratch — then used to fully compromise a real lab target.

![Python](https://img.shields.io/badge/Python-3.x-00ff9d?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=flat-square&logo=kali-linux)
![Purpose](https://img.shields.io/badge/Purpose-OSCP%20Prep-red?style=flat-square)
![License](https://img.shields.io/badge/License-Educational-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

---

## ⚠️ Disclaimer
> This tool is for **authorized penetration testing and educational purposes only.**
> Only use against systems you own or have explicit written permission to test.
> All testing shown was performed in a controlled VirtualBox lab on Metasploitable2.

---

## 🎯 What This Tool Does

NetScanner automates the complete OSCP recon methodology in one pipeline:

```
Host Discovery → Port Scan → Banner Grab → CVE Lookup → Exploit → HTML Report
```

---

## 📸 Screenshots

### 1. Scanner Running — 12 Open Ports Found
![Scanner Running](screenshots/The_Scanner_Running.png)

### 2. CVE Lookup — Auto Vulnerability Detection
![CVE Lookup](screenshots/CVE_Lookup_Output.png)

### 3. ROOT Shell — uid=0(root)
![ROOT Shell](screenshots/ROOT_Shell.png)

### 4. Password Cracking — /etc/shadow Dumped
![Password Cracking](screenshots/Password_Cracking.png)

### 5. HTML Pentest Report — Auto Generated
![HTML Report](screenshots/HTML_Pentest_Report.png)

---

## 🛠️ Project Structure

```
netscanner/
  ├── scanner.py          ← Main CLI entry point (ties everything together)
  ├── host_discover.py    ← Multithreaded ping sweep
  ├── port_scan.py        ← 100-thread TCP port scanner
  ├── banner_grab.py      ← Service & version detection
  ├── cve_lookup.py       ← Auto CVE matching from banners
  ├── report_gen.py       ← Professional HTML report generator
  └── screenshots/        ← Lab proof screenshots
```

---

## ⚙️ Requirements

No external libraries needed — uses Python standard library only!

```bash
python3 --version   # Python 3.6+
```

---

## 🚀 Usage

### Full scan with host discovery
```bash
python scanner.py -t 192.168.56.0/24 --discover -o report.json
```

### Scan single target
```bash
python scanner.py -t 192.168.56.200 -p 1-1024 -o results.json
```

### Scan full port range
```bash
python scanner.py -t 192.168.56.200 -p 1-65535 -o full.json
```

### Run individual modules
```bash
# Host discovery
python host_discover.py 192.168.56.0/24

# Port scan
python port_scan.py 192.168.56.200

# Banner grab
python banner_grab.py 192.168.56.200

# CVE lookup
python cve_lookup.py 192.168.56.200

# Generate HTML report
python report_gen.py
```

---

## 📊 Sample Output

```
╔══════════════════════════════════════╗
║        NETSCANNER  v1.0              ║
║        Red Team Recon Toolkit        ║
║   [!] For authorized testing only    ║
╚══════════════════════════════════════╝

[*] Phase 1 — Host Discovery on 192.168.56.0/24
    [+] Host up: 192.168.56.200
[+] Found 1 live host

[*] Phase 2 — Port Scan on 192.168.56.200 (1-1024)
[+] 12 open port(s): [21, 22, 23, 25, 53, 80, 111, 139, 445, 512, 513, 514]

[*] Phase 3 — Banner Grab on 192.168.56.200
    21/tcp  open  220 (vsFTPd 2.3.4)
    22/tcp  open  SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
    80/tcp  open  HTTP/1.1 200 OK Server: Apache/2.2.8

[+] Scan complete! Report saved → report.json
```

### CVE Lookup Output
```
══════════════════════════════════════════════════════
  CVE FINDINGS FOR 192.168.56.200
══════════════════════════════════════════════════════

  [🔴 CRITICAL]
  Port    : 21/tcp
  Banner  : 220 (vsFTPd 2.3.4)
  CVE     : CVE-2011-2523
  Detail  : vsftpd 2.3.4 backdoor — gives instant root shell
  Exploit : exploit/unix/ftp/vsftpd_234_backdoor

  [🔴 CRITICAL]
  Port    : 445/tcp
  CVE     : CVE-2007-2447
  Detail  : Samba 3.x usermap_script — remote root command injection
  Exploit : exploit/multi/samba/usermap_script

  [!] Total vulnerabilities found: 3
══════════════════════════════════════════════════════
```

---

## ⚔️ Lab Results — Metasploitable2

Tested against Metasploitable2 in a controlled VirtualBox lab:

| Port | Service | Version | CVE | Result |
|---|---|---|---|---|
| 21 | FTP | vsftpd 2.3.4 | CVE-2011-2523 | ✅ ROOT shell via backdoor |
| 22 | SSH | OpenSSH 4.7p1 | CVE-2008-0166 | ✅ Identified |
| 80 | HTTP | Apache 2.2.8 | CVE-2012-0053 | ✅ Identified |
| 445 | Samba | 3.0.20 | CVE-2007-2447 | ✅ ROOT shell |
| 1524 | Backdoor | — | — | ✅ Instant ROOT via netcat |
| 3306 | MySQL | 5.0.51a | — | ✅ No password login |
| shadow | Passwords | md5crypt | — | ✅ 3 passwords cracked |

---

## 🧠 Concepts Learned

| Concept | Where Used |
|---|---|
| TCP Sockets | port_scan.py, banner_grab.py |
| Multithreading | host_discover.py, port_scan.py |
| Subprocess | host_discover.py (ping sweep) |
| String matching | cve_lookup.py |
| JSON handling | scanner.py, report_gen.py |
| HTML generation | report_gen.py |
| OSCP methodology | Full pipeline |
| CVE research | cve_lookup.py |
| Password cracking | John the Ripper + rockyou.txt |

---

## 🗺️ OSCP Methodology Map

```
Phase 1 → host_discover.py   Recon          ✅
Phase 2 → port_scan.py       Enumeration    ✅
Phase 3 → banner_grab.py     Service ID     ✅
Phase 4 → cve_lookup.py      Vuln Research  ✅
Phase 5 → Metasploit         Exploitation   ✅ (ROOT)
Phase 6 → Post Exploitation  Loot           ✅ (/etc/shadow)
Phase 7 → report_gen.py      Reporting      ✅
```

---

## 🔮 Planned Upgrades

- [ ] SYN stealth scanning with Scapy
- [ ] OS fingerprinting via TTL analysis
- [ ] NVD API integration for live CVE lookup
- [ ] UDP port scanning
- [ ] Automatic Metasploit module suggestions
- [ ] CVSS score integration

---

## 📁 Related

- 🔗 Medium write-up: [Full article on how I built and used this tool]
- 🔗 Project 1: [Previous cybersecurity project]
- 🔗 LinkedIn: [S-aghori]

---

## 👤 Author

**S-aghori** — Cybersecurity student preparing for OSCP
Building projects in public to document the journey.

---

*Built on Kali Linux | Tested on Metasploitable2 | For educational use only*
