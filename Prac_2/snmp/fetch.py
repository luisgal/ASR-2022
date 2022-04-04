import rrdtool
import time

def fetch_rrd(fecha_I, fecha_F,name):
    tiempo_inicial = int(time.mktime(time.strptime(fecha_I,"%Y-%m-%d %H:%M:%S")))
    tiempo_final = int(time.mktime(time.strptime(fecha_F,"%Y-%m-%d %H:%M:%S")))
    print(tiempo_inicial, tiempo_final)
    print()

    result = rrdtool.fetch("./bd/"+name+".rrd", "-s,"+str(tiempo_inicial), "-e,"+str(tiempo_final), "AVERAGE")

    return result
    #start, end, step = result[0]
    #ds = result[1]
    #rows = result[2]