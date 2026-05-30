# scanner.py — Main entry point for NetScanner
# Ties together host discovery, port scanning, and banner grabbing
#
# Usage examples:
#   python scanner.py -t scanme.nmap.org
#   python scanner.py -t 192.168.56.105 -p 1-65535
#   python scanner.py -t 192.168.56.0/24 --discover
#   python scanner.py -t 192.168.56.0/24 --discover -o report.json

import argparse
import json
from port_scan     import scan_ports
from banner_grab   import grab_banners
from host_discover import discover_hosts
from datetime      import datetime

def print_banner():
    print("""
  ╔══════════════════════════════════════╗
  ║        NETSCANNER  v1.0              ║
  ║        Red Team Recon Toolkit        ║
  ║   [!] For authorized testing only    ║
  ╚══════════════════════════════════════╝
    """)

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="NetScanner - Network Reconnaissance Tool"
    )
    parser.add_argument(
        '-t', '--target',
        required=True,
        help='Target IP, hostname, or subnet (e.g. 192.168.56.0/24)'
    )
    parser.add_argument(
        '-p', '--ports',
        default='1-1024',
        help='Port range to scan (default: 1-1024)'
    )
    parser.add_argument(
        '-o', '--output',
        default='report.json',
        help='Output JSON report file (default: report.json)'
    )
    parser.add_argument(
        '--discover',
        action='store_true',
        help='Run host discovery on subnet before scanning'
    )

    args = parser.parse_args()

    # Build results structure
    results = {
        'scan_time': datetime.now().isoformat(),
        'target':    args.target,
        'hosts':     []
    }

    # Step 1: Determine targets
    targets = []
    if args.discover:
        print(f"[*] Phase 1 — Host Discovery on {args.target}")
        print("-" * 45)
        targets = discover_hosts(args.target)
        print(f"[+] Found {len(targets)} live host(s)\n")
    else:
        targets = [args.target]

    # Parse port range
    start_port, end_port = map(int, args.ports.split('-'))

    # Step 2: Scan each target
    for host in targets:
        print(f"[*] Phase 2 — Port Scan on {host} ({args.ports})")
        print("-" * 45)
        open_ports = scan_ports(host, start_port, end_port)
        print(f"[+] {len(open_ports)} open port(s): {open_ports}\n")

        # Step 3: Banner grab
        print(f"[*] Phase 3 — Banner Grab on {host}")
        print("-" * 45)
        banners = grab_banners(host, open_ports)

        # Print results
        print(f"\n[+] Results for {host}:")
        for port, banner in banners.items():
            print(f"    {port:5}/tcp  open  {banner[:60]}")

        # Add to report
        results['hosts'].append({
            'ip':         host,
            'open_ports': open_ports,
            'services':   {str(k): v for k, v in banners.items()}
        })
        print()

    # Step 4: Save report
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"[+] Scan complete!")
    print(f"[+] Report saved → {args.output}")
    print(f"[+] Scanned {len(targets)} host(s) | "
          f"{sum(len(h['open_ports']) for h in results['hosts'])} open port(s) found")


if __name__ == '__main__':
    main()
