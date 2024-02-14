import json
import os
import pickle
from entities.control import AboveControl, BelowControl, TimeControl


class smartContract:
    def __init__(self, plc,  controls):
        """
        初始化智能合约
        """
        self.blockchain_path = None
        self.index = None
        self.submit(pickle.dumps(controls))
        self.plc = plc

    def submit(self, controls):
        """
        写入区块
        """
        untx_path = os.path.join(self.plc.intermediate_yaml['output_path'], self.plc.intermediate_plc['name'], 'untx')

        sign_path = os.path.join(self.plc.intermediate_yaml['output_path'], self.plc.intermediate_plc['name'], 'sign')

        while not self.get_sign(sign_path, 1):
            pass

        json_data = json.dumps(controls, indent=2)

        with open(untx_path, 'w') as f:
            f.write(json_data)

        self.set_sign(sign_path, 0)

        self.blockchain_path = os.path.join(self.plc.intermediate_yaml['output_path'], self.plc.intermediate_plc['name'], 'blockchain')

        with open(self.blockchain_path, 'r+') as f:
            raw = f.readline()
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []

        for item in data:
            if item['tx'] == json_data:
                self.index = item['index']
                break


    def checkrun(self, plc, local_controls):
        """
        check controls
        """
        # 从区块链中找对应数据
        with open(self.blockchain_path, 'r+') as f:
            raw = f.readline()
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []

        for item in data:
            if item['index'] == self.index:
                controls = item['tx']
                if pickle.dumps(local_controls) == controls:
                    for control in local_controls:
                        control.apply(plc)
                break
        pass

    @staticmethod
    def get_sign(sign_path, expected_value):

        if os.path.exists(sign_path):
            with open(sign_path, 'r') as f:
                current_value = f.read().strip()
                return current_value == str(expected_value)
        else:
            return False

    @staticmethod
    def set_sign(sign_path, new_value):

        with open(sign_path, 'w') as f:
            f.write(str(new_value))