from pyModbusTCP.client import ModbusClient
import pyModbusTCP.utils as utils

from Register import Register

class ModBus_device:
    def __init__(self, addr, port, uid):
        self.addr: str = addr
        self.port: int = port
        self.uid: int = uid

        self.input_registers: dict[str, Register] = {}

    def connect(self):
        self.conn = ModbusClient(host = self.addr, port = self.port, unit_id = self.uid, auto_open = True, auto_close = False)

    # Read an input register
    def read_input_reg(self, addr, nb):
        return self.conn.read_input_registers(addr, nb)

    # read an holding register
    def read_hold_reg(self, addr, nb):
        return self.conn.read_holding_registers(addr, nb)

    # read a uint32 from an input register
    def read_in_uint32(self, addr):
        raw = self.read_input_reg(addr, 2)
        return utils.word_list_to_long(raw, long_long = False)[0]

    def read_in_uint64(self, addr):
        raw = self.read_input_reg(addr, 4)
        return utils.word_list_to_long(raw, long_long = True)[0]

    # read a string of length=len from an input register
    def read_in_str(self, addr, len):
        raw = self.read_input_reg(addr, len)
        return bytes(raw).decode("utf-8")

    def get_input_reg(self, name):
        reg = self.input_registers[name]

        if(reg.type == "UInt16"):
            val = self.read_input_reg(reg.addr, 1)
            if(val is None or len(val) == 0):
                raise IOError(f"Error while reading register {reg}")
            return val[0]

        if(reg.type == "UInt32"):
            val = self.read_in_uint32(reg.addr)
            return val

        if(reg.type == "UInt64"):
            val = self.read_in_uint64(reg.addr)
            return val
