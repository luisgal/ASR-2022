import os
import time
from Prac_1.menu.menu import menu
from Prac_1.snmp.updateRRD import update

filename = "./bd/dispositivos.json"

def child():
    menu(filename)

def parent():
    newpid = os.fork()
    if newpid == 0:
        child()
    else:
        time.sleep(1)
        update(filename)

parent()