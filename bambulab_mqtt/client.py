import paho.mqtt.client as mqtt
import json
import time
import random
import string
import ssl


class BambulabPrinter:
    def __init__(self, ip, access_code, username="bblp"):
        self.client = None
        self.connected = False

        self.ip = ip
        # self.serial = serial
        self.access_code = access_code
        self.username = username

        self.latest_status = {}
        self.latest_snapshot = None
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            topic = f"device/{self.serial}/report"
            client.subscribe(topic)
            self.connected = True
        else:
            print(f"Connection failed with code {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            print("Raw data:", json.dumps(payload, indent=2))

            for key, value in payload.items():
                if key not in self.latest_status:
                    self.latest_status[key] = value
                else:
                    if isinstance(value, dict):
                        self.latest_status[key].update(value)
                    else:
                        self.latest_status[key] = value

        except Exception as e:
            print(f"Error processing message: {e}")

    def connect(self):
        client_id = "PythonLib_" + ''.join(random.choices(string.ascii_letters, k=6))
        self.client = mqtt.Client(client_id=client_id, clean_session=True)

        self.client.username_pw_set(self.username, self.access_code)
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        try:
            self.client.connect(self.ip, 8883, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Connection error: {e}")
            return False
        
    def request_full_status(self):
        if not self.connected:
            print("Not connected to printer")
            return None
        
        payload = {
            "pushing": {
                "sequence_id" : 1,
                "command" : "pushall",
                "version" : 1,
                "push_target" :1
            }
        }
