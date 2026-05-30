# cve_lookup.py — Auto CVE suggestions based on banner info
# Matches service banners to known CVEs and Metasploit modules

import re
import json

CVE_DB = {
    # FTP
    'vsftpd 2.3.4': {
        'cve':       'CVE-2011-2523',
        'severity':  'CRITICAL',
        'desc':      'vsftpd 2.3.4 backdoor — gives instant root shell',
        'msf':       'exploit/unix/ftp/vsftpd_234_backdoor',
        'port':      21
    },
    # SSH
    'openssh 4.7': {
        'cve':       'CVE-2008-0166',
        'severity':  'HIGH',
        'desc':      'OpenSSH weak key generation on Debian/Ubuntu',
        'msf':       'exploit/linux/ssh/debian_openssh_integer_overflow',
        'port':      22
    },
    'openssh 3.': {
        'cve':       'CVE-2002-0639',
        'severity':  'CRITICAL',
        'desc':      'OpenSSH 3.x remote root exploit',
        'msf':       'exploit/unix/ssh/openssh_memory_corruption',
        'port':      22
    },
    # HTTP
    'apache/2.2.8': {
        'cve':       'CVE-2012-0053',
        'severity':  'MEDIUM',
        'desc':      'Apache 2.2.x header injection vulnerability',
        'msf':       'auxiliary/scanner/http/apache_optionsbleed',
        'port':      80
    },
    'apache/2.4.7': {
        'cve':       'CVE-2017-9798',
        'severity':  'HIGH',
        'desc':      'Apache Optionsbleed — memory leak via OPTIONS method',
        'msf':       'auxiliary/scanner/http/apache_optionsbleed',
        'port':      80
    },
    # Samba
    'samba 3.': {
        'cve':       'CVE-2007-2447',
        'severity':  'CRITICAL',
        'desc':      'Samba 3.x usermap_script — remote root command injection',
        'msf':       'exploit/multi/samba/usermap_script',
        'port':      445
    },
    # MySQL
    'mysql 5.0': {
        'cve':       'CVE-2012-2122',
        'severity':  'HIGH',
        'desc':      'MySQL 5.x authentication bypass — root with no password',
        'msf':       'auxiliary/scanner/mysql/mysql_login',
        'port':      3306
    },
    # Telnet
    'telnet': {
        'cve':       'CVE-1999-0619',
        'severity':  'HIGH',
        'desc':      'Telnet sends all data in plaintext including passwords',
        'msf':       'auxiliary/scanner/telnet/telnet_login',
        'port':      23
    },
    # Nginx
    'nginx/1.': {
        'cve':       'CVE-2021-23017',
        'severity':  'HIGH',
        'desc':      'Nginx 1.x resolver buffer overflow',
        'msf':       'N/A — manual exploit required',
        'port':      80
    },
    # PHP
    'php/5.': {
        'cve':       'CVE-2012-1823',
        'severity':  'CRITICAL',
        'desc':      'PHP CGI argument injection — remote code execution',
        'msf':       'exploit/multi/http/php_cgi_arg_injection',
        'port':      80
    },
}

SEVERITY_COLOR = {
    'CRITICAL': '🔴 CRITICAL',
    'HIGH':     '🟠 HIGH',
    'MEDIUM':   '🟡 MEDIUM',
    'LOW':      '🟢 LOW',
    'INFO':     '🔵 INFO',
}

def lookup_banner(port, banner):
    """
    Check a single banner against CVE database.
    Returns list of matching CVE dicts.
    """
    matches = []
    banner_lower = banner.lower()

    for signature, cve_info in CVE_DB.items():
        if signature.lower() in banner_lower:
            matches.append({
                'port':     port,
                'banner':   banner[:80],
                'cve':      cve_info['cve'],
                'severity': cve_info['severity'],
                'desc':     cve_info['desc'],
                'msf':      cve_info['msf'],
            })

    return matches


def lookup_all(banners):
    """
    Check all banners from a scan.
    banners = { port: banner_string }
    Returns list of all CVE matches found.
    """
    all_findings = []

    for port, banner in banners.items():
        findings = lookup_banner(port, banner)
        all_findings.extend(findings)

    return all_findings

def print_findings(findings, host):
    """Print CVE findings in a clean readable format."""

    if not findings:
        print(f"    [*] No known CVEs found for {host}")
        return

    print(f"\n{'='*55}")
    print(f"  CVE FINDINGS FOR {host}")
    print(f"{'='*55}")

    for f in findings:
        sev = SEVERITY_COLOR.get(f['severity'], f['severity'])
        print(f"""
  [{sev}]
  Port    : {f['port']}/tcp
  Banner  : {f['banner']}
  CVE     : {f['cve']}
  Detail  : {f['desc']}
  Exploit : {f['msf']}
  {'─'*50}""")

    print(f"\n  [!] Total vulnerabilities found: {len(findings)}")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    import sys
    from port_scan import scan_ports
    from banner_grab import grab_banners

    target = sys.argv[1] if len(sys.argv) > 1 else "192.168.56.200"

    print(f"[*] Scanning {target}...")
    ports   = scan_ports(target, 1, 65535)
    banners = grab_banners(target, ports)

    findings = lookup_all(banners)
    print_findings(findings, target)

    with open("cve_report.json", "w") as f:
        json.dump(findings, f, indent=2)
    print("[+] CVE report saved → cve_report.json")