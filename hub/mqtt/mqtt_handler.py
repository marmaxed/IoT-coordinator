import re
from hub.mqtt.mqtt_client import MqttClient
import hub.grpc_server.protos.hub_pb2 as pb2
from threading import Thread
from queue import Queue
from hub.database.database_servicer import DataBaseServicer
from calendar import timegm
from time import gmtime


class MqttHandler:

    def __init__(self, main_topic='#', broker='127.0.0.1', port=1883, client_name='hub',
                 db_handler: DataBaseServicer = None):
        self.main_topic = main_topic
        self.devices = {'humidity': [], 'temperature': [], 'light': []}
        self.dynamic_to_static_dict = {}
        self._dynamic_id = 0

        self.messages = Queue()
        self.ack_messages = Queue()

        self.mqtt_client = MqttClient(topic='#',
                                      broker=broker,
                                      port=port,
                                      client_name=client_name)
        self.mqtt_subscriber = Thread(target=self.mqtt_client.run_subscriber,
                                      args=(self.messages,))
        self.mqtt_subscriber.start()
        self.mqtt_publisher = Thread(target=self.mqtt_client.run_publisher,
                                     args=(self.ack_messages,))
        self.mqtt_publisher.start()

        if not db_handler:
            raise ValueError('Database not set!')
        self.db = db_handler

    def reg_dynamic_id(self, static_id):
        """Generate dynamic id and add it to dict."""
        self._dynamic_id += 1
        self.dynamic_to_static_dict[self._dynamic_id] = static_id
        return self._dynamic_id

    def get_static_id(self, dynamic_id):
        return self.dynamic_to_static_dict[dynamic_id]

    def get_device_type(self, sensor_id: int):
        """Returns device type ing gRPC format"""
        if sensor_id in self.devices['temperature']:
            return pb2.SensorType.TEMPERATURE_SENSOR
        elif sensor_id in self.devices['humidity']:
            return pb2.SensorType.HUMIDITY_SENSOR
        elif sensor_id in self.devices['light']:
            return pb2.SensorType.LIGHT_SENSOR
        else:
            raise ValueError(f'Device with id {sensor_id} does not exist!')

    def get_devices_dict(self):
        return self.devices

    def register_device_type(self, device_id, device_types):
        """Method registers device to hub. Return 0 on success, 1 if device already registered."""
        status_code = [0, []]
        if device_id not in self.devices['humidity'] or \
                device_id not in self.devices['temperature'] or \
                device_id not in self.devices['light']:
            if int(device_id) not in self.dynamic_to_static_dict.values():
                for device_type in device_types:
                    dynamic_id = self.reg_dynamic_id(int(device_id))
                    self.devices[device_type].append(dynamic_id)
                    status_code[1].append(str(dynamic_id))
            else:
                status_code[0] = 1
            return status_code
        else:
            status_code[0] = 1
            return status_code

    def start_handling(self):
        while True:
            if not self.messages.empty():
                channel, message = self.messages.get(block=False)

                # Register channel event
                if channel == self.main_topic:
                    try:
                        device_id, device_types = message.split(';')
                        device_types = device_types.split(',')
                    except ValueError:
                        print(f'Message: {message}\nError: Could not parse data!')
                        continue

                    # Device check in
                    result = self.register_device_type(device_id, device_types)
                    if result[0] == 0:
                        channel_ids = ','.join(result[1])
                        self.ack_messages.put([self.main_topic, f'ACK;{device_id};{channel_ids}'],
                                              block=True,
                                              timeout=None)
                        print(f'Device with ID {device_id} registered as {str(device_types)[1:-1]}')
                        continue
                    else:
                        print(f'Device with ID {device_id} already registered in hub!')  # TODO security alert
                        continue

                # Client channel event
                elif re.match(r"client\d+\/\w+", channel):
                    try:
                        if len(channel.split('/')) > 2:
                            device_id, subchannel, subject = channel.split('/')
                        else:
                            device_id, subchannel = channel.split('/')
                        if subchannel != 'data' and subchannel != 'status':
                            raise ValueError
                    except ValueError:
                        print('Result: Illegal channel!')  # TODO security alert
                        continue

                    # channel144 => 144
                    device_id = int(device_id[6:])

                    # Check if device exist
                    if device_id not in self.devices['humidity'] and \
                            device_id not in self.devices['temperature'] and \
                            device_id not in self.devices['light']:
                        print('Result: Unregistred device sent data!')  # TODO security alert
                        continue

                    # Handle status sent
                    if subchannel == 'status':
                        print('Result: Status handled!')  # TODO status handler
                        continue

                    # Handle data sent
                    elif subchannel == 'data':
                        if subject == 'humidity' and device_id in self.devices['humidity']:
                            pass
                        elif subject == 'temperature' and device_id in self.devices['temperature']:
                            pass
                        elif subject == 'light' and device_id in self.devices['light']:
                            pass
                        else:
                            print('Result: Unregistred subject!')  # TODO security alert
                            continue

                        timestamp = timegm(gmtime())
                        sensor_data = message

                        if not re.fullmatch(r"\d+\.?\d+", sensor_data):
                            print(f'Illegal data: {sensor_data}\nPossible SQL injection!')
                            continue

                        self.db.insert_sensor_data(self.get_static_id(device_id), subject, timestamp, sensor_data)
                        print('Result: Data recieved!')

                    # Illegal channel event
                    else:
                        print('Result: Unregistred channel!')  # TODO security alert

