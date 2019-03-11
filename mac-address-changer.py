#!/usr/bin/env python

import subprocess
from optparse import OptionParser
import re


def change_mac_address(interface, new_mac_address):
    print("[+] Changing MAC Address for "+interface+" to "+new_mac_address+" ...")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_arguments():
    command_parser = OptionParser()
    command_parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    command_parser.add_option("-m", "--mac", dest="new_mac_address", help="New MAC address")
    (options, args) = command_parser.parse_args()
    if not options.interface:
        command_parser.error("[-] Please specify an interface, use --help for more info...")
    elif not options.new_mac_address:
        command_parser.error("[-] Please specify a new MAC, use --help for more info...")
    return options

def current_mac_lookup(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    search_result = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if search_result:
        return search_result.group(0)
    else:
        print("[-] Could not read MAC Address...")

options = get_arguments()
current_mac = current_mac_lookup(options.interface)
print("[+] Current MAC = "+str(current_mac))
change_mac_address(options.interface, options.new_mac_address)
current_mac = current_mac_lookup(options.interface)
print("[+] Current MAC = "+current_mac)
if current_mac == options.new_mac_address:
    print("[+] MAC address was changed successfully...")
else:
    print("[-] MAC address update failed !!!")
