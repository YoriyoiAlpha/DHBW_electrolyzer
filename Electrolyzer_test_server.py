import json

from pyModbusTCP.server import ModbusServer, DataHandler
from pyModbusTCP.constants import EXP_ILLEGAL_FUNCTION

input_register = {}
with open("input_registers.json") as f:
    data = json.load(f)
    for r in data["registers"]:
        for i in range(r["len"]//16):
            input_register[r["id"] + i] = 1

class MyDataHandler(DataHandler):
    def read_coils(self, address, count, srv_info):
        return super().read_coils(address, count, srv_info)

    def read_d_inputs(self, address, count, srv_info):
        return super().read_d_inputs(address, count, srv_info)

    def read_h_regs(self, address, count, srv_info):
        return super().read_h_regs(address, count, srv_info)

    def read_i_regs(self, address, count, srv_info):
        print(f"input register read {address} x{count}")
        for i in range(count):
            if input_register[i + address] != 1:
                print("address unset")
                # return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
                return DataHandler.Return(1)
        return super().read_i_regs(address, count, srv_info)

    def write_coils(self, address, bits_l, srv_info):
        return super().write_coils(address, bits_l, srv_info)

    def write_h_regs(self, address, words_l, srv_info):
        return super().write_h_regs(address, words_l, srv_info)
        
s = ModbusServer(data_hdl = MyDataHandler(), port = 4502)
s.start()
