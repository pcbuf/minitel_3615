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
    admin_mode = False
    prompt = "root@serveur-police: # "
    ligne = 1
    while True:
        m.pos(ligne, 1)
        m._print(prompt)
        (cmd, touche) = m.input(ligne, len(prompt) + 1, 40 - len(prompt))
        cmd = cmd.strip()
        cmd = cmd.loweer()
        ligne += 1

        if cmd == "":
            continue
        elif cmd == "exit":
            retour_menu()
        elif cmd == "reboot":
            os.execv("/usr/bin/python3", ["python3", "main_teletel.py"])
        elif cmd == "sudo":
            m.pos(ligne, 1)
            m._print("mode administrateur activé")
            admin_mode = True
            prompt = "root@serveur-police: $ "
            ligne += 1
        elif admin_mode and cmd == "policehub--force":
            os.execv("/usr/bin/python3", ["python3", "pirate_minigame.py"])
        elif cmd in ["ls", "dir"]:
            fake_files = [
                "logs/",
                "dossiers_suspects/",
                "rapports_missions.txt",
                "confidential/",
                "acces_reseau/",
                "archive_2021.zip",
                "recherche/",
                "agents.csv",
                "README_SYS.md",
                "sysconfig/"
            ]
            for f in fake_files:
                m.pos(ligne, 1)
                m._print(f)
                ligne += 1
        else:
            m.pos(ligne, 1)
            m._print("Commande inconnue")
            ligne += 1
else:
    m.message(0, 1, 2, "Choix invalide", bip=True)
    time.sleep(2)
    retour_menu()
