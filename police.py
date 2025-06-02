#!/usr/bin/env python3
import serial, pynitel
import os

m = pynitel.Pynitel(serial.Serial('/dev/serial0', 1200,
    parity=serial.PARITY_EVEN,
    bytesize=7,
    stopbits=serial.STOPBITS_ONE,
    timeout=2))

m.home()
m.cursor(False)
m.xdraw("ecrans/E.POLICE.vtx")

# Ajout du champ de saisie
m.resetzones()
m.pos(24, 5)
m._print("Choix : .. + ENVOI")
m.zone(24, 13, 1, '', m.blanc)
m.cursor(True)

(zone, touche) = m.waitzones(1)
choix = m.zones[0]['texte'].strip()

m.cursor(False)
m.canblock(23, 40, 1)

if choix == "1":
    m.message(0, 1, 2, "SERVICE TEMPORAIREMENT INDISPONIBLE", bip=True)
    import time
    time.sleep(2)
    os.execv("/usr/bin/python3", ["python3", "police.py"])
elif choix == "2":
    m.message(0, 1, 2, "ALLEZ AU COMMISSARIAT, FEIGNASSE", bip=True)
    import time
    time.sleep(2)
    os.execv("/usr/bin/python3", ["python3", "police.py"])
elif choix == "3":
    m.message(0, 1, 2, "ALORS VOUS, PENDANT LA GUERRE....", bip=True)
    import time
    time.sleep(2)
    os.execv("/usr/bin/python3", ["python3", "police.py"])
elif choix == "4":
    os.execv("/usr/bin/python3", ["python3", "police_login.py"])
else:
    m.message(0, 1, 2, "Choix invalide", bip=True)
    import time
    time.sleep(2)
    os.execv("/usr/bin/python3", ["python3", "police.py"])
