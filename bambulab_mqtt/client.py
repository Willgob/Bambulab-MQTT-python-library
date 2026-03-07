import paho.mqtt.client as mqtt
import ssl
import json
import time, random, string
import os
import threading

    
class BambulabPrinter:
    def __init__ (self, ip, access_code, serial):
        self.printer_ip = ip
        self.printer_serial = serial
        self.printer_username = "bblp"
        self.password = access_code
        self.latest_status = {}
        self.latest_snapshot = None
        self._data_received = threading.Event()

    def on_connect(self, client, userdata, flags, rc):
        printer = userdata
        # print("MQTT Connected:", rc)
        if rc == 0:
            topic = f"device/{printer.printer_serial}/report"
            client.subscribe(topic)
            # print("subbed to: ", topic)
        else: 
            # print("MQTT Connection failed: ",rc)
            pass



    def on_message(self, client, userdata, msg):
        printer = userdata
        try:
            payload = json.loads(msg.payload.decode() )
            # print("Raw data", json.dumps(payload, indent=2))
            for key, value in payload.items():
                if key not in printer.latest_status:
                    printer.latest_status[key] = value
                else: 
                    if isinstance(value, dict):
                        printer.latest_status[key].update(value)
                    else :
                        printer.latest_status[key] = value

            # print(json.dumps(printer.latest_status, indent=2))
            # print("message")
            printer._data_received.set()
        
        except: pass

    def request_full_status(self, timeout=5):
        payload = {
            "pushing" : {
                "sequence_id" : "1",
                "command" : "pushall",
                "version" : 1,
                "push_target" : 1
            }
        }
        self._data_received.clear()
        topic = f"device/{self.printer_serial}/request"
        self.client.publish(topic, json.dumps(payload))
        # print("requested full data")
        if not self._data_received.wait(timeout=timeout):
            # print("Warning: timed out waiting for printer response")
            pass

    # ── Convenience properties ──────────────────────────────────

    def _print_status(self):
        """Return the 'print' sub-dict from latest_status, or empty dict."""
        return self.latest_status.get("print", {})

    @property
    def nozzle_temp(self):
        return self._print_status().get("nozzle_temper")

    @property
    def nozzle_target_temp(self):
        return self._print_status().get("nozzle_target_temper")

    @property
    def bed_temp(self):
        return self._print_status().get("bed_temper")

    @property
    def bed_target_temp(self):
        return self._print_status().get("bed_target_temper")

    @property
    def chamber_temp(self):
        return self._print_status().get("chamber_temper")

    @property
    def print_percentage(self):
        return self._print_status().get("mc_percent")

    @property
    def print_state(self):
        """e.g. 'RUNNING', 'PAUSE', 'IDLE', 'FINISH', 'FAILED'"""
        return self._print_status().get("gcode_state")

    @property
    def print_speed(self):
        """Speed profile: 1=Silent, 2=Standard, 3=Sport, 4=Ludicrous"""
        return self._print_status().get("spd_lvl")

    @property
    def remaining_time(self):
        """Remaining print time in minutes."""
        return self._print_status().get("mc_remaining_time")

    @property
    def current_layer(self):
        return self._print_status().get("layer_num")

    @property
    def total_layers(self):
        return self._print_status().get("total_layer_num")

    @property
    def fan_speed(self):
        """Part cooling fan speed (percentage string)."""
        return self._print_status().get("cooling_fan_speed")

    @property
    def aux_fan_speed(self):
        return self._print_status().get("big_fan1_speed")

    @property
    def chamber_fan_speed(self):
        return self._print_status().get("big_fan2_speed")

    @property
    def wifi_signal(self):
        return self._print_status().get("wifi_signal")

    @property
    def gcode_file(self):
        return self._print_status().get("gcode_file")

    @property
    def subtask_name(self):
        return self._print_status().get("subtask_name")

    @property
    def stg_cur(self):
        """Current print stage."""
        return self._print_status().get("stg_cur")

    # ── Commands ────────────────────────────────────────────────

    def send_command(self, client, serial, payload):
        topic = f"device/{self.printer_serial}/request"
        client.publish(topic, json.dumps(payload))
        # print("Command sent: ", json.dumps(payload,indent=2))


    def connect(self):
        client_id = "Personal_dashboard" + str(int(time.time()))
        self.client = mqtt.Client(client_id=client_id, clean_session=True, userdata=self)
        self.client.username_pw_set(self.printer_username, self.password)
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.tls_insecure_set(True)

        self.client.on_connect = self.on_connect
        self.client.on_message =self.on_message

        try:
            self.client.connect(self.printer_ip, 8883, 60)
            self.client.loop_start()
            return self.client
        except Exception as e:
            # print("MQTT Printer Connection Error")
            return None
