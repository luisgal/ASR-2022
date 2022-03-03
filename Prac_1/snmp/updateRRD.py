import os.path
import rrdtool
import json
from Prac_1.snmp.getSNMP import consultaSNMP

def updateDisp(disp):
    if(disp["name"]=='windows'):
        ifInNUcastPkts = int(consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.2.2.1.12.11')) #Wirless
    else:
        ifInNUcastPkts = int(consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.2.2.1.12.2')) #Wireless
    ipInDelivers = int(consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.4.9.0'))
    icmpOutEchoReps = int(consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.5.22.0'))
    tcpOutSegs = int(consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.6.11.0'))
    udpInErrors = int(consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.7.3.0'))

    valor = "N:"+str(ifInNUcastPkts)+':'+str(ipInDelivers)+':'+str(icmpOutEchoReps)+':'+str(tcpOutSegs)+':'+str(udpInErrors)

    if(os.path.exists('./bd/'+disp["name"]+".rrd")):
        rrdtool.update('./bd/'+disp["name"]+".rrd", valor)
        rrdtool.dump('./bd/'+disp["name"]+".rrd", './bd/'+disp["name"]+".xml")

def update(filename):
    while 1:
        with open(filename, 'r') as file:
            file_data = json.load(file)
            for disp in file_data["dispositivos"]:
                if (disp["conexion"] == "True"):
                    updateDisp(disp)