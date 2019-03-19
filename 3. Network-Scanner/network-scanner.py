#!/usr/bin/env python

import scapy.all as scapy
from optparse import OptionParser
from pyfiglet import Figlet
from termcolor import cprint

def scan(ip_addr):
    arp_req = scapy.ARP(pdst=ip_addr)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast/arp_req
    arp_answered, arp_unanswered = scapy.srp(arp_broadcast, timeout=1, verbose=False)

    clients_list = []
    for element in arp_answered:
        client_dict = {'ip':element[1].psrc, 'mac':element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_output(result_set):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for client in result_set:
        print(client["ip"] +"\t\t"+ client["mac"])
    print("------------------------------------------")


def get_arguments():
    command_parser = OptionParser()
    command_parser.add_option("-t", "--target", dest="target", help="Target IP address or Subnet in CIDR notation.")
    options = command_parser.parse_args()[0]
    if not options.target:
        command_parser.error("[-] Please specify a target, use --help for more info...")
    return options

def print_banner(text):
    print("-" * 42)
    cprint(Figlet().renderText(text), 'white', attrs=['bold'])
    print("-" * 42)


print_banner("net : scan")
option = get_arguments()
scan_res = scan(option.target)
print_output(scan_res)
