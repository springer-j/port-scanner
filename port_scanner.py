'''
Program:        Port Scanner
Author:         Jake Springer
Date:           5/16/23
Purpose:        Scan open ports with Python
Python Vers:    3.11.3
'''
from subprocess import call # For clear
from socket import *
import time # Runtime information
import sys # sys.exit()
import os # os.path.exists(ports_file)
import nmap

start_time = time.time()
clear_mode = False # Don't clear terminal, used for screenshots
use_default_target = False # Always scan the default_target_ip
default_target_ip = '10.0.0.151' # dutiful raspberry pi
ports_file = "target_ports.txt" # Loaded ports to be scanned
most_common_ports = [ # Used for writing ports_file
    20,21,22,25,53,80,123,179,443,500,587,3389
]


def clear():
    try:
        if clear_mode: # Save output for screenshots
            print("\n")
        else:
            call("clear")
    except: # Cause critfail on windows
        return


def report(ip,ports,open):
    clear()
    print("-"* 50)
    print()
    print("\t ///  SCAN COMPLETE  ///\n")
    print("[>] HOST:                    ", ip)
    print("[>] TOTAL PORTS SCANNED:     ", len(ports))
    print("[>] OPEN PORTS FOUND:        ", len(open))
    print("[>] RUNTIME:                 ",time.time() - start_time)
    print()
    print("-"* 50)
    print()
    print("\t  /  Open Ports  / ")
    print()
    for p in open:
        print("[>] Port: " + p["port"])
        print(" >  Service:    " + p["name"])
        print(" >  Product:    " + p["product"])
        print(" >  Version:    " + p["version"])
        print(" >  Other info: " + p["misc"])
        print()
    print("-"* 50)
    input("\n[>] Press enter to return to menu ")


def get_ip():
    if use_default_target:
        return default_target_ip
    clear()
    while True:
        print("[~] Enter target")
        print("[~] Target can either be a URL or IPv4")
        print("[~] Example: site.com OR 10.10.10.10")
        entry = input("\n[?] ")
        try:
            target = gethostbyname(entry)
            return target
        except gaierror:
            print("\n[X] Bad URL/Service\n")


def scan(ip, ports): 
    # Returns dict of scan info from open ports
    if not ports:
        clear()
        print("[X] Scan failed: no ports provided.")
        input("[~] Press enter to return to menu.")
        main()
        return
    open_ports = []
    clear()
    print("[~] Scanning ports...")
    print("[~] Target IP:     ", ip)
    print("[~] Ports to scan: ", len(ports))
    print()
    scanner = nmap.PortScanner()
    for port in ports:
        print(f"[>] SCANNING PORT: {str(port)} ", end='',flush=True)
        scan = scanner.scan(ip, str(port))
        result = scan['scan'][ip]['tcp'][port]
        if result["state"] == 'open':
            port_data = {
                "port":str(port),
                "name":result["name"],
                "product":result["product"],
                "version":result["version"],
                "misc":result["extrainfo"]
            }
            print("=" * (40 - len(str(port))) + " OPEN")
            open_ports.append(port_data)
        else:
            print(("-" * (40 - len(str(port)))) + " CLOSED")
    return open_ports
        

def manual_scan(ip):
    # User enters target ports one by one
    ports = []
    clear()
    print("[~] Enter a port and press enter.")
    print("[~] Enter \"Q\" when finished.")
    print("[~] Enter \"cancel\" to return to menu.")
    print()
    while True:
        select = input("[?] ")
        if select.lower() == "q":
            open = scan(ip, ports)
            report(ip, ports, open)
            return
        elif select.lower() == "cancel":
            main()
            break
        else:
            ports.append(int(select))


def range_scan(ip):
    # User enters a range of ports to scan (start-stop)
    clear()
    print("[~] Starting range scan")
    while True:
        try:
            start_port = int(input("[?] Start port: "))
            end_port = int(input("[?] End port: "))
            break
        except ValueError:
            print("\n[X] Enter start/end ports as integers.\n")
            pass
    ports = [i for i in range(start_port, end_port + 1)]
    open = scan(ip, ports)
    report(ip, ports, open)
    return
    

def scan_from_file(ip):
    # Loads ports from ./target_ports.txt
    clear()
    # Big annoying loop for checking if file is present
    # and generating it if its not (and user agrees)
    if os.path.exists(ports_file):
        file = open(ports_file, 'r')
        print("[>] Loaded ports file")
    else: # If file doesn't exist: 
        print("\n[X] Ports file not found.")
        print("[~] Was looking for \"" + ports_file + "\"")
        while True: #! Kinda jank to have this loop here
            gen_conf = input("\n[Y/N] Generate file? ")
            # Write port file
            if gen_conf.lower() == 'y':
                with open(ports_file, 'w') as file:
                    for p in most_common_ports:
                        file.write(str(p) + '\n')
                    print("\n[>] Wrote to " + ports_file)
                    break
            else:
                return
        file = open(ports_file,'r')
        print("\n[>] Loaded ports file")
    # buckle up for this slick one-liner
    ports = [int(l.strip()) for l in file.readlines()] 
    print(f"[~] {str(len(ports))} ports in file.")
    while True:
        conf = input("\n[Y/N] Contine? ")
        if conf.lower() == 'y':
            open_ports = scan(ip, ports)
            report(ip, ports, open_ports)
            return open
        return


def main():
    # Main menu
    ip = get_ip()
    while True:
        clear()
        print(f"\n[>] Target: {ip}\n")
        print("[1]. Manual ports")
        print("[2]. Scan from range")
        print("[3]. Scan from file")
        print("[Q]. Exit")
        select = input("\n[?] ")
        if select.lower() == 'q':
            sys.exit()
        elif select == '1':
            manual_scan(ip)
        elif select == '2':
            range_scan(ip)
        elif select == '3':
            scan_from_file(ip)


try:    
    main()
except KeyboardInterrupt:
    clear()
    sys.exit()