from paho.mqtt import client as mqtt
from queue import Queue
from time import sleep


class MqttClient:

    def __init__(self, topic='#', broker='127.0.0.1', port=1883, client_name='clienthub'):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_name = client_name
        self.message_queue = None
        self.publish_queue = None

    def publish(self, client: mqtt):
        while True:
            if self.publish_queue.empty():
                sleep(0.001)
                continue
            topic, msg = self.publish_queue.get(block=False)
            result = client.publish(topic, msg, qos=0)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")

    def connect_mqtt(self, mode: str):
        def on_connect(client, userdata, flags, rc):
            #if rc == 0:
            #    print("Connected to MQTT Broker!")
            #else:
            #    print("Failed to connect, return code %d\n", rc)
            if rc != 0:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt.Client(self.client_name + f'_{mode}')
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self, client: mqtt):
        def on_message(client, userdata, msg):
            if not self.message_queue:
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            else:
                #print(f'Queue updated with `{msg.payload.decode()}` from `{msg.topic}` topic')
                payload = msg.payload.decode()
                if not 'ACK' in payload:
                    self.message_queue.put([msg.topic, msg.payload.decode()], block=True, timeout=None)
        client.subscribe(self.topic)
        client.on_message = on_message

    def run_subscriber(self, message_queue=None):
        self.message_queue = message_queue
        client = self.connect_mqtt(mode='sub')
        self.subscribe(client)
        client.loop_forever()

    def run_publisher(self, publish_queue=None):
        if not publish_queue:
            raise ValueError('Publish queue required!')
        self.publish_queue = publish_queue
        client = self.connect_mqtt(mode='pub')
        self.publish(client)
