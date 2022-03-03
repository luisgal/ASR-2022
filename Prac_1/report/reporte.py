import json
from Prac_1.snmp.graphRRD import graph
from Prac_1.snmp.getSNMP import consultaSNMP
from reportlab.pdfgen import canvas
from datetime import timedelta

def mostrarDispositivos(filename):
    with open(filename, 'r+') as file:
        file_data = json.load(file)

        x = 1
        for disp in file_data["dispositivos"]:
            print("Dispositivo", x)
            print("\t", disp)
            x += 1

        return file_data["dispositivos"]

def crearReport(filename):
    dispositivos = mostrarDispositivos(filename)
    print("Elige el dispositivo del cual deseas generar su reporte: ", end='')
    opc = input()
    disp = dispositivos[int(opc)-1]

    name = disp["name"]

    graph('Paquetes multicast que ha \nrecibido la interfaz Wireless', 'ifInNUcastPkts', name, 'Numero de paquetes')
    graph('Paquetes recibidos exitosamente, entregados a protocolos IPv4', 'ipInDelivers', name, 'Numero de paquetes')
    graph('Mensajes de respuesta ICMP que ha enviado el agente', 'icmpOutEchoReps', name, 'Numero de mesajes')
    graph('Segmentos enviados incluyendo los de las conexiones actuales pero excluyendo los que contienen solamente octetos retrasnmitidos', 'tcpOutSegs', name, 'Numero de segmentos')
    graph('Datagramas recibidos que no pudieron ser netregados por cuestiones distintas a la falta de aplicacion en el puerto destino', 'udpInErrors', name, 'Numero de datagramas')

    #generar PDF
    c = canvas.Canvas("./report/ReporteDisp"+name+".pdf")
    c.setFont("Helvetica",20) #Titulos
    c.drawString(25,800,"Resporte de Dispositivo")

    c.setFont("Helvetica",12) #Texto
    name_ = consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.1.5.0')
    version = consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.1.1.0')
    ubi = consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.1.6.0')
    tiempo = consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.1.3.0')
    dateT = consultaSNMP(disp["community"], disp["ipAddress"], '1.3.6.1.2.1.25.1.2.0')
    comunidad = disp["community"]
    ip = disp["ipAddress"]

    if(tiempo != ''):
        tiempo = int(tiempo)/100
        tiempo = timedelta(seconds=int(tiempo))

    dateT_ = ""
    if(dateT != ''):
        dateT_ = "{0:04}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}:{6:02} UTC{7}{8:02}:{9:02}".format(
            int(dateT[2:6],16),         #Year
            int(dateT[6:8],16),         #Month
            int(dateT[8:10],16),        #Day
            int(dateT[10:12],16),       #Hour
            int(dateT[12:14],16),       #Minutes
            int(dateT[14:16],16),       #Seconds
            int(dateT[16:18],16),       #Deci-seconds
            chr(int(dateT[18:20],16)),  #Direction from UTC (ASCII format)
            int(dateT[20:22],16),       #Hoours from UTC
            int(dateT[22:24],16))       #Minutes from UTC

    c.drawString(25, 780, "Nombre del dispositivo: "+name_)
    c.drawString(25, 765, "Version: " + version)
    c.drawString(25, 750, "Ubicacion: " + ubi)
    c.drawString(25, 735, "Tiempo en actividad: " + str(tiempo))
    c.drawString(25, 720, "Hora del dispositivo: " + dateT_)
    c.drawString(25, 705, "Comunidad: " + comunidad)
    c.drawString(25, 690, "Host/IP: " + ip)

    c.drawImage("./graph/ifInNUcastPkts" + name + ".png",25,540,265,125)
    c.drawImage("./graph/ipInDelivers" + name + ".png", 300, 540,265,125)
    c.drawImage("./graph/icmpOutEchoReps" + name + ".png", 25, 350,265,125)
    c.drawImage("./graph/tcpOutSegs" + name + ".png", 300, 350,265,125)
    c.drawImage("./graph/udpInErrors" + name + ".png", 25, 160,265,125)

    c.save()


