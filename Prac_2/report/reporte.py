import json
from Prac_2.snmp.getSNMP import consultaSNMP
from reportlab.pdfgen import canvas
from datetime import timedelta
from Prac_2.snmp.fetch import fetch_rrd

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

    print("Ingresa la fecha de inicio y final que deseas mostrar en el reporte, sigue el formato del ejemplo.")
    print("Ejemplo de fecha: 2022-03-01 12:30:56")

    print("Fecha inicial: ", end='')
    fecha_I = input()
    print("Fecha final: ", end='')
    fecha_F = input()

    result = fetch_rrd(fecha_I,fecha_F,name)

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
    ip = disp["ipAddress"]

    if(tiempo != ''):
        tiempo = int(tiempo)/100
        tiempo = timedelta(seconds=int(tiempo))

    dateT_ = ""
    if(dateT != ''):
        dateT_ = "{0:04}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}:{6:02}".format(
            int(dateT[2:6], 16),  # Year
            int(dateT[6:8], 16),  # Month
            int(dateT[8:10], 16),  # Day
            int(dateT[10:12], 16),  # Hour
            int(dateT[12:14], 16),  # Minutes
            int(dateT[14:16], 16),  # Seconds
            int(dateT[16:18], 16))  # Deci-seconds

        if len(dateT) > 18:
            dateT_ = dateT_ + " UTC{0}{1:02}:{2:02}".format(
                chr(int(dateT[18:20], 16)),  # Direction from UTC (ASCII format)
                int(dateT[20:22], 16),  # Hoours from UTC
                int(dateT[22:24], 16))  # Minutes from UTC

    c.drawString(25, 780, "Nombre del dispositivo: "+name_)
    c.drawString(25, 765, "Version: " + version)
    c.drawString(25, 750, "Ubicacion: " + ubi)
    c.drawString(25, 735, "Tiempo en actividad: " + str(tiempo))
    c.drawString(25, 720, "Hora del dispositivo: " + dateT_)
    c.drawString(25, 705, "Host/IP: " + ip)

    inicio_In = str(result[2][0][0])
    inicio_Out = str(result[2][-1][0])
    final_In = str(result[2][0][1])
    final_Out = str(result[2][-1][1])

    if (inicio_In == "None"):
        inicio_In = 0
    if (inicio_Out == "None"):
        inicio_Out = 0
    if (final_In == "None"):
        final_In = 0
    if (final_Out == "None"):
        final_Out = 0

    segs_In = int(final_In) - int(inicio_In)
    segs_Out = int(final_Out) - int(inicio_Out)


    c.drawString(25, 690, "TCP In Segments: " + str(segs_In))
    c.drawString(25, 675, "TCP In Segments: " + str(segs_Out))

    c.save()


