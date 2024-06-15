import pyModbusTCP
from Electrolyzer import Electrolyzer

d = Electrolyzer("localhost", 4502, 1)
d.get_input_defs_from_JSON("input_registers.json")
print(d.input_registers)
d.connect()
print(d.get_input_reg("ProjectId"))
print(d.dump_all_in_reg())
