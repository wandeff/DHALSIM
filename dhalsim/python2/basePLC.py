import json
import os
import signal
import sys
import time
import thread
import numpy as np
from minicps.devices import PLC


class BasePLC(PLC):

    # Pulls a fresh value from the local DB and updates the local CPPPO
    def send_system_state(self):
        values = []
        # Send sensor values (may have gaussian noise)
        for tag in self.sensors:
            # noinspection PyBroadException
            try:
                # Gaussian noise added with respect to noise_scale
                if self.noise_scale != 0:
                    sensor_value = float(self.get(tag))
                    noise_value = np.random.normal(0, self.noise_scale * sensor_value)
                    values.append(sensor_value + noise_value)
                else:
                    values.append(float(self.get(tag)))
            except Exception:
                self.logger.error("Exception trying to get the tag.")
                continue
        # write sensor values to untx

        untx_path = os.path.join(self.intermediate_yaml['output_path'], self.intermediate_plc['name'], 'untx')

        sign_path = os.path.join(self.intermediate_yaml['output_path'], self.intermediate_plc['name'], 'tx')

        while not self.get_sign(sign_path, 1):
            pass

        sensor_values = {sensor: value for sensor, value in zip(self.intermediate_plc['sensors'], values)}

        quoted_sensor_values = ['"{}: {}"'.format(sensor, value) for sensor, value in sensor_values.items()]

        with open(untx_path, 'w') as f:
            f.write('\n'.join(quoted_sensor_values))

        # json_data = json.dumps(sensor_values, indent=2)
        #
        # with open(untx_path, 'w') as f:
        #     f.write(json_data)

        # self.set_sign(sign_path, 0)

        # Send actuator values (unaffected by noise)
        for tag in self.actuators:
            # noinspection PyBroadException
            try:
                values.append(self.get(tag))
            except Exception:
                self.logger.error("Exception trying to get the tag.")
                continue

        self.send_multiple(self.tags, values, self.send_adddress)

    def set_parameters(self, sensors, actuators, values, send_address, noise_scale, week_index=0):
        self.sensors = sensors
        self.actuators = actuators
        self.tags = self.sensors + self.actuators
        self.values = values
        self.send_adddress = send_address
        self.noise_scale = noise_scale
        self.week_index = week_index

    def sigint_handler(self, sig, frame):
        self.logger.debug('PLC shutdown commencing.')
        self.reader = False
        sys.exit(0)

    def startup(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)
        # thread.start_new_thread(self.send_system_state, (0, 0))

    def get_sign(self, sign_path, expected_value):

        if os.path.exists(sign_path):
            with open(sign_path, 'r') as f:
                current_value = f.read().strip()
                return current_value == str(expected_value)
        else:
            return False

    def set_sign(self, sign_path, new_value):

        with open(sign_path, 'w') as f:
            f.write(str(new_value))
