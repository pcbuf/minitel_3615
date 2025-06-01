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
    m._print("code du service :")
    m.zone(18, 25, 8, '', m.jaune)

    m.color(m.blanc)
    m.pos(6, 6)
    m._print("0,12F à la connexion, puis:")
    m.backcolor(m.rouge)
    m.pos(7, 6)
    m._print("prix total en F/min TTC")
    m.backcolor(m.bleu)

    tarifs = [
        ("t2", "0.37", "t32", "0.85", "t36", "2.29"),
        ("t23", "0.45", "t34", "1.01", "t44", "2.23"),
        ("t22", "0.45 (avantages horaires)", "", "", "", "")
    ]
    ligne = 8
    for ligne_tarif in tarifs:
        m.pos(ligne, 6)
        formatted = ""
        for i in range(0, 6, 2):
            code = ligne_tarif[i].ljust(5)
            val = ligne_tarif[i+1].rjust(10)
            formatted += code + val + "  "
        m._print(formatted.rstrip())
        ligne += 1

    m.pos(ligne, 6)
    m._print("dont F. TELECOM 0,12 à la connexion")
    ligne += 1
    m.pos(ligne, 6)
    m._print("vers les DOM, ajouter 0,33F/min")
    ligne += 1
    m.pos(ligne, 6)
    m._print("facturation par Unités Télécom")
    ligne += 1
    m.pos(ligne, 6)
    m._print("indivisibles de 0,74F TTC")

    m.pos(21, 2)
    m._print("(C)")
    m.pos(22, 2)
    m._print("Qwest")
    m.pos(23, 2)
    m._print("Telecom")
    m.pos(24, 2)
    m._print("1992")

    m.pos(21, 32)
    m._print("Envoi")
    m.pos(22, 32)
    m.inverse()
    m._print("Guide")
    m.inverse(False)
    m.pos(23, 32)
    m.color(m.vert)
    m._print("Sommaire")
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
