import argparse
import ipaddress
from scapy.all import *
from scapy.layers.inet import IP, TCP


class ParametersGetter:

    @staticmethod
    def read_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="My range port scanner")
        parser.add_argument("address", help="IP address to scan")
        parser.add_argument("ports", help='Port range (e.g., 80-120)')
        args = parser.parse_args()
        return args

    @staticmethod
    def process_args() -> dict:
        raw_args = ParametersGetter.read_args()
        raw_subnet, raw_range = raw_args.address, raw_args.ports
        subnet = ParametersGetter.process_subnet(raw_subnet)

        if not ParametersGetter.validate_subnet(subnet):
            return {}

        left, right = raw_range.split('-')
        port_range = [i for i in range(int(left), int(right) + 1)]
        return {"subnet": subnet, "port_range": port_range}

    @staticmethod
    def validate_subnet(processed_subnet: str) -> bool:
        try:
            ipaddress.ip_network(processed_subnet)
        except ValueError as e:
            print(e)
            return False
        return True

    @staticmethod
    def process_subnet(raw_subnet: str) -> str:
        left_part, right_part = raw_subnet.split('/')
        left_part = left_part.split('.')
        if int(right_part) >= 24:
            left_part[-1] = '0'
        elif int(right_part) >= 16:
            left_part[-1] = left_part[-2] = '0'
        elif int(right_part) >= 8:
            left_part[-1] = left_part[-2] = left_part[-3] = '0'
        else:
            left_part = ['0'] * 4
        return '.'.join(left_part) + '/' + right_part


class PortScanner:
    def __init__(self):
        parameters = ParametersGetter().process_args()
        if not parameters:
            self.ready_to_work = False
            return
        self.subnet = ipaddress.ip_network(parameters["subnet"])
        self.port_range = parameters["port_range"]
        self.ready_to_work = True

    def scan_ports(self):
        if not self.ready_to_work:
            print("PortScanner is not configured")
            return

        for ip in self.subnet.hosts():
            ip = str(ip)
            print(f"Scanning ports of {ip} from {self.port_range[0]} to {self.port_range[-1]}...")
            answered, _ = sr(IP(dst=ip) / TCP(dport=self.port_range, flags="S"), verbose=0, timeout=2)
            if len(answered):
                open_ports = []
                for (s, _) in answered:
                    open_ports.append(s[TCP].dport)
                print("Open ports found: ", open_ports)
                print("-" * 200)
            else:
                print(f"No open ports of {ip} in range({self.port_range[0]} - {self.port_range[-1]})")
                print("-" * 200)


if __name__ == "__main__":
    MyPortScanner = PortScanner()
    MyPortScanner.scan_ports()
