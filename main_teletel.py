#!/usr/bin/env python3

import serial
import pynitel

m = None

def init():
    """Initialisation du Minitel avec les bons paramètres"""
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
    """Affichage de l'écran TELENET 3615 statique avec saisie"""
    global m
    m.home()
    m.cursor(False)
    m.xdraw("ecrans/E.TELETEL.vtx")

    # Zone de saisie du code service
    m.resetzones()
    m.zone(18, 25, 8, '', m.jaune)

    # Ajout des textes dynamiques
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
    for trio in tarifs:
        m.pos(ligne, 6)
        m._print("{:5}{:>7}   {:5}{:>7}   {:5}{:>7}".format(*trio))
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

    # Remplacement (C) France Télécom par Qwest Télécom
    m.pos(21, 2)
    m._print("Qwest")
    m.pos(22, 2)
    m._print("Telecom")
    m.pos(23, 2)
    m._print("1992")

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
