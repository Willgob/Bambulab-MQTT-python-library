import json


class CommandsMixin:
    """Add command methods here. BambulabPrinter inherits this."""

    def _publish(self, payload):
        """Send a JSON payload to the printer."""
        topic = f"device/{self.printer_serial}/request"
        self.client.publish(topic, json.dumps(payload))

    # Add your commands below, for example:
    #
    # def pause_print(self):
    #     self._publish({"print": {"sequence_id": "0", "command": "pause"}})
