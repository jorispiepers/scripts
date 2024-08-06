import time
import socket

def scan(target, ports):
    newline = '\n'
    print(f"{newline}Starting scan for {target}")

    tick = time.perf_counter()
    sock = socket.socket()
    for port in range(1, ports + 1):
        scan_port(target, port, sock)

    sock.close()
    print(f"{newline}Time used to scan all ports, {time.perf_counter() - tick:.4f} seconds.")

def scan_port(ipaddress, port, sock):
    try:
        sock.connect((ipaddress, port))
        print(f"[+] Port on {ipaddress} opened {port}")
    except:
        print(f"[-] Port on {ipaddress} closed {port}")
        #pass

def main():
    targets = input("[*] Enter targets to scan (split them by ,): ")
    ports = int(input("[*] Enter how many ports you want to scan: "))
    if ',' in targets:
        print(("[*] Scanning multiple targets"))
        for ip_addr in targets.split(','):
            scan(ip_addr.strip(' '), ports)
    else:
        scan(targets, ports)

if __name__ == "__main__":
    main()