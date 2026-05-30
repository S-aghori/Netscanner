# port_scan.py — Threaded TCP port scanner

import socket
import threading
from queue import Queue

THREAD_COUNT = 100    # concurrent threads
TIMEOUT      = 0.5    # seconds per port

def tcp_connect(host, port, results):
    """Try a TCP connect to host:port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((host, port))
        if result == 0:
            results.append(port)
        sock.close()
    except (socket.error, OSError):
        pass

def worker(host, queue, results):
    """Thread worker — pulls ports from queue"""
    while not queue.empty():
        port = queue.get()
        tcp_connect(host, port, results)
        queue.task_done()

def scan_ports(host, start_port=1, end_port=1024):
    """
    Scan a range of TCP ports on host.
    Returns a sorted list of open port numbers.
    """
    queue   = Queue()
    results = []
    threads = []

    # Fill queue with port numbers to scan
    for port in range(start_port, end_port + 1):
        queue.put(port)

    # Spawn worker threads
    for _ in range(THREAD_COUNT):
        t = threading.Thread(
            target=worker,
            args=(host, queue, results)
        )
        t.daemon = True
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    return sorted(results)

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
    start  = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end    = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    print(f"[*] Scanning {target}...")
    open_ports = scan_ports(target, 1, 1024)
    print(f"[+] Open ports: {open_ports}")