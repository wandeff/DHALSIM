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

        self.index = None
        self.path = os.path.join(plc.intermediate_yaml['output_path'], plc.intermediate_plc['name'])
        self.blockchain_path = os.path.join(self.path, 'blockchain')
        # self.submit(controls)

    # def submit(self, controls):
    #     """
    #     写入区块
    #     """
    #     untx_path = os.path.join(self.path, 'untx')
    #
    #     sign_path = os.path.join(self.path, 'tx')
    #
    #     while not self.get_sign(sign_path, 1):
    #         pass
    #
    #     json_data = jsonpickle.encode({"controls": controls})
    #
    #     with open(untx_path, 'w') as f:
    #         f.write(json_data)
    #
    #     self.set_sign(sign_path, 0)
    #
    #     self.blockchain_path = os.path.join(self.path, 'blockchain')
    #
    #     a = 1
    #     while a:
    #         time.sleep(1)
    #         with open(self.blockchain_path, 'r') as f:
    #             raws = f.readlines()
    #         if len(raws) > 0:
    #             for raw in raws:
    #                 if "controls" in raw:
    #                     data = json.loads(raw)
    #                     c = json.loads(jsonpickle.encode({"controls": controls}))
    #                     if data['tx'][0] == c:
    #                         self.index = data['index']
    #                         a = 0
    #                         break

    def checkrun(self, plc, local_controls):
        """
        check controls
        """
        # 从区块链中找对应数据
        with open(self.blockchain_path, 'r') as f:
            raws = f.readlines()
        if len(raws) > 0:
            for raw in raws:
                if 'plc' in raw:
                    data = json.loads(raw)
                    if data['plc'] == plc.name:
                        controls = json.loads(data['tx'])
                        if json.loads(jsonpickle.encode({"controls": local_controls})) == controls:
                            for control in local_controls:
                                control.apply(plc)
                        else:
                            # new_controls = []
                            # for control in controls["controls"]:
                            #     new_controls.append(jsonpickle.decode(control))
                            # for control in new_controls:
                            #     control.apply(plc)
                            for control in jsonpickle.decode(json.dumps(controls["controls"])):
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

# if __name__ == "__main__":
#     raw = """{"index": 0, "timestamp": 1714310975.962976, "tx": "", "previous_block": "", "node": "", "nouce": 11283, "hash": "0000530c088134c235f751894f502b84099d6215c18210e4c158cd985c6b46a6"}
# {"index": 1, "timestamp": 1714310976.0246344, "tx": [{"controls": [{"action": "open", "actuator": "PUMP1", "dependant": "TANK", "py/object": "entities.control.BelowControl", "value": 4.0}, {"action": "closed", "actuator": "PUMP1", "dependant": "TANK", "py/object": "entities.control.AboveControl", "value": 6.3}, {"action": "open", "actuator": "PUMP2", "dependant": "TANK", "py/object": "entities.control.BelowControl", "value": 1.0}, {"action": "closed", "actuator": "PUMP2", "dependant": "TANK", "py/object": "entities.control.AboveControl", "value": 4.5}]}], "previous_block": "0000530c088134c235f751894f502b84099d6215c18210e4c158cd985c6b46a6", "node": "3003", "nouce": 100984, "hash": "000044631445218a4822958573fbc6f48ee804a23ed6d2d5a00be755dad1a57f"}
# {"index": 2, "timestamp": 1714310976.6043324, "tx": ["TANK: 2.08023668123"], "previous_block": "00008155deaaf92bc2170dd152ea6bddf6c39720e3f528eb0f38016240746074", "node": "3002", "nouce": 109441, "hash": "0000cfdf72b5681a3d14a2c4fcec127ed44f6ee74ddd1146ef68c574aad030ec"}"""
#     if len(raw) > 0:
#         data = json.loads(raw)
#     else:
#         data = []
#
#     for item in data:
#         if "controls" in item['tx']:
#             c = json.loads(jsonpickle.encode({"controls": controls}))
#             if item['tx'] == c:
#                 self.index = item['index']
#                 a = 0
#                 break
#     pass
