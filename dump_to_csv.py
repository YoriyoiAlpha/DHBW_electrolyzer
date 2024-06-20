import tqdm
from pyModbusTCP.client import ModbusClient

NB_REGS = 2**13

conn = ModbusClient(host = "127.0.0.1", port = 4502, unit_id = 1, auto_open = True, auto_close = False)

with open("input_regs_dump.csv", "w") as f:
    for i in tqdm.tqdm(range(NB_REGS)):
        res = conn.read_input_registers(i, 1)
        if not res is None:
            res = res[0]
        f.write(f"{res}\n")
