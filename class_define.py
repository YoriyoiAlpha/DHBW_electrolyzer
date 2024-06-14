from pyModbusTCP.client import ModbusClient

class Modbus_element :
    def __init__(self,ip_add,port,uid) :
        self.ip = ip_add
        self.port = port
        self.uid = uid

    def StartConnect(self):
        self.MODBUS_connect = ModbusClient(host=self.ip_add,port=self.port,unit_id=self.uid,auto_open=True,auto_close=False)

    def ReadAddr(self,addr,nb):
        return self.MODBUS_connect.read_input_registers(addr,nb)

    def Close(self):
        self.MODBUS_connect.close();
    
class Electrolyzer (Modbus_element) :
    def __init__(self, ip_add, port, uid):
        super().__init__(ip_add, port, uid)
        self.name = 0

    def GetName(self):
        print(self.ReadAddr(self.name,0))


class Compressor (Modbus_element):
    def __init__(self, ip_add, port, uid):
        super().__init__(ip_add, port, uid)

class Automaton (Modbus_element):
    def __init__(self, ip_add, port, uid):
        super().__init__(ip_add, port, uid)
         
if __name__ == '__main__':
   electrolyser = Electrolyzer('192.168.0.2',502,1)
   electrolyser.StartConnect()
   while True :
      electrolyser.GetName()

