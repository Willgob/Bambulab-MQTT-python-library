class PropertiesMixin:
    """Add read-only properties here. BambulabPrinter inherits this."""

    def _print_status(self):
        """Safely get the 'print' sub-dict from latest_status."""
        return self.latest_status.get("print", {})


    @property
    def nozzle_temp(self):
        return self._print_status().get("nozzle_temper")
    
    @property
    def bed_temp(self):
        return self._print_status().get("bed_temper")
    
    @property
    def wifi_signal(self):
        return self._print_status().get("wifi_signal")
    
    @property
    def ams_chip_id(self):
        return self._print_status().get("chip_id")
    
    @property
    def amd_id(self):
        return self._print_status().get("amd_id")
    
    @property
    def ams_humidity(self):
        return self._print_status().get("humidity_raw")
    
    @property
    def ams_temp(self):
        return self._print_status().get("temp")
    
    @property
    def ams_1_tray_type(self):
        return self._print_status().get("tray_1_type")
