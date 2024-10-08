from Electrolyzer import Electrolyzer

import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import re

d = Electrolyzer("127.0.0.1", 4502, 1)

t = time.time()
d.get_input_defs_from_JSON("input_registers.json")
t_el = time.time() - t
print(f"time to load registers defs : {t_el}")

d.connect()
print(d.dump_all_in_reg())

url = "http://141.72.13.23:9091"

while True:
    t = time.time()
    data = d.dump_all_in_reg()
    t_el = time.time() - t
    print(f"time to fetch data : {t_el}")

    registry = CollectorRegistry()
    for v in data:
        if(data[v] == NotImplemented):
         data[v] = -1
         data[v] = str(data[v])
         #if int larger than 64 bits convert it to string because influxDB only support int64
         if(type(data[v]) == int and data[v].bit_length() > 64):
             data[v] = str(data[v])
        g = Gauge(re.sub(r'[\W_]+','_',v), v, registry=registry)
        g.set(data[v])

    push_to_gateway(url, job='electrolyzer', registry=registry)
    print(time.time() - t)
    print(d.dump_all_in_reg())
