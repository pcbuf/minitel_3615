#!/usr/bin/env python3
import serial, pynitel, os, time

m = pynitel.Pynitel(serial.Serial('/dev/serial0', 1200,
    parity=serial.PARITY_EVEN,
    bytesize=7,
    stopbits=serial.STOPBITS_ONE,
    timeout=2))

def retour_menu():
    os.execv("/usr/bin/python3", ["python3", "police_menu.py"])

m.home()
m.cursor(False)
m.xdraw("ecrans/E.POLICE2.vtx")

m.resetzones()
m.pos(24, 2)
m._print("Choix : .. + ENVOI")
m.zone(24, 10, 2, '', m.blanc)
m.cursor(True)

(zone, touche) = m.waitzones(1)
choix = m.zones[0]['texte'].strip()

m.cursor(False)

if touche in [m.sommaire, m.retour]:
    os.execv("/usr/bin/python3", ["python3", "police.py"])

if choix in [str(i) for i in range(1, 12)]:
    m.home()
    m._print("=== ACCÈS RÉSERVÉ ===\r\n\r\nCode superviseur : ........")
    (saisie, t) = m.input(3, 21, 16, data='', caractere='*')
    m.message(0, 1, 2, "Code invalide", bip=True)
    time.sleep(2)
    retour_menu()

elif choix == "28":
    m.home()
    m._print("root@serveur-police:~#")
    (cmd, t) = m.input(1, 24, 32, data='')
    if cmd.strip() == "sudo police-hub --force-access":
        m._print("\r\nAccès en cours...\r\n")
        m.attend(100)
        m._print("\r\n*** MODULE DE PIRATAGE À VENIR ***")
    else:
        m._print("\r\nCommande inconnue")
        time.sleep(2)
        retour_menu()
else:
    m.message(0, 1, 2, "Choix invalide", bip=True)
    time.sleep(2)
    retour_menu()
