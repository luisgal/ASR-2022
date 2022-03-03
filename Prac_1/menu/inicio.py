import os.path
import json
from Prac_1.snmp.CreateRRD import create
from Prac_1.snmp.getSNMP import consultaSNMP

def inicio(filename):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        dispositivos = file_data["dispositivos"]

        for dispositivo in dispositivos:
            if(consultaSNMP(dispositivo["community"],dispositivo["ipAddress"],'1.3.6.1.2.1.1.1.0') == ""):
                print(dispositivo, 'is down')
                dispositivo["conexion"] = "False"
            else:
                print(dispositivo, 'is up')
                dispositivo["conexion"] = "True"
                interfaces = int(consultaSNMP(dispositivo["community"],dispositivo["ipAddress"], '1.3.6.1.2.1.2.1.0'))
                print('Interfaces: ', interfaces)
                for x in range(1,interfaces+1):
                    status = ['up','down','testing']

                    print('\tInterface: ',x)

                    print('\tSatus: ', status[
                        int(consultaSNMP(dispositivo["community"],dispositivo["ipAddress"], '1.3.6.1.2.1.2.2.1.7.'+str(x)))-1
                        ])

                    descrip = consultaSNMP(dispositivo["community"],dispositivo["ipAddress"], '1.3.6.1.2.1.2.2.1.2.'+str(x))
                    if(descrip[0:2]=='0x'):
                        descrip = bytes.fromhex(descrip[2:]).decode('ASCII')
                    print('\tDescription: ', descrip)

                if(not os.path.exists('./bd/'+dispositivo["name"]+'.rrd')):
                    create(dispositivo["name"])

        file.seek(0)
        json.dump(file_data, file, indent=4)