import subprocess
import yaml
import docker


def generate_topology(topo_name: str, num_routers: int, num_pcs: int, links: list) -> dict:
    """
    This function generates topology whish should be dumped in .yml file
    The topology pattern is like this:
        PC1 -- R1 --- R2 -- PC2
                |  /
                | /
                R3 -- PC3
    So, number of routers should be equal to number of PCs
    """
    assert num_routers == num_pcs, 'Number of routers should be equal to number of PC\'s'
    topology = {'name': topo_name, 'topology': {'nodes': {}, 'links': []}}
    for i in range(1, num_routers + 1):
        topology['topology']['nodes'][f'router{i}'] = {'kind': 'linux', 'image': 'frrouting/frr:latest',
                                                       'binds': ['daemons:/etc/frr/daemons']}
    for i in range(1, num_pcs + 1):
        topology['topology']['nodes'][f'PC{i}'] = {'kind': 'linux', 'image': 'frrouting/frr:latest',
                                                   'binds': ['daemons:/etc/frr/daemons']}
    for link in links:
        topology['topology']['links'].append({'endpoints': link})
    return topology


def configure_topology(topology: dict) -> None:
    """
    This function configures existing topology (assigns IP-addresses etc.)

    !!! Before running the function, make sure that you have already generated topo via generate_topology() and started clab via "sudo clab deploy --topo topo_name.yml"  !!!
    """

    def configure_node(node: str):
        node_name = node
        if node_name == 'router1':
            print("configuring router1...")
            container = client.containers.get(f'clab-{topo_name}-router1')
            container.exec_run(cmd='vtysh -c "conf" '
                                   '-c "router isis 1" '
                                   '-c "is-type level-2-only" '
                                   '-c "net 49.0001.1000.0000.1001.00" '
                                   '-c "q" '
                                   '-c "int lo0" '
                                   '-c "ip router isis 1" '
                                   '-c "isis passive" '
                                   '-c "q" '
                                   '-c "int eth1" '
                                   '-c "ip addr 192.168.1.1/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "q" '
                                   '-c "int eth2" '
                                   '-c "ip addr 192.168.2.1/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "q" '
                                   '-c "int eth3" '
                                   '-c "ip addr 192.168.11.1/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "do wr"', stdout=True, stderr=True, tty=True, privileged=True)

            print("finished configuring router1!")
        elif node_name == 'router2':
            print("configuring router2...")
            container = client.containers.get(f'clab-{topo_name}-router2')
            container.exec_run(cmd='vtysh -c "conf" '
                                   '-c "router isis 1" '
                                   '-c "is-type level-2-only" '
                                   '-c "net 49.0001.2000.0000.2000.00" '
                                   '-c "q" '
                                   '-c "int lo0" '
                                   '-c "ip router isis 1" '
                                   '-c "isis passive" '
                                   '-c "q" '
                                   '-c "int eth1" '
                                   '-c "ip address 192.168.1.2/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "q" '
                                   '-c "int eth2" '
                                   '-c "ip address 192.168.3.2/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "q" '
                                   '-c "int eth3" '
                                   '-c "ip address 192.168.22.2/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "do wr"', stdout=True, stderr=True, tty=True, privileged=True)

            print("finished configuring router2!")
        elif node_name == 'router3':
            print("configuring router3...")
            container = client.containers.get(f'clab-{topo_name}-router3')
            container.exec_run(cmd='vtysh -c "conf" '
                                   '-c "router isis 1" '
                                   '-c "is-type level-2-only" '
                                   '-c "net 49.0001.3000.0000.3000.00" '
                                   '-c "q" '
                                   '-c "int lo0" '
                                   '-c "ip router isis 1" '
                                   '-c "isis passive" '
                                   '-c "q" '
                                   '-c "int eth1" '
                                   '-c "ip address 192.168.2.3/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "q" '
                                   '-c "int eth2" '
                                   '-c "ip address 192.168.3.3/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "q" '
                                   '-c "int eth3" '
                                   '-c "ip address 192.168.33.3/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "isis network point-to-point" '
                                   '-c "do wr"', stdout=True, stderr=True, tty=True, privileged=True)

            print("finished configuring router3!")
        elif node_name == 'PC1':
            print("configuring PC1...")
            container = client.containers.get(f'clab-{topo_name}-PC1')
            container.exec_run(cmd='vtysh -c "conf" '
                                   '-c "router isis 1" '
                                   '-c "net 49.0001.0000.0000.0001.00" '
                                   '-c "is-type level-2-only" '
                                   '-c "q" '
                                   '-c "int lo" '
                                   '-c "ip router isis 1" '
                                   '-c "isis passive" '
                                   '-c "q" '
                                   '-c "int eth1" '
                                   '-c "ip address 192.168.11.4/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis network point-to-point" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "do wr"', stdout=True, stderr=True, tty=True, privileged=True)

            print("finished configuring PC1!")
        elif node_name == 'PC2':
            print("configuring PC2...")
            container = client.containers.get(f'clab-{topo_name}-PC2')
            container.exec_run(cmd='vtysh -c "conf" '
                                   '-c "router isis 1" '
                                   '-c "net 49.0001.2000.0000.2002.00" '
                                   '-c "is-type level-2-only" '
                                   '-c "q" '
                                   '-c "int lo" '
                                   '-c "ip router isis 1" '
                                   '-c "isis passive" '
                                   '-c "q" '
                                   '-c "int eth1" '
                                   '-c "ip address 192.168.22.4/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis network point-to-point" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "do wr"', stdout=True, stderr=True, tty=True, privileged=True)

            print("finished configuring PC2!")
        elif node_name == 'PC3':
            print("configuring PC3...")
            container = client.containers.get(f'clab-{topo_name}-PC3')
            container.exec_run(cmd='vtysh -c "conf" '
                                   '-c "router isis 1" '
                                   '-c "net 49.0001.3000.0000.3003.00" '
                                   '-c "is-type level-2-only" '
                                   '-c "q" '
                                   '-c "int lo" '
                                   '-c "ip router isis 1" '
                                   '-c "isis passive" '
                                   '-c "q" '
                                   '-c "int eth1" '
                                   '-c "ip address 192.168.33.4/24" '
                                   '-c "ip router isis 1" '
                                   '-c "isis network point-to-point" '
                                   '-c "isis circuit-type level-2-only" '
                                   '-c "do wr"', stdout=True, stderr=True, tty=True, privileged=True)

            print("finished configuring PC3!")
    client = docker.from_env()
    for node in topology['topology']['nodes'].keys():
        configure_node(node)


if __name__ == '__main__':
    # Buidling topology with name test0
    topo_name = "test1"
    endpoints = [["router1:eth1", "router2:eth1"], ["router1:eth2", "router3:eth1"], ["router2:eth2", "router3:eth2"],
                 ["PC1:eth1", "router1:eth3"], ["PC2:eth1", "router2:eth3"], ["PC3:eth1", "router3:eth3"]]
    topology = generate_topology(topo_name, 3, 3, endpoints)
    with open(topo_name + '.yml', 'w') as f:
        yaml.dump(topology, f, default_flow_style=False)

    # Starting clab...
    docker_process = subprocess.run(['sudo', 'clab', 'deploy', '--topo', topo_name + '.yml', '--reconfigure'])

    # Configuring topology...
    if docker_process.returncode == 0:
        configure_topology(topology)
        print("The topology has been successfully generated and launched")
