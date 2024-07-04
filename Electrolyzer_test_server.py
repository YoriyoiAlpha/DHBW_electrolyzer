import json

from pyModbusTCP.server import EXP_DATA_ADDRESS, ModbusServer, DataHandler
from pyModbusTCP.constants import EXP_ILLEGAL_FUNCTION, EXP_NONE

input_register = {}
with open("input_regs_dump.csv") as f:
    for i, l in enumerate(f.readlines()):
         if l != "None\n":
            input_register[i] = int(l)
holding_register = {}
with open("holding_regs_dump.csv") as f:
    for i, l in enumerate(f.readlines()):
         if l != "None\n":
            holding_register[i] = int(l)
print(holding_register)

class MyDataHandler(DataHandler):
    def read_coils(self, address, count, srv_info):
        return super().read_coils(address, count, srv_info)

    def read_d_inputs(self, address, count, srv_info):
        return super().read_d_inputs(address, count, srv_info)

    def read_h_regs(self, address, count, srv_info):
        print(f"holding register read {address} x{count}")
        res = []
        for i in range(count):
            if not address + i in holding_register:
                print(f"address unset {address + i}")
                return DataHandler.Return(exp_code=EXP_DATA_ADDRESS)
            else:
                res.append(holding_register[address + i])
        return DataHandler.Return(exp_code=EXP_NONE, data=res)

    def read_i_regs(self, address, count, srv_info):
        print(f"input register read {address} x{count}")
        res = []
        for i in range(count):
            if not address + i in input_register:
                print("address unset")
                return DataHandler.Return(exp_code=EXP_DATA_ADDRESS)
            else:
                res.append(input_register[address + i])
        return DataHandler.Return(exp_code=EXP_NONE, data=res)

    def write_coils(self, address, bits_l, srv_info):
        return super().write_coils(address, bits_l, srv_info)

    def write_h_regs(self, address, words_l, srv_info):
        return super().write_h_regs(address, words_l, srv_info)
        
s = ModbusServer(data_hdl = MyDataHandler(), port = 4502)
s.start()
