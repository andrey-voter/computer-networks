import argparse

from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6


class ParametersGetter:

    @staticmethod
    def read_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="MyMTR")
        parser.add_argument("destination", help="Destination for the traceroute")
        parser.add_argument("-ip", "--ip-version", type=int, default=4, help="Which IP version to use: 4 or 6")
        parser.add_argument("-p", "--protocol", type=str, default="TCP", help="Which protocol to use: TCP, UDP, ICMP")
        parser.add_argument("-m", "--max-hops", type=int, default=28, help="Max number of hops to reach destination")
        parser.add_argument("-t", "--timeout", type=int, default=2, help="Time waiting for each packet")
        arguments = parser.parse_args()
        return arguments


class MyMTR:
    def __init__(self, destination: str = "google.com", IPv4: bool = True, protocol: str = "TCP", max_hops: int = 28,
                 timeout: int = 2):
        self.destination = destination
        self.supported_protocols = ("TCP", "UDP", "ICMP")
        self.default_protocol = self.supported_protocols[0]
        self.IPv4 = IPv4
        if protocol in self.supported_protocols:
            self.protocol = protocol
        else:
            self.protocol = self.default_protocol
        self.max_hops = max_hops
        self.timeout = timeout

    def set_protocol(self, protocol: str):
        self.protocol = protocol

    def use_IPv4(self):
        self.IPv4 = True

    def use_IPv6(self):
        self.IPv4 = False

    def set_destination(self, new_destination):
        self.destination = new_destination

    def set_max_hops(self, new_max_hops):
        self.max_hops = new_max_hops

    def set_timeout(self, new_timeout):
        self.timeout = new_timeout

    def traceroute(self):
        lost_packets = defaultdict(int)
        ttl = 1
        while True:
            if self.IPv4:
                ip_packet = IP(dst=self.destination, ttl=ttl)
            else:
                ip_packet = IPv6(dst=self.destination, hlim=ttl)

            if self.protocol == "UDP":
                lower_layer_packet = UDP(dport=33434)
            elif self.protocol == "TCP":
                lower_layer_packet = TCP(dport=80, flags="S")
            else:
                lower_layer_packet = ICMP()

            stacked_packet = ip_packet / lower_layer_packet
            # Sending packet and waiting for the reply
            reply = sr1(stacked_packet, timeout=self.timeout, verbose=0)

            if reply is None:
                # There can be no reply in case of different situations, such as firewall settings and others.
                # We can do nothing here
                lost_packets[ttl] += 1
                print(f"Hop {ttl}\t* * *")
            elif reply.type == 3:
                # We reached destination
                print(f"Hop {ttl}\t{reply.src}")
                break
            else:
                # Here we are somewhere between source and destination
                print(f"Hop {ttl}\t{reply.src}")

            ttl += 1

            if ttl > self.max_hops:
                # If we reached max_hops we need to stop
                break
        print("-" * 100)
        print("Lost packets statistics:")
        for hop, lost_count in lost_packets.items():
            print(f"Hop {hop}: {lost_count} packet(s) lost")


if __name__ == "__main__":
    args = ParametersGetter.read_args()
    my_mtr = MyMTR(args.destination, args.ip_version == 4, args.protocol, args.max_hops, args.timeout)
    my_mtr.traceroute()

# Usage example:
# sudo python3 my_mtr.py "google.com" -p ICMP -m 15 -t 1
