import subprocess
import docker


def make_output_pretty(output: str):
    lines = output.splitlines()
    lines.pop(0)
    lines = [line for line in lines if not line.startswith(('exit', '!', 'end', 'frr', 'Current', 'Building'))]
    cleaned_output = '\n'.join(lines)
    return cleaned_output

def check_ping(topo_name: str, node_name: str, ip_to_check: str):
    """
    This function checks IP connectivity between two nodes in the topology.
    """
    client = docker.from_env()
    node = client.containers.get(f'clab-{topo_name}-{node_name}')
    print(f"Checking IP connectivity between {node_name} and node with ip {ip_to_check}")
    result = node.exec_run(cmd=f'bash -c "ping -c 4 {ip_to_check}"', stdout=True)
    print(make_output_pretty(result.output.decode()))


def check_tracert(topo_name: str, node_name: str, ip_to_check: str):
    """
    This function shows traceroute between two nodes in the topology.
    """
    client = docker.from_env()
    node = client.containers.get(f'clab-{topo_name}-{node_name}')
    print(f"Executing traceroute on {node_name} to address {ip_to_check}")
    result = node.exec_run(cmd=f'vtysh -c "traceroute {ip_to_check}"', stdout=True)
    print(make_output_pretty(result.output.decode()))


def parse_sh_run(node: str):
    client = docker.from_env()
    node = client.containers.get(f'clab-{topo_name}-{node}')
    print(f"Executing sh run command on {node.name}")
    result = node.exec_run(cmd=f'vtysh -c "sh run"', stdout=True)
    print(make_output_pretty(result.output.decode()))


def parse_sh_ip_route(node: str):
    client = docker.from_env()
    node = client.containers.get(f'clab-{topo_name}-{node}')
    print(f"Executing sh ip route command on {node.name}")
    result = node.exec_run(cmd=f'vtysh -c "sh ip route"', stdout=True)
    print(make_output_pretty(result.output.decode()))


def parse_sh_int_brief(node: str):
    client = docker.from_env()
    node = client.containers.get(f'clab-{topo_name}-{node}')
    print(f"Executing sh int brief command on {node.name}")
    result = node.exec_run(cmd=f'vtysh -c "sh int brief"', stdout=True)
    print(make_output_pretty(result.output.decode()))


def parse_command(command:str):
    """
    This function execute and parse the input command
    If command checks something about node, it should start with node name, e. g. PC1 sh run
    """
    if "docker ps" in command:
        print("Executing docker ps")
        docker_process = subprocess.run(['sudo', 'docker', 'ps'])
        print(docker_process.stdout)
    else:
        device_name, instruction = command.split(" ", 1)
        if instruction == "sh run":
            parse_sh_run(device_name)
        elif instruction == "sh ip route":
            parse_sh_ip_route(device_name)
        elif instruction == "sh int brief":
            parse_sh_int_brief(device_name)
        else:
            print(f"unknown command {command}")

if __name__ == '__main__':
    topo_name = "test0"
    check_ping(topo_name, 'PC1', '192.168.22.4')
    check_ping(topo_name, 'PC1', '192.168.33.4')

    check_ping(topo_name, 'PC2', '192.168.11.4')
    check_ping(topo_name, 'PC2', '192.168.33.4')

    check_ping(topo_name, 'PC3', '192.168.11.4')
    check_ping(topo_name, 'PC3', '192.168.22.4')

    check_tracert(topo_name, 'PC1', '192.168.22.4')
    parse_command("PC1 sh run")
    parse_command("PC1 sh ip route")
    parse_command("PC1 sh int brief")
    parse_command("docker ps")