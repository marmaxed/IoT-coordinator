from threading import Thread
from hub.mqtt.mqtt_handler import MqttHandler
from hub.grpc_server.grpc_servicer import grpc_start_insecure_server
from hub.database.database_servicer import DataBaseServicer


if __name__ == '__main__':
    print('Run....')
    print('Starting database handler...')
    database_handler = DataBaseServicer(host='127.0.0.1',
                                        user='hub',
                                        password='hubpassword',
                                        db='hub',
                                        clean_timeout=None)
    database_handler.create_scheme()
    print('Database handler started!')

    mqtt_handler = MqttHandler(main_topic='broker/register', broker="127.0.0.1", db_handler=database_handler)
    mqtt_handler_task = Thread(target=mqtt_handler.start_handling)
    mqtt_handler_task.start()
    print('MQTT handler started!')

    grpc_start_insecure_server('127.0.0.1', 6789, mqtt_handler, database_handler)
    print('gRPC server started!')
