# coding=utf-8
import json
import os
import time

import jsonpickle
from entities.control import AboveControl, BelowControl, TimeControl


class smartContract:
    def __init__(self, plc,  controls):
        """
        初始化智能合约
        """
        self.blockchain_path = None
        self.index = None
        self.path = os.path.join(plc.intermediate_yaml['output_path'], plc.intermediate_plc['name'])
        self.submit(jsonpickle.encode(controls))

    def submit(self, controls):
        """
        写入区块
        """
        untx_path = os.path.join(self.path, 'untx')

        sign_path = os.path.join(self.path, 'sign')

        while not self.get_sign(sign_path, 1):
            pass

        json_data = json.dumps(controls)

        with open(untx_path, 'wb') as f:
            f.write(json_data)

        self.blockchain_path = os.path.join(self.path, 'blockchain')
        while 1:
            time.sleep(0.3)
            with open(self.blockchain_path, 'rb') as f:
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
        with open(self.blockchain_path, 'rb') as f:
            raw = f.readline()
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []

        for item in data:
            if item['index'] == self.index:
                controls = item['tx']
                if json.dumps(jsonpickle.encode(local_controls)) == controls:
                    for control in local_controls:
                        control.apply(plc)
                else:
                    for control in jsonpickle.decode(json.loads(controls)):
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