import argparse
import hashlib
import logging
import os
import shutil
import signal
import subprocess
import sys
import time

import py2_logger
from pathlib import Path
import networkx as nx
import json
import yaml
import jsonpickle

from datetime import datetime
from minicps.mcps import MiniCPS
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

from topo.simple_topo import SimpleTopo
from topo.complex_topo import ComplexTopo
from entities.control import AboveControl, BelowControl, TimeControl


class GeneralCPS(MiniCPS):
    """
    This class can run a experiment from a intermediate yaml file

    :param intermediate_yaml: The path to the intermediate yaml file
    :type intermediate_yaml: Path
    """

    def __init__(self, intermediate_yaml):

        # Create logs directory in working directory
        try:
            os.mkdir('logs')
        except OSError:
            pass

        self.intermediate_yaml = intermediate_yaml

        with self.intermediate_yaml.open(mode='r') as file:
            self.data = yaml.safe_load(file)

        self.logger = py2_logger.get_logger(self.data['log_level'])

        if self.data['log_level'] == 'debug':
            logging.getLogger('mininet').setLevel(logging.DEBUG)
        else:
            logging.getLogger('mininet').setLevel(logging.WARNING)

        # Create directory output path
        try:
            os.makedirs(str(Path(self.data["output_path"])))
        except OSError:
            pass

        signal.signal(signal.SIGINT, self.interrupt)
        signal.signal(signal.SIGTERM, self.interrupt)

        if self.data["network_topology_type"].lower() == "complex":
            topo = ComplexTopo(self.intermediate_yaml)
        else:
            topo = SimpleTopo(self.intermediate_yaml)

        # draw topo graph
        # automatic_router_path = Path(__file__).parent.absolute() / "graph_draw.py"
        # subprocess.Popen(["python2", str(automatic_router_path), str(topo)])
        # self.draw_topology(topo)
        # self.logger.info("Drew the net Graph")

        self.write_topo(topo.g, self.data['output_path'])

        # blockchain data file
        self.write_blockchain(self, self.data['output_path'], self.data['db_path'], self.data['plcs'])

        self.net = Mininet(topo=topo, autoSetMacs=False, link=TCLink)

        self.net.start()

        topo.setup_network(self.net)

        with self.intermediate_yaml.open(mode='r') as file:
            self.data = yaml.safe_load(file)

        if self.data["mininet_cli"]:
            CLI(self.net)

        self.plc_processes = None
        self.scada_process = None
        self.plant_process = None
        self.attacker_processes = None
        self.network_event_processes = None
        self.router_processes = None
        self.blockchain_processes = None

        self.automatic_start()
        self.poll_processes()
        self.finish()

    # @staticmethod
    # def draw_topology(topo):
    #     G = nx.MultiGraph()
    #
    #     nodes = topo.g.nodes()
    #     edges = topo.g.edges()
    #
    #     G.add_nodes_from(nodes)
    #     G.add_edges_from(edges)
    #
    #     nx.draw(G, with_labels=True, node_color='lightblue', node_size=1500, font_size=20, font_weight='bold')
    #     plt.show()

    @staticmethod
    def create_controls(controls_list):
        """
        Generates list of control objects for a plc
        :param controls_list: a list of the control dicts to be converted to Control objects
        """
        ret = []
        for control in controls_list:
            if control["type"].lower() == "above":
                control_instance = AboveControl(control["actuator"], control["action"],
                                                control["dependant"],
                                                control["value"])
                ret.append(control_instance)
            if control["type"].lower() == "below":
                control_instance = BelowControl(control["actuator"], control["action"],
                                                control["dependant"],
                                                control["value"])
                ret.append(control_instance)
            if control["type"].lower() == "time":
                control_instance = TimeControl(control["actuator"], control["action"],
                                               control["value"])
                ret.append(control_instance)
        return ret

    @staticmethod
    def write_blockchain(self, path, db_path, plcs):

        json_path = path + '/topo.json'

        with open(json_path, 'r') as json_file:
            tdata = json.load(json_file)

        plc_nodes = [node for node in tdata['nodes'] if node.get('type') == 'PLC']

        num = 0
        for plc_node in plc_nodes:
            # get node id
            plc_id = plc_node.get('id')

            # plc_ip = plc_node.get('ip').split('/')[0]
            plc_ip = "http://127.0.0.1:30{}".format(plc_node.get('mac').split(':')[5])
            plc_folder_path = os.path.join(path, plc_id)

            # other plc data
            # other_plc_nodes = [node for node in data['nodes'] if node.get('type') == 'PLC' and node.get('id') != plc_id]
            other_plc_nodes = [node for node in tdata.get('nodes', []) if
                               node.get('type') == 'PLC' and node.get('id') != plc_id]

            # other_plc_addresses = ["http://{}:3009".format(node['ip'].split('/')[0]) for node in other_plc_nodes]
            other_plc_addresses = ["http://127.0.0.1:30{}".format(node['mac'].split(':')[5]) for node in
                                   other_plc_nodes]

            # config data
            config_data = {
                'ip_address': "127.0.0.1:{}".format(plc_ip.split(':')[-1]),
                'data_path': plc_folder_path
            }

            # delete file if it has existed
            if os.path.exists(plc_folder_path):
                shutil.rmtree(plc_folder_path)

            # new file
            os.makedirs(plc_folder_path)
            os.chown(plc_folder_path, os.getuid(), os.getgid())
            os.chmod(plc_folder_path, 0o755)

            # new node and write other plc's address
            node_path = os.path.join(plc_folder_path, 'node')
            with open(node_path, 'w') as node_file:
                for address in other_plc_addresses:
                    node_file.write('"' + address + '"\n')

            os.chown(node_path, os.getuid(), os.getgid())
            os.chmod(node_path, 0o644)

            # new config.yaml
            config_path = os.path.join(plc_folder_path, 'config.yaml')
            with open(config_path, 'w') as config_file:
                yaml.safe_dump(config_data, config_file, default_flow_style=False, allow_unicode=True)
            os.chown(config_path, os.getuid(), os.getgid())
            os.chmod(config_path, 0o644)

            # write sign file to sync data
            # 0: dhalsin finish write, blockchain can read and clear
            # 1: dhalsim can start to write
            sign_path = os.path.join(plc_folder_path, 'tx')
            with open(sign_path, 'w') as sign_file:
                sign_file.write('1')
            os.chown(sign_path, os.getuid(), os.getgid())
            os.chmod(sign_path, 0o644)

            blockchain_path = os.path.join(plc_folder_path, 'blockchain')
            with open(blockchain_path, 'w') as blockchain_file:
                pass
            os.chown(sign_path, os.getuid(), os.getgid())
            os.chmod(sign_path, 0o644)

            json_datas = []
            plc_index = []
            for plc_c in plcs:
                controls = self.create_controls(plc_c['controls'])

                plc_index.append(plc_c['name'])
                json_datas.append(jsonpickle.encode({"controls": controls}))

            blockchain_data = dict()

            # init-block
            blockchain_data["index"] = 0
            blockchain_data["timestamp"] = time.time()
            blockchain_data["tx"] = ''
            blockchain_data["previous_hash"] = ''
            blockchain_data["nouce"] = ''
            header_hash = hashlib.sha256((str(blockchain_data["index"]) + str(
                blockchain_data["timestamp"]) + str(blockchain_data["tx"]) + str(
                blockchain_data["previous_hash"])).encode('utf-8')).hexdigest()
            token = ''.join((header_hash, str(blockchain_data["nouce"]))).encode('utf-8')
            ghash = hashlib.sha256(token).hexdigest()
            blockchain_data["hash"] = ghash

            with open(blockchain_path, 'a') as f:
                json.dump(blockchain_data, f)
                f.write('\n')
            # insert controls
            for json_data, plc_i in zip(json_datas, plc_index):
                dicts = []
                with open(blockchain_path, 'r') as f:
                    # with open(self.filepath, encoding='utf-8-sig', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        # cprint('print', 'line: %s' % (str(line, )))
                        try:
                            data = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        dicts.append(data)
                if len(dicts) > 0:
                    last_block = dicts[-1]
                    blockchain_data["index"] = last_block['index'] + 1
                    blockchain_data["timestamp"] = time.time()
                    blockchain_data["tx"] = json_data
                    blockchain_data["previous_hash"] = last_block['hash']
                    blockchain_data["node"] = ''
                    blockchain_data["nouce"] = ''
                    blockchain_data["plc"] = plc_i

                    header_hash = hashlib.sha256((str(blockchain_data["index"]) + str(
                        blockchain_data["timestamp"]) + str(blockchain_data["tx"]) + str(
                        blockchain_data["previous_hash"])).encode('utf-8')).hexdigest()
                    token = ''.join((header_hash, str(blockchain_data["nouce"]))).encode('utf-8')
                    ghash = hashlib.sha256(token).hexdigest()
                    blockchain_data["hash"] = ghash

                with open(blockchain_path, 'a') as f:
                    json.dump(blockchain_data, f)
                    f.write('\n')

            file_names = ['account', 'sign', 'untx']
            for file_name in file_names:
                file_path = os.path.join(plc_folder_path, file_name)
                with open(file_path, 'w'):
                    pass
                os.chown(file_path, os.getuid(), os.getgid())
                os.chmod(file_path, 0o644)

            num = num + 1

    @staticmethod
    def write_topo(topo, path):

        file_path = path + '/topo.json'
        G = nx.MultiGraph()

        nodes = topo.node
        edges = topo.edges()

        jdata = {'nodes': [], 'edges': []}

        for node_id, node_data in nodes.items():
            new_node = {'id': node_id, 'label': node_id}

            if 'ip' in node_data:
                new_node['ip'] = node_data['ip']

            if 'mac' in node_data:
                new_node['mac'] = node_data['mac']

            if 'defaultRoute' in node_data:
                new_node['defaultRoute'] = node_data['defaultRoute']

            if node_id == 'scada':
                new_node['type'] = 'SCADA'
            elif node_id.startswith('r'):
                new_node['type'] = 'ROUTER'
            elif node_id.startswith('s'):
                new_node['type'] = 'SWITCH'
            elif node_id.startswith('PLC'):
                new_node['type'] = 'PLC'
            else:
                new_node['type'] = 'unknown'

            jdata['nodes'].append(new_node)

        for edge in edges:
            new_edge = {'from': edge[0], 'to': edge[1]}
            jdata['edges'].append(new_edge)

        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, 'w') as file:
            json.dump(jdata, file)

    def interrupt(self, sig, frame):
        """
        Interrupt handler for :class:`~signal.SIGINT` and :class:`~signal.SIGINT`.
        """
        self.finish()
        sys.exit(0)

    def automatic_start(self):
        """
        This starts all the processes for plcs, etc.
        """

        self.router_processes = []
        if 'plcs' in self.data:
            automatic_router_path = Path(__file__).parent.absolute() / "automatic_router.py"

            for plc in self.data["plcs"]:
                node = self.net.get(plc['gateway_name'])
                cmd = ["python2", str(automatic_router_path), str(self.intermediate_yaml), str(plc['gateway_name'])]
                self.router_processes.append(node.popen(cmd, stderr=sys.stderr, stdout=sys.stdout))

        self.logger.info('Launched router processes')

        self.plc_processes = []
        self.blockchain_processes = []
        if "plcs" in self.data:
            automatic_plc_path = Path(__file__).parent.absolute() / "automatic_plc.py"
            chain_path = 'blockchain'
            for i, plc in enumerate(self.data["plcs"]):
                # summon blockchain
                config_path = str(self.data['output_path']) + '/' + str(plc['name']) + '/config.yaml'
                cmd_blockchain = [chain_path, config_path]
                self.blockchain_processes.append(
                    subprocess.Popen(cmd_blockchain, shell=False, stderr=sys.stderr, stdout=sys.stdout))

                node = self.net.get(plc["name"])
                cmd = ["python2", str(automatic_plc_path), str(self.intermediate_yaml), str(i)]
                self.plc_processes.append(node.popen(cmd, stderr=sys.stderr, stdout=sys.stdout))
        self.logger.info("Launched the BLockChain processes.")
        self.logger.info("Launched the PLCs processes.")

        automatic_scada_path = Path(__file__).parent.absolute() / "automatic_scada.py"
        scada_cmd = ["python2", str(automatic_scada_path), str(self.intermediate_yaml)]
        self.scada_process = self.net.get('scada').popen(scada_cmd, stderr=sys.stderr, stdout=sys.stdout)

        automatic_router_path = Path(__file__).parent.absolute() / "automatic_router.py"
        node = self.net.get(self.data['scada']['gateway_name'])
        cmd = ["python2", str(automatic_router_path), str(self.intermediate_yaml),
               str(self.data['scada']['gateway_name'])]
        self.router_processes.append(node.popen(cmd, stderr=sys.stderr, stdout=sys.stdout))

        self.logger.info("Launched the SCADA process.")

        self.attacker_processes = []
        if "network_attacks" in self.data:
            automatic_attacker_path = Path(__file__).parent.absolute() / "automatic_attacker.py"
            for i, attacker in enumerate(self.data["network_attacks"]):
                node = self.net.get(attacker["name"][0:9])
                cmd = ["python2", str(automatic_attacker_path), str(self.intermediate_yaml), str(i)]
                self.attacker_processes.append(node.popen(cmd, stderr=sys.stderr, stdout=sys.stdout))

        self.logger.debug("Launched the attackers processes.")

        self.network_event_processes = []
        if 'network_events' in self.data:
            automatic_event = Path(__file__).parent.absolute() / "automatic_event.py"
            node_name = None
            for i, event in enumerate(self.data['network_events']):
                target_node = event['target']
                if target_node == 'scada':
                    self.logger.debug('Network event in SCADA link')
                    node_name = self.data['scada']['switch_name']
                else:
                    for plc in self.data['plcs']:
                        if target_node == plc['name']:
                            self.logger.debug('Network event in link to ' + str(plc['name']))
                            node_name = plc['switch_name']

                node = self.net.get(node_name)
                # Network events have effect on network interfaces;
                # in addition to the node, we also need the network interface
                event_interface_name = self.get_network_event_interface_name(target_node, node_name)

                cmd = ["python2", str(automatic_event), str(self.intermediate_yaml), str(i), event_interface_name]
                self.network_event_processes.append(node.popen(cmd, stderr=sys.stderr, stdout=sys.stdout))

        self.logger.info("Launched the event processes.")
        automatic_plant_path = Path(__file__).parent.absolute() / "automatic_plant.py"

        cmd = ["python2", str(automatic_plant_path), str(self.intermediate_yaml)]
        self.plant_process = subprocess.Popen(cmd, stderr=sys.stderr, stdout=sys.stdout)

        self.logger.debug("Launched the plant processes.")

    def get_network_event_interface_name(self, target, source):
        for link in self.net.links:
            # example: PLC1-eth0<->s2-eth2
            link_source = str(link).split('-')[0]

            if link_source == target:
                switch_name = str(link).split('-')[2].split('>')[-1]
                interface_name = str(link).split('-')[-1]
                # todo: We are only supporting cases where a PLC has only 1 interface. ALL our cases so far, but still
                return str(switch_name + '-' + interface_name)

    def poll_processes(self):
        """Polls for all processes and finishes if one closes"""
        processes = []
        processes.extend(self.blockchain_processes)
        processes.extend(self.plc_processes)
        processes.extend(self.attacker_processes)
        processes.extend(self.router_processes)
        processes.append(self.scada_process)
        processes.append(self.plant_process)

        # We wait until the simulation ends
        while True:
            for process in processes:
                if process.poll() is None:
                    pass
                else:
                    self.logger.debug("process has finished, stopping simulation...")
                    return

    @staticmethod
    def end_process(process):
        """
        End a process.

        :param process: the process to end
        """
        process.send_signal(signal.SIGINT)
        process.wait()
        if process.poll() is None:
            process.terminate()
        if process.poll() is None:
            process.kill()

    def finish(self):
        """
        Terminate the plcs, physical process, mininet, and remaining processes that
        automatic run spawned.
        """
        self.logger.info("Simulation finished.")

        self.write_mininet_links()

        if self.scada_process.poll() is None:
            try:
                self.end_process(self.scada_process)
            except Exception as msg:
                self.logger.error("Exception shutting down SCADA: " + str(msg))

        for plc_process in self.plc_processes:
            if plc_process.poll() is None:
                try:
                    self.end_process(plc_process)
                except Exception as msg:
                    self.logger.error("Exception shutting down plc: " + str(msg))

        for attacker in self.attacker_processes:
            if attacker.poll() is None:
                try:
                    self.end_process(attacker)
                except Exception as msg:
                    self.logger.error("Exception shutting down attacker: " + str(msg))

        for event in self.network_event_processes:
            if event.poll() is None:
                try:
                    self.end_process(event)
                except Exception as msg:
                    self.logger.error("Exception shutting down event: " + str(msg))

        for router in self.router_processes:
            if router.poll() is None:
                try:
                    self.end_process(router)
                except Exception as msg:
                    self.logger.error("Exception shutting down event: " + str(msg))

        for blockchain in self.blockchain_processes:
            if blockchain.poll() is None:
                try:
                    self.end_process(blockchain)
                except Exception as msg:
                    self.logger.error("Exception shutting down event: " + str(msg))

        if self.plant_process.poll() is None:
            try:
                self.end_process(self.plant_process)
            except Exception as msg:
                self.logger.error("Exception shutting down plant_process: " + str(msg))

        cmd = 'sudo pkill -f "python2 -m cpppo.server.enip"'
        subprocess.call(cmd, shell=True, stderr=sys.stderr, stdout=sys.stdout)

        self.net.stop()
        sys.exit(0)

    def write_mininet_links(self):
        """Writes mininet links file."""
        if 'batch_simulations' in self.data:
            links_path = (Path(self.data['config_path']).parent / self.data['output_path']).parent / 'configuration'
        else:
            links_path = Path(self.data['config_path']).parent / self.data['output_path'] / 'configuration'

        if not os.path.exists(str(links_path)):
            os.makedirs(str(links_path))

        with open(str(links_path / 'mininet_links.md'), 'w') as links_file:
            links_file.write("# Mininet Links")
            for link in self.net.links:
                links_file.write("\n\n" + str(link))


def is_valid_file(parser_instance, arg):
    """Verifies whether the intermediate yaml path is valid"""
    if not os.path.exists(arg):
        parser_instance.error(arg + " does not exist.")
    else:
        return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run experiment from intermediate yaml file')
    parser.add_argument(dest="intermediate_yaml",
                        help="intermediate yaml file", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))

    args = parser.parse_args()

    general_cps = GeneralCPS(intermediate_yaml=Path(args.intermediate_yaml))
