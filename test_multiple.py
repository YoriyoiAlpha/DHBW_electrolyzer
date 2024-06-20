from threading import Thread
import time
from pyModbusTCP.client import ModbusClient

conn = ModbusClient(host = "127.0.0.1", port = 4502, unit_id = 1, auto_open = True, auto_close = False)

regs = [
    (0,19),
    (20,4),
    (768,33),
    (832,33),
    (1000,15),
    (1200,1),
    (4000,5),
    (4600,1),
    (7000,5),
    (7007,1),
    (7009,2),
    (7500,22),
    (7526,2),
    (7532,2),
    (7538,4),
    (8002,4)
]

def get_range(addr, len):
    res = conn.read_input_registers(addr, len)
    print(res)

ts = []
start = time.time()
for r in regs:
    ts.append(Thread(target = get_range, args = r))
    ts[len(ts) - 1].start()

for t in ts:
    t.join()
    
print(time.time() - start)
