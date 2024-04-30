from scapy.all import *

def packet_callback(packet):
    print("Packet received")

    print(packet[IP].src)
    if ICMP in packet and packet[ICMP].type == 8:
        reply = IP(dst=packet[IP].src)/ICMP(type=0, id=packet[ICMP].id, seq=packet[ICMP].seq)/packet[Raw].load
        send(reply)
        print("Reply sent")

sniff(iface="tap0", prn=packet_callback)