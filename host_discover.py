# host_discover.py — Ping sweep to find live hosts on a subnet
# Usage: python host_discover.py 192.168.56.0/24

import subprocess
import ipaddress
import threading
from queue import Queue

THREAD_COUNT = 50
TIMEOUT      = 1

def ping_host(ip, results):
    """Ping a single IP. Adds to results list if host is alive."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(TIMEOUT), str(ip)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            results.append(str(ip))
            print(f"    [+] Host up: {ip}")
    except subprocess.SubprocessError:
        pass

def worker(queue, results):
    """Thread worker — pulls IPs from queue and pings them."""
    while not queue.empty():
        ip = queue.get()
        ping_host(ip, results)
        queue.task_done()

def discover_hosts(subnet):
    """
    Ping sweep an entire subnet.
    Example: discover_hosts('192.168.56.0/24')
    Returns a sorted list of live host IPs.
    """
    queue   = Queue()
    results = []
    threads = []

    # Generate all host IPs in the subnet (excludes .0 and .255)
    network = ipaddress.ip_network(subnet, strict=False)
    all_ips = list(network.hosts())

    print(f"[*] Scanning {len(all_ips)} hosts in {subnet}...")

    # Load all IPs into queue
    for ip in all_ips:
        queue.put(ip)

    # Spawn worker threads
    for _ in range(min(THREAD_COUNT, len(all_ips))):
        t = threading.Thread(target=worker, args=(queue, results))
        t.daemon = True
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Sort IPs in correct numeric order
    return sorted(results, key=lambda x: ipaddress.ip_address(x))


if __name__ == "__main__":
    import sys

    subnet = sys.argv[1] if len(sys.argv) > 1 else "192.168.56.0/24"

    print(f"[*] Starting host discovery on {subnet}")
    print(f"[*] Using {THREAD_COUNT} threads, {TIMEOUT}s timeout\n")

    live_hosts = discover_hosts(subnet)

    print(f"\n[+] Discovery complete!")
    print(f"[+] {len(live_hosts)} live host(s) found:")
    for host in live_hosts:
        print(f"    → {host}")