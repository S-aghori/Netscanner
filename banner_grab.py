# banner_grab.py — Service & version detection via banner grabbing

import socket

TIMEOUT = 2
# Probes sent to common ports to get a response
PROBES = {
    80:  b"GET / HTTP/1.0\r\nHost: target\r\n\r\n",
    443: b"GET / HTTP/1.0\r\nHost: target\r\n\r\n",
    21:  None,   # FTP sends banner on connect
    22:  None,   # SSH sends banner on connect
    25:  None,   # SMTP sends banner on connect
    110: None,   # POP3
    143: None,   # IMAP
    3306:None,   # MySQL
}

def grab_single(host, port):
    """
    Connect to host:port, optionally send a probe,
    and return the banner string.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((host, port))

        probe = PROBES.get(port, None)
        if probe:
            sock.send(probe)

        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner if banner else "open (no banner)"

    except (socket.error, UnicodeDecodeError, OSError):
        return "open (no banner)"

def grab_banners(host, open_ports):
    """
    Grab banners from all open ports.
    Returns dict: { port_number: banner_string }
    """
    banners = {}
    for port in open_ports:
        banner = grab_single(host, port)
        banners[port] = banner
    return banners

if __name__ == "__main__":
    import sys
    from port_scan import scan_ports

    target = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
    print(f"[*] Scanning ports on {target}...")
    open_ports = scan_ports(target, 1, 1024)
    print(f"[+] Open ports found: {open_ports}\n")

    print(f"[*] Grabbing banners...")
    banners = grab_banners(target, open_ports)

    for port, banner in banners.items():
        print(f"    Port {port:5} → {banner[:80]}")