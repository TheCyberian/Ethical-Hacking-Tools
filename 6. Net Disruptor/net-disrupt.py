#!/usr/bin/env python

import netfilterqueue
import subprocess

queue_num = 0

def process_packet(packet):
    print(packet.get_payload())
    packet.drop()

#executing system calls
subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", str(queue_num)])
subprocess.call(["bash", "-c", "echo 1 > /proc/sys/net/ipv4/ip_forward"])

queue = netfilterqueue.NetfilterQueue()
queue.bind(queue_num, process_packet)
queue.run()
