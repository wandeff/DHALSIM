# coding=utf-8
import json
import os
import time

import jsonpickle
from entities.control import AboveControl, BelowControl, TimeControl


class smartContract:
    def __init__(self, plc, controls):
        """
        初始化智能合约
        """
        self.blockchain_path = None
        self.index = None
        self.path = os.path.join(plc.intermediate_yaml['output_path'], plc.intermediate_plc['name'])
        self.submit(controls)

    def submit(self, controls):
        """
        写入区块
        """
        untx_path = os.path.join(self.path, 'untx')

        sign_path = os.path.join(self.path, 'tx')

        while not self.get_sign(sign_path, 1):
            pass

        json_data = jsonpickle.encode({"controls": controls})

        with open(untx_path, 'w') as f:
            f.write(json_data)

        self.set_sign(sign_path, 0)

        self.blockchain_path = os.path.join(self.path, 'blockchain')

        a = 1
        while a:
            time.sleep(1)
            with open(self.blockchain_path, 'r') as f:
                raw = f.readline()
            if len(raw) > 0:
                data = json.loads(raw)
            else:
                data = []
            for item in data:
                if "controls" in item['tx']:
                    c = json.loads(jsonpickle.encode({"controls": controls}))
                    if item['tx'] == c:
                        self.index = item['index']
                        a = 0
                        break

    def checkrun(self, plc, local_controls):
        """
        check controls
        """
        # 从区块链中找对应数据
        with open(self.blockchain_path, 'r') as f:
            raw = f.readline()
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []

        for item in data:
            if item['index'] == self.index:
                controls = item['tx']
                if json.loads(jsonpickle.encode({"controls": local_controls})) == controls:
                    for control in local_controls:
                        control.apply(plc)
                else:
                    for control in jsonpickle.decode(controls["controls"]):
                        control.apply(plc)
                break

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


if __name__ == "__main__":
    if []:
        print(1)
    pass
