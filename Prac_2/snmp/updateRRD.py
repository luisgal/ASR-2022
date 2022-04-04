import os.path
import rrdtool
import json
import time
from Prac_2.snmp.getSNMP import consultaSNMP

def updateDisp(disp):
    tcpInSegs = int(consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.6.10.0'))
    tcpOutSegs = int(consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.6.11.0'))

    valor = "N:"+str(tcpInSegs)+':'+str(tcpOutSegs)

    if(os.path.exists('./bd/'+disp["name"]+".rrd")):
        rrdtool.update('./bd/'+disp["name"]+".rrd", valor)
        rrdtool.dump('./bd/'+disp["name"]+".rrd", './bd/'+disp["name"]+".xml")

def update(filename):
    while 1:
        time.sleep(2)
        with open(filename, 'r') as file:
            file_data = json.load(file)
            for disp in file_data["dispositivos"]:
                if (disp["conexion"] == "True"):
                    updateDisp(disp)