import json
import time
from tqdm import tqdm
from pyModbusTCP.client import ModbusClient

conn = ModbusClient(host = "127.0.0.1", port = 4502, unit_id = 1, auto_open = True, auto_close = False)

with open("input_registers.json") as f:
    data = json.load(f)
    regs = data["registers"]
    res = {}
    for r in tqdm(range(100)):
        for r in regs:
            start = time.time()
            conn.read_input_registers(r["id"], r["len"] // 16)
            res[r["name"]] = res.get(r["name"], 0) + time.time() - start
    with open("registers_time.json") as out:
        json.dump(res, out)
