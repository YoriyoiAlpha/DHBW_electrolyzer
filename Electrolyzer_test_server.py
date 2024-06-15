from pyModbusTCP.server import ModbusServer, DataBank
import json

db = DataBank()

with open("input_registers.json") as f:
    data = json.load(f)
    for r in data["registers"]:
        db.set_input_registers(r["id"], [0x5555] * (r["len"] // 16))

print(db.get_input_registers(0, 100))

s = ModbusServer(data_bank = db, port = 4502)
s.start()
