from Register import Register
from modbus_device import ModBus_device
import json

class Electrolyzer(ModBus_device):
    def __init__(self, addr, port, uid):
        super().__init__(addr, port, uid)

    def get_input_defs_from_JSON(self, file):
        with open(file) as f:
            data = json.load(f)
            for r in data["registers"]:
                self.input_registers[r["name"]] = Register(r["name"], r["id"], r["len"], r["type"])
