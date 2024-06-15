import pyModbusTCP
from Electrolyzer import Electrolyzer

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

d = Electrolyzer("localhost", 4502, 1)
d.get_input_defs_from_JSON("input_registers.json")
d.connect()
print(d.dump_all_in_reg())

token = os.environ.get("INFLUXDB_TOKEN")
org = "DHBW"
url = "https://dhbw-influx.leserveurdansmongrenier.uk"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="electrolyzer"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

while True:
    data = d.dump_all_in_reg()
    for v in data:
        if(data[v] == NotImplemented):
            data[v] = -1
        point = Point("electrolyser").field(v, data[v])
        write_api.write(bucket=bucket, org="DHBW", record=point)
    time.sleep(1)
