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
