from pyModbusTCP.client import ModbusClient
import pyModbusTCP

class Modbus_element :
    def __init__(self,ip_add,port,uid) :
        self.ip = ip_add
        self.port = port
        self.uid = uid

    def StartConnect(self):
        self.MODBUS_connect = ModbusClient(host=self.ip,port=self.port,unit_id=self.uid,auto_open=True,auto_close=False)

    def ReadAddr(self,addr,nb):
        return self.MODBUS_connect.read_input_registers(addr,nb)

    def Close(self):
        self.MODBUS_connect.close();
    
class Electrolyzer (Modbus_element) :
    def __init__(self, ip_add, port, uid):
        super().__init__(ip_add, port, uid)
        self.name = 0
        self.Firmware_major = 1
        self.Firmware_patch = 2
        self.Firmware_build = 3
        self.Device_Control_Board_Serial_Number = 4
        self.Chassis_Serial_Number = 5
        self.System_State = 6
        self.Life_Time = 7
        self.Uptime = 8
        self.Warning_Event = 9
        self.Error_Event = 10
        self.Product_Code = 11
        self.Stack_Cycles_Quantity = 12
        self.Stack_Runtime = 13
        self.Stack_Production = 14
        self.H2_Flow_Rate = 15
        self.Stack_Serial_Number = 16
        self.Cooling_Type = 17
        self.Electrolyser_State = 18
        self.Configuration_Progress = 19
        self.Configuration_Source = 20
        self.Last_Configuration_Result = 21
        self.Last_Configuration_Wrong_Holding = 22
        self.Hearthbeat = 22
        self.Hight_Electrolyte_Level_Switch = 23
        self.Very_Hight_Electrolyte_Level_Switch = 24
        self.Low_Electrolyte_Level_Switch = 25
        self.Medium_Electrolyte_Level_Switch = 26
        self.Electrolyte_Tank_High_Pressure_Switch = 27
        self.Electronic_Compartment_High_Temperatue_Switch = 28
        self.Chassis_Water_Presence_Switch = 29
        self.Dry_Contact = 30
        self.Electrolyte_Cooler_Fan_Speed = 31
        self.Air_Circulation_Fan_Speed = 32
        self.Electonic_Compartment_Fan_Speed = 33
        self.Electrolyte_Flow_Meter = 34
        self.Stack_Current = 35
        self.PSU_Voltage = 36
        self.Inner_Hydrogen_Pressure = 37
        self.Outer_Hydrogen_Pressure = 38
        self.Water_Inlet_Pressure = 39
        self.Electrolyte_Temperature = 40
        self.Downstream_Temperature = 41
        self.Board_Power = 42
        self.Board_Temperature = 43
        self.Gas_Presence = 44
        self.Safety_Board_Temperature = 45
        self.Outer_Hydrogen_Pressure_Raw_Sensor_Value = 46
        self.Stack_Current_Raw_Sensor_Value = 47
        self.addr = [0,2,3,4,6,14,18,20,22,768,832,1000,1002,1004,1006,1008,1014,1200,4000,4001,4002,4004,4600,7000,7001,7002,7003,7004,7007,7009,7010,7500,7502,7504,7506,7508,7510,7512,7514,7516,7518,7520,7526,7532,7538,7540,8002,8004]
        self.register_lenght = [2,1,1,2,8,4,1,2,2,33,33,2,2,2,2,2,4,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]


    def GetName(self):
        self.realname = pyModbusTCP.utils.word_list_to_long( self.ReadAddr(self.name,2)) 
        print(hex(self.realname[0]))

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
