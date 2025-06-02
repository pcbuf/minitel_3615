#!/usr/bin/env python3
import serial, pynitel, os, time

m = pynitel.Pynitel(serial.Serial('/dev/serial0', 1200,
    parity=serial.PARITY_EVEN,
    bytesize=7,
    stopbits=serial.STOPBITS_ONE,
    timeout=2))

def retour():
    os.execv("/usr/bin/python3", ["python3", "police_login.py"])

m.home()
m.cursor(False)
m._print("=== ACCÈS SERVEUR POLICE ===\r\n")

# Forcer clavier en majuscules
m._print(m.PRO2 + '\x6D\x4A')

# Saisie login
m._print("\r\nIdentifiant : ")
(login, touche) = m.input(2, 15, 20, data='')
login = login.strip().upper()

# Saisie mot de passe
m._print("\r\nMot de passe : ")
(password, touche) = m.input(3, 15, 20, data='', caractere='*')
password = password.strip().upper()

# Vérification
if login == "H.GONTIER" and password == "GADGET":
    os.execv("/usr/bin/python3", ["python3", "police_menu.py"])
else:
    m.message(0, 1, 2, "Identifiants incorrects", bip=True)
    time.sleep(2)
    retour()
