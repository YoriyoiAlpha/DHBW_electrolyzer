from Electrolyzer import Electrolyzer

import time
import re

d = Electrolyzer("127.0.0.1", 4502, 1)

t = time.time()
d.get_input_defs_from_JSON("input_registers.json")
t_el = time.time() - t
print(f"time to load registers defs : {t_el}")

d.connect()
print(d.dump_all_in_reg())

while True:
    t = time.time()
    data = d.dump_all_in_reg()
    t_el = time.time() - t
    print(f"time to fetch data : {t_el}")

    print(data)
