import grpc
import hub.grpc_server.protos.hub_pb2 as pb2
from os import getcwd
from hub.grpc_server.protos.hub_pb2_grpc import HubInfoServiceServicer, add_HubInfoServiceServicer_to_server
from concurrent import futures
from hub.database.database_servicer import DataBaseServicer
from hub.mqtt.mqtt_handler import MqttHandler


def grpc_start_insecure_server(host: str, port: int, mqtt_handler: MqttHandler, db_handler: DataBaseServicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HubInfoServiceServicer_to_server(GrpcServicer(mqtt_handler, db_handler), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    print(f'GRPC server started on {host}:{port}')
    server.wait_for_termination()


def grpc_start_secure_server(host: str, port: int, mqtt_handler: MqttHandler, db_handler: DataBaseServicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HubInfoServiceServicer_to_server(GrpcServicer(mqtt_handler, db_handler), server)

    keyfile = './hub/grpc_server/certs/server-key.pem'
    certfile = './hub/grpc_server/certs/server-cert.pem'
    rootcertfile = './hub/grpc_server/certs/ca-cert.pem'
    private_key = open(keyfile, 'rb').read()
    certificate_chain = open(certfile, 'rb').read()
    root_certificate = open(rootcertfile, 'rb').read()
    credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)], root_certificate
    )

    server.add_secure_port(f'{host}:{port}', credentials)
    server.start()
    print(f'GRPC TLS server started on {host}:{port}')
    server.wait_for_termination()


def convert_db_to_pb2(sensor_type: str):
    if sensor_type == 'humidity':
        return pb2.SensorType.HUMIDITY_SENSOR
    elif sensor_type == 'temperature':
        return pb2.SensorType.TEMPERATURE_SENSOR
    elif sensor_type == 'light':
        return pb2.SensorType.LIGHT_SENSOR
    else:
        print(sensor_type)
        raise ValueError('Type does not exist')


def convert_pb2_to_db(sensor_type: pb2.SensorType):
    if sensor_type == pb2.SensorType.HUMIDITY_SENSOR:
        return 'humidity'
    elif sensor_type == pb2.SensorType.TEMPERATURE_SENSOR:
        return 'temperature'
    elif sensor_type == pb2.SensorType.LIGHT_SENSOR:
        return 'light'
    else:
        raise ValueError('Type does not exist')


class GrpcServicer(HubInfoServiceServicer):
    def __init__(self, mqtt_handler: MqttHandler, db_handler: DataBaseServicer, *args, **kwargs):
        if not db_handler:
            raise ValueError('Database not set!')
        if not mqtt_handler:
            raise ValueError('Mqtt hanlder not set!')

        self.mqtt_handler = mqtt_handler
        self.database_handler = db_handler

    def GetSensorData(self, request, context):
        try:
            sensor_type = self.mqtt_handler.get_device_type(int(request.sensor_id))
        except ValueError:
            raise ValueError(f'Device with id {request.sensor_id} does not exist!')
        response = self.database_handler.sensor_last_data(self.mqtt_handler.get_static_id(int(request.sensor_id)),
                                                          convert_pb2_to_db(sensor_type))
        if not response:
            raise ValueError(f'Device with id {request.sensor_id} has no metrics!')
        value, timestamp = response
        sensor_id = int(request.sensor_id)
        grpc_response = pb2.SensorDataResponse()
        grpc_response.sensor.sensor_id = sensor_id
        grpc_response.sensor.sensor_type = sensor_type
        grpc_response.sensor.value = value
        grpc_response.sensor.timestamp = timestamp
        return grpc_response

    def GetSensorsData(self, request, context):
        sensor_list = []
        for sensor_id in request.sensor_ids:
            try:
                sensor_type = self.mqtt_handler.get_device_type(sensor_id)
            except ValueError:
                raise ValueError(f'Device with id {request.sensor_id} does not exist!')

            response = self.database_handler.sensor_last_data(self.mqtt_handler.get_static_id(int(request.sensor_id)),
                                                              sensor_type)
            if not response:
                raise ValueError(f'Device with id {request.sensor_id} has no metrics!')
            value, timestamp = response
            sensor_list.append(pb2.Sensor(sensor_id=request.sensor_id,
                                          sensor_type=sensor_type,
                                          value=value,
                                          timestamp=timestamp))

        grpc_response = pb2.SensorsDataResponse()
        grpc_response.sensor_list.extend(sensor_list)
        return grpc_response

    def GetAllSensorsList(self, request, context):
        sensor_list = {}
        for sensor_type, sensor_ids in self.mqtt_handler.get_devices_dict().items():
            for sensor_id in sensor_ids:
                sensor_list[sensor_id] = sensor_type

        grpc_response = pb2.AllSensorsListResponse(sensor_list)
        return grpc_response

    def GetAllSensorsData(self, request, context):
        sensors = []
        for sensor_type, sensor_ids in self.mqtt_handler.get_devices_dict().items():
            for sensor_id in sensor_ids:
                response = self.database_handler.sensor_last_data(self.mqtt_handler.get_static_id(int(sensor_id)),
                                                                  sensor_type)
                if response:
                    value, timestamp = response
                    sensors.append(pb2.Sensor(sensor_id=sensor_id,
                                              sensor_type=convert_db_to_pb2(sensor_type),
                                              value=value,
                                              timestamp=timestamp))

        grpc_response = pb2.AllSensorsDataResponse()
        grpc_response.sensors.extend(sensors)
        return grpc_response

    def GetValuesByTimeStamp(self, request, context):
        time_list = []
        value_list = []
        sensor_type = self.mqtt_handler.get_device_type(request.sensor_id)
        rows = self.database_handler.sensor_period_data(self.mqtt_handler.get_static_id(int(request.sensor_id)),
                                                        convert_pb2_to_db(sensor_type),
                                                        request.since, request.until)
        if not rows:
            raise ValueError(f'Device with id {request.sensor_id} has no metrics!')
        for row in rows:
            data, timestamp = row
            time_list.append(timestamp)
            value_list.append(data)
        grpc_response = pb2.TimeResponse()
        grpc_response.time.extend(time_list)
        grpc_response.value.extend(value_list)
        return grpc_response
