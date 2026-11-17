# -*- coding: cp1250 -*-

import json
import urllib.request
import hashlib
# import loggerClass




class SendToServer:
    def __init__(self):
        self.num = 10

    def Float(self, data):
        if float(data) == int(float(data)):
            return int(float(data))
        else:
            return float(data)

    def CrcData(self, Co):
        Crc = hashlib.md5()

        Data = str(Co["ide"]) + "#"
        Aux = 0

        for i in Co["data"]:
            Aux = Aux + self.Float(i["value"]) + int(i["idd"])
        print(Aux)
        Aux = round(Aux,10)
        Aux = self.Float(Aux)
        Data = Data + str(Aux)
        print (Data)

        # Python 3 → must encode to bytes
        Crc.update(Data.encode("utf-8"))

        return Crc.hexdigest()[:6]

    def SendData(self, Data, Name="logger",
                 Adr='http://monitor.mkchynov.eu/ppm3_data_receiver.php'):

        Data["crc"] = self.CrcData(Data)
        print(Data)
        
        # Prepare request
        req = urllib.request.Request(Adr)
        req.add_header('Content-Type', 'application/json')

        # Python 3 → data must be bytes
        json_data = json.dumps(Data).encode("utf-8")

        with urllib.request.urlopen(req, json_data) as response:
            r = response.read().decode("utf-8")  # decode response

        print(r)
        return r

if __name__ == '__main__':
    ss = SendToServer()
    Data = {'info': ['Info block'], 'crc': '1e372d', 'ide': 208, 'data': [{'idd': 1, 'idu': 62, 'qname': 'POR FVE', 'value': 1}, {'idd': 1, 'idu': 62, 'qname': 'Stav RNN1', 'value': 0}, {'idd': 1, 'idu': 62, 'qname': 'Stav RNN2', 'value': 1}, {'idd': 1, 'idu': 62, 'qname': 'Stav RNN3', 'value': 1}, {'idd': 1, 'idu': 62, 'qname': 'Data OK', 'value': 1}, {'idd': 1, 'idu': 28, 'qname': 'EP vyr.', 'value': 938.85}, {'idd': 1, 'idu': 28, 'qname': 'EP spotr.', 'value': 3.52}, {'idd': 1, 'idu': 44, 'qname': 'EQ spotr.', 'value': 6.05}, {'idd': 1, 'idu': 44, 'qname': 'EQ vyr.', 'value': 21.89}, {'idd': 1, 'idu': 1, 'qname': 'cos FI', 'value': 0.0}, {'idd': 1, 'idu': 62, 'qname': 'POR FVE', 'value': 1.0}, {'idd': 1, 'idu': 12, 'qname': 'REG P', 'value': 100.0}, {'idd': 1, 'idu': 1, 'qname': 'REG Q', 'value': 1.0}, {'idd': 1, 'idu': 2, 'qname': 'I L1', 'value': 0.0}, {'idd': 1, 'idu': 2, 'qname': 'I L3', 'value': 0.0}, {'idd': 1, 'idu': 3, 'qname': 'U L1-L2', 'value': 22846.0}, {'idd': 1, 'idu': 3, 'qname': 'U L2', 'value': 22776.0}, {'idd': 1, 'idu': 3, 'qname': 'U L3', 'value': 22811.0}, {'idd': 1, 'idu': 21, 'qname': 'P Celk.', 'value': -2.0}, {'idd': 1, 'idu': 23, 'qname': 'Q Celk.', 'value': -1.0}, {'idd': 1, 'idu': 22, 'qname': 'S Celk.', 'value': 2.0}, {'idd': 1, 'idu': 11, 'qname': 'Osvit', 'value': 8.4}], 'format': 1}
    Data = {'info': ['Info block'], 'crc': '1e372d', 'ide': 208, 'data': [
        {'idd': 1, 'idu': 62, 'qname': 'POR FVE', 'value': 1}, 
        {'idd': 1, 'idu': 11, 'qname': 'Osvit', 'value': 8.4}, 
        {'idd': 1, 'idu': 62, 'qname': 'Stav RNN2', 'value': 0}, 
        {'idd': 1, 'idu': 62, 'qname': 'Stav RNN3', 'value': 0}, 
        {'idd': 1, 'idu': 62, 'qname': 'Data OK', 'value': 0}, 
        {'idd': 1, 'idu': 28, 'qname': 'EP vyr.', 'value': 938.85}, 
        {'idd': 1, 'idu': 28, 'qname': 'EP spotr.', 'value': 3.52}, 
        {'idd': 1, 'idu': 44, 'qname': 'EQ spotr.', 'value': 6.05}, 
        {'idd': 1, 'idu': 44, 'qname': 'EQ vyr.', 'value': 21.89}, 
        {'idd': 1, 'idu': 1, 'qname': 'cos FI', 'value': 0.0}, 
        {'idd': 1, 'idu': 62, 'qname': 'POR FVE', 'value': 1.0}, 
        {'idd': 1, 'idu': 12, 'qname': 'REG P', 'value': 100.0}, 
        {'idd': 1, 'idu': 1, 'qname': 'REG Q', 'value': 1.0}, 
        {'idd': 1, 'idu': 2, 'qname': 'I L1', 'value': 0.0}, 
        {'idd': 1, 'idu': 2, 'qname': 'I L3', 'value': 0.0}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L1-L2', 'value': 22846.0}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L2', 'value': 22776.0}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L3', 'value': 22811.0}, 
        {'idd': 1, 'idu': 21, 'qname': 'P Celk.', 'value': -2.0}, 
        {'idd': 1, 'idu': 23, 'qname': 'Q Celk.', 'value': -1.0}, 
        {'idd': 1, 'idu': 22, 'qname': 'S Celk.', 'value': 2.0},         
        {'idd': 1, 'idu': 62, 'qname': 'Stav RNN1', 'value': 0}], 'format': 1}
    Data = {'info': ['Info block'], 'crc': 'e682a4', 'ide': 204, 'data': [
        {'idd': 1, 'idu': 62, 'qname': 'Data OK', 'value': 1}, 
        {'idd': 1, 'idu': 1, 'qname': 'cos FI', 'value': 0.0}, 
        {'idd': 1, 'idu': 2, 'qname': 'I L1', 'value': 6.0}, 
        {'idd': 1, 'idu': 2, 'qname': 'I L2', 'value': 6.0}, 
        {'idd': 1, 'idu': 2, 'qname': 'I L3', 'value': 7.0}, 
        {'idd': 1, 'idu': 12, 'qname': 'I Unbal.', 'value': 4.8}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L1-L2', 'value': 394.0}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L2-L3', 'value': 395.0}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L3-L1', 'value': 395.0}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L1', 'value': 228.0}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L2', 'value': 228.0}, 
        {'idd': 1, 'idu': 3, 'qname': 'U L3', 'value': 228.0}, 
        {'idd': 1, 'idu': 12, 'qname': 'U Unbal.', 'value': 0.2}, 
        {'idd': 1, 'idu': 21, 'qname': 'P Celk.', 'value': 0.0}, 
        {'idd': 1, 'idu': 23, 'qname': 'Q Celk.', 'value': 4.0}, 
        {'idd': 1, 'idu': 22, 'qname': 'S Celk.', 'value': 4.0}], 'format': 1}
    Data["crc"] = ss.CrcData(Data)
    Adr='http://phpstack-175919-2410865.cloudwaysapps.com/ppm3_data_receiver.php'
    req = urllib.request.Request(Adr)
    req.add_header('Content-Type', 'application/json')
    json_data = json.dumps(Data).encode("utf-8")
    
    with urllib.request.urlopen(req, json_data) as response:
        r = response.read().decode("utf-8")
    print(r)
    print(Data["crc"])