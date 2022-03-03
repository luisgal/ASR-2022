from Prac_1.menu.inicio import inicio
from Prac_1.menu.manejoDispositivos import *
from Prac_1.report.reporte import crearReport

def menu(filename):
    inicio(filename)
    while 1:
        print("\n")

        print("A continuacion se muestra el menu de opciones, escoge la que deseas.")
        print("1. Inicio - Ve los dispositivos monitoreados y sus interfaces, intenta establecer conexion y determina el status del dispositivo ")
        print("2. Agregar un nuevo dispositivo para monitorear. ")
        print("3. Eliminar un dispositivo. ")
        print("4. Generar el reporte de un dispositivo. ")

        print("Opcion a elegir: ", end='')
        opc = input()

        if(opc=='1'):
            inicio(filename)
        elif(opc=='2'):
            alta(filename)
        elif(opc=='3'):
            baja(filename)
        elif(opc=='4'):
            crearReport(filename)
        else:
            print("Opcion incorrecta, intenta nuvamente")

        print("\n")