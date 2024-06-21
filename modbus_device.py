from pyModbusTCP.client import ModbusClient
import pyModbusTCP.utils as utils

from Register import Register

MODBUS_MAX_LEN = 125

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
        res = self.conn.read_input_registers(addr, nb)
        if res is None:
            raise IOError(f"Error while reading register {addr}")
        return res
            
    # read an holding register
    def read_hold_reg(self, addr, nb):
        res = self.conn.read_holding_registers(addr, nb)
        if res is None:
            raise IOError(f"Error while reading register {addr}")
        return res

    # read a uint32 from an input register
    def read_in_uint32(self, addr):
        raw = self.read_input_reg(addr, 2)
        return utils.word_list_to_long(raw, long_long = False)[0]

    def read_in_uint64(self, addr):
        raw = self.read_input_reg(addr, 4)
        return utils.word_list_to_long(raw, long_long = True)[0]

    def read_in_uint128(self, addr):
        raw = self.read_input_reg(addr, 8)
        res = 0
        for r in raw:
            res <<= 16
            res += r
        return res

    def read_in_float32(self, addr):
        raw = self.read_in_uint32(addr)
        return utils.decode_ieee(raw)

    def read_in_int32(self, addr):
        raw = self.read_in_uint32(addr)
        return utils.get_2comp(raw, val_size = 32)

    # read a string of length=len from an input register
    def read_in_str(self, addr, len):
        raw = self.read_input_reg(addr, len)
        return bytes(raw).decode("utf-8")

    # convert a register from raw bytes to its value
    def get_input_reg(self, name, raw) -> int | float | str:
        reg = self.input_registers[name]

        if(reg.type == "UInt16"):
            return raw[0]

        if(reg.type == "UInt32"):
            return utils.word_list_to_long(raw, long_long=False)[0]

        if(reg.type == "UInt64"):
            return utils.word_list_to_long(raw, long_long=True)[0]

        if(reg.type == "UInt128"):
            res = 0
            for r in raw:
                res <<= 16
                res += r
            return res

        if(reg.type == "IEEE-754 float32"):
            uint = utils.word_list_to_long(raw, long_long=False)[0]
            return utils.decode_ieee(uint)

        if(reg.type == "Int32"):
            uint = utils.word_list_to_long(raw, long_long=False)[0]
            return utils.get_2comp(uint, val_size=32)

        if(reg.type == "Enum16"):
            return NotImplemented

        if(reg.type == "Sized+Uint16[31]"):
            return NotImplemented

        if(reg.type == "boolean"):
            return raw[0] != 0

        raise NotImplementedError(f"type {reg.type} not implemented")

    def read_input_register(self, regs: list[Register]) -> dict[str, int | str| float]:
        regs.sort(key = lambda v: v.addr)

        reg_range_start = 0
        reg_range_end = 0

        res = {}

        for i, r in enumerate(regs[1:]):
            i = i + 1

            if r.addr - regs[reg_range_start].addr > MODBUS_MAX_LEN or r.addr != regs[reg_range_end].addr + regs[reg_range_end].len // 16 or i == len(regs) - 1:
                s_reg = regs[reg_range_start]
                e_reg = regs[reg_range_end]

                print(s_reg.addr, e_reg.addr + e_reg.len // 16 - s_reg.addr)
                read_regs = self.read_input_reg(s_reg.addr, e_reg.addr + e_reg.len // 16 - s_reg.addr)

                read_regs_map = {e.name: self.get_input_reg(e.name, read_regs[e.addr - s_reg.addr: e.addr - s_reg.addr + e.len // 16]) for e in regs[reg_range_start: reg_range_end]}

                res.update(read_regs_map)

                reg_range_start = i
                
            reg_range_end = i            

        return res
    
    # dump all the values in the inputs registers
    def dump_all_in_reg(self) -> dict[str, int|float|str]:
        return self.read_input_register(list(self.input_registers.values()))
