import os
import os.path
import json
from Prac_1.snmp.CreateRRD import create

def alta(filename):
    print('Para agregar un nuevo dispostivo se requieren los siguientes datos.')

    print('\tNombre del dispositivo: (NOTA: una sola palabra) ', end='')
    name = input()

    print('\tHostName o IpAddress: ', end='')
    ipAddress = input()

    print('\tVersion snmp a utilizar: ', end='')
    version = input()

    print('\tNombre de la comunidada a la que pertenece: ', end='')
    community = input()

    print('\tPuerto de consulta snmp: ', end='')
    port = input()

    print('\tNumero de interfaz de red, dada en snmp, a monitorear: (NOTA: la interfaz por default es 1)', end='')
    interfaz = input()
    if interfaz == '':
        interfaz = '1'

    newDispositivo = {
        "name": name,
        "ipAddress": ipAddress,
        "version": version,
        "community": community,
        "port": port,
        "interface" : interfaz,
        "conexion": "False"
    }

    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["dispositivos"].append(newDispositivo)
        file.seek(0)
        json.dump(file_data, file, indent=4)

        create(newDispositivo["name"])

        print("El dispositivo fue agregado, ahora debes intentar establecer conexion para que comenzar a monitorearlo")

def baja(filename):
    print('Eliminar un dispositivo, inserta hostName o iPAdress: ', end='')
    host = input()

    file_data = {
        "dispositivos": []
    }

    remove = False
    with open(filename, 'r') as file:
        file_data = json.load(file)
        dispositivos = file_data["dispositivos"]

        index = 0
        for dispositivo in dispositivos:
            if host == dispositivo["ipAddress"]:
                if os.path.exists('./bd/' + dispositivo["name"] + ".rrd"):
                    os.remove('./bd/' + dispositivo["name"] + ".rrd")
                if os.path.exists('./bd/' + dispositivo["name"] + ".xml"):
                    os.remove('./bd/' + dispositivo["name"] + ".xml")
                break
            index += 1

        if index < len(dispositivos):
            dispositivos.pop(index)
            remove = True

    if file_data and remove:
        with open(filename, 'w') as file:
            json.dump(file_data, file, indent=4)

            print("El dispositivo ha sido removido")