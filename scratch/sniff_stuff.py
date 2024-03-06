# import scapy.all as scapy

import socket as soc
import time

from scapy.all import *

ARP_OPT_ARP_REQUEST = 1
ARP_OPT_ARP_REPLY = 2
ICMP_TYPE_ECHO_REQUEST = 8
ICMP_TYPE_ECHO_REPLY = 0
BROADCAST = "255.255.255.255"


def is_arp_rep_frame(frame):
    if frame[Ether].type == ETHER_TYPES.ARP:
        if frame[ARP].op == ARP_OPT_ARP_REQUEST:
            print(".", end="")
        else:
            print("\n" + frame[ARP].psrc)

    return (
        frame[Ether].type == ETHER_TYPES.ARP
        and frame[ARP].op == ARP_OPT_ARP_REPLY
    )


def print_arp_rep(frame):
    print(frame[ARP].psrc + "\t is at " + frame[ARP].hwsrc)


def arp_scan(ip_range="192.168.8.0/24"):
    # set up sniffing
    sniffer = AsyncSniffer(iface=conf.iface, prn=None, lfilter=is_arp_rep_frame)
    sniffer.start()

    # send arp requests
    requests = Ether(dst=ETHER_BROADCAST) / ARP(pdst=ip_range)
    sendp(requests, inter=0.005, verbose=False)

    # wait for scan to complete
    time.sleep(1)

    # stop sniffing
    results = sniffer.stop()

    # print results
    print("\n\n" + "=" * 100)
    for r in results:
        print_arp_rep(r)
    pass


def icmp_scan(ip_range="192.168.8.0/24"):
    requests = Ether(dst=ETHER_BROADCAST) / IP(dst=ip_range) / ICMP()
    ans, unans = sr(requests, timeout=2)
    pass


def send_arp_request(ip_dst="192.168.8.101"):
    ###############################################
    # Create an ARP request
    ###############################################
    p = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_dst)
    sendp(p)


def send_dns_request(domain_name="google.com", qtype="A"):
    ###############################################
    # Create a DNS request
    ###############################################
    dns_addr = "8.8.8.8"
    # dns_addr = "192.168.8.1"

    dns_req = (
        IP(dst=dns_addr)
        / UDP(dport=53)
        / DNS(rd=1, qd=DNSQR(qname=domain_name, qtype=qtype))
    )
    ans = sr1(dns_req)


def dhcp_release():
    server_ip = conf.route.route()[2].encode()
    client_ip = conf.iface.ip.encode()
    fam, client_mac = get_if_raw_hwaddr(conf.iface.name)
    hostname = b"als-acer"
    pkt = (
        IP(dst=server_ip)
        / UDP(sport=68, dport=67)
        / BOOTP(
            chaddr=client_mac,
            ciaddr=client_ip,
            xid=random.randint(0, 0xFFFFFFFF),
        )
        / DHCP(
            options=[
                ("message-type", "release"),
                ("server_id", server_ip),
                ("hostname", hostname),
                "end",
            ]
        )
        / Padding()
    )
    send(pkt)


def main():
    # arp_scan(ip_range)
    # icmp_scan(ip_range)
    # send_arp_request()
    # send_dns_request()

    gw_ip = conf.route.route("0.0.0.0")[2]
    gw_mac = getmacbyip(gw_ip)
    dst_ip = "192.168.0.101"
    dst_mac = getmacbyip(dst_ip)

    request = Ether(dst=dst_mac) / IP(dst=dst_ip) / ICMP()
    ans, unans = sr(request, timeout=1)

    request = Ether(dst=gw_mac) / IP(dst=dst_ip) / ICMP()
    ans, unans = sr(request, timeout=1)

    dhcp_release()

    pass


if __name__ == "__main__":
    main()
