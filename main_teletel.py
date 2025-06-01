#!/usr/bin/env python3

import serial
import pynitel

m = None

def init():
    global m
    m = pynitel.Pynitel(serial.Serial(
        '/dev/serial0',
        baudrate=1200,
        bytesize=7,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=2
    ))
    return m

def page_accueil():
    global m
    m.home()
    m.cursor(False)
    m.xdraw("ecrans/E.TELETEL.vtx")

    m.resetzones()
    m.pos(18, 5)
    m._print("code du service : ...............")
    m.zone(18, 25, 8, '', m.jaune)

    m.color(m.blanc)
    m.pos(6, 10)
    m._print("0,12F à la connexion, puis:")
    m.backcolor(m.rouge)
    m.pos(7, 10)
    m._print("prix total en F/min TTC")
    m.backcolor(m.bleu)

    # Trois lignes de tarifs
    m.pos(8, 10)
    m._print("t2 0.37  t23 0.45")
    m.pos(9, 10)
    m._print("t22 0.45 (avantages horaires)")
    m.pos(10, 10)
    m._print("t32 0.85  t34 1.01  t36 2.29")

    # Lignes de mentions légales
    m.pos(11, 10)
    m._print("dont 0,12 à la connexion")
    m.pos(12, 10)
    m._print("vers les DOM, ajouter 0,33F/min")
    m.pos(13, 10)
    m._print("facturation par Unités Télécom")
    m.pos(14, 10)
    m._print("indivisibles de 0,74F TTC")


    m.pos(21, 2)
    m._print("(C)")
    m.pos(22, 2)
    m._print("Qwest")
    m.pos(23, 2)
    m._print("Telecom")
    m.pos(24, 2)
    m._print("1992")

    m.pos(19, 32)
    m.inverse()
    m._print("Envoi")
    m.inverse(False)

    m.pos(20, 31)
    m._print("└───────────────")
    m.pos(21, 32)
    m.inverse()
    m._print("Guide")
    m.inverse(False)

    m.pos(22, 31)
    m._print("───────────────┘")
    m.pos(23, 32)
    m.color(m.vert)
    m._print("Sommaire")

    m.pos(24, 31)
    m._print("└───────────────")
    m.pos(24, 32)
    m.color(m.blanc)
    m._print("Cx/Fin")

    m.cursor(True)
    (zone, touche) = m.waitzones(1)

    code = m.zones[0]['texte'].strip().upper()
    if touche == m.envoi and code in ['ULLA', 'ANNU', 'POLICE']:
        m.message(0, 1, 2, f"Code {code} reconnu (pas encore actif)", bip=True)
    elif touche == m.envoi:
        m.message(0, 1, 2, "Code inconnu", bip=True)
    elif touche == m.sommaire:
        m.message(0, 1, 2, "Retour sommaire", bip=True)
    elif touche == m.guide:
        m.message(0, 1, 2, "Guide non disponible", bip=True)

if __name__ == '__main__':
    init()
    while True:
        page_accueil()
