#!/usr/bin/env python

import socket
from optparse import OptionParser
import sys
from datetime import datetime
from pyfiglet import Figlet
from termcolor import cprint

def print_output(result_set):
    print "-"*60
    print "Scanning the Host... Please wait..."
    print "-"*60
    for port in result_set:
         print "Port {} : Open".format(port)
    print "_"*60


def get_arguments():
    command_parser = OptionParser()
    command_parser.add_option("-a", "--address", dest="remoteHost", help="Remote Host address.")
    options = command_parser.parse_args()[0]
    if not options.remoteHost:
        command_parser.error("[-] Please specify a remote host, use --help for more info...")
    return options


def scanHost(remoteHostIP):
    ports_list = []
    try:
        for p in range(1,1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            res = sock.connect_ex((remoteHostIP, p))
            if res == 0:
                ports_list.append(p)
                sock.close()
            else:
                sock.close()
	return ports_list

    except KeyboardInterrupt:
        print "Program interrupted... Aborting the scan..."
        sys.exit()

    except socket.gaierror:
        print "Host name couldn't be resolved... Aborting..."
        sys.exit()

    except socket.errot:
        print "Could not connect to server... Host may be down..."
        sys.exit()



# subprocess.call('clear', shell=True)
def print_banner(text):
    print("-" * 50)
    cprint(Figlet().renderText(text), 'blue', attrs=['bold'])
    print("-" * 50)


print_banner("port : scan")
option = get_arguments()
remoteHostIP = socket.gethostbyname(option.remoteHost)
# remoteHost = raw_input("Enter a remote host to scan: ")
t1 = datetime.now()
results = scanHost(remoteHostIP)
print_output(results)
t2 = datetime.now()
print "Scan completed in: ", t2 - t1
