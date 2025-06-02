#!/usr/bin/env python3
import serial, pynitel, os, time, random

m = pynitel.Pynitel(serial.Serial('/dev/serial0', 1200,
    parity=serial.PARITY_EVEN,
    bytesize=7,
    stopbits=serial.STOPBITS_ONE,
    timeout=2))

# Setup initial
m.home()
m.cursor(False)

WIDTH, HEIGHT = 40, 24
total_nodes = 11
nodes_valides = [False] * total_nodes
pulses_joueur = 5
pulses_ia = 5
ligne_curseur = 5
ligne_ia = 14

def afficher_interface():
    m.home()
    # Ligne des pulses
    m.color(m.vert)
    m.pos(1, 1)
    m._print("●" * pulses_joueur)
    m.color(m.rouge)
    m.pos(1, WIDTH - 4)
    m._print("●" * pulses_ia)

    # Ligne sécurités
    m.color(m.blanc)
    m.pos(2, 2)
    m._print("Sécurités : ")
    for ok in nodes_valides:
        if ok:
            m.color(m.vert)
            m._print("█")
        else:
            m.color(m.blanc)
            m._print("*")

    # Quelques pulsers et nodes simulés
    for i in range(total_nodes):
        y = 4 + i
        m.color(m.jaune)
        m.pos(y, 1)
        m._print("P")  # pulser joueur
        m.pos(y, WIDTH)
        m._print("P")  # pulser IA

        m.color(m.cyan if not nodes_valides[i] else m.vert)
        m.pos(y, WIDTH // 2)
        m._print("▒" if not nodes_valides[i] else "0")

        m.color(m.blanc)
        m.pos(y, WIDTH // 2 - 4)
        m._print("S")  # splitter
        m.pos(y, WIDTH // 2 + 4)
        m._print("J")  # joiner

def valider_node(i):
    nodes_valides[i] = True

def invalider_node(i):
    nodes_valides[i] = False

afficher_interface()

start = time.time()
dernier_deplacement_ia = start
etat_ia = "deplacement"
temps_attente = 1
jeu_termine = False

while not jeu_termine:
    m.cursor(True)
    m.pos(4 + ligne_curseur, 1)
    (cmd, touche) = m.input(4 + ligne_curseur, 1, 1, data='', caractere=' ', redraw=True)
    m.cursor(False)
    
    car = cmd.upper() if cmd else ""

    if car == "A":
        ligne_curseur = max(0, ligne_curseur - 1)
    elif car == "Q":
        ligne_curseur = min(total_nodes - 1, ligne_curseur + 1)

    if touche == m.retour:
        os.execv("/usr/bin/python3", ["python3", "police_menu.py"])

    elif car == " " or touche == m.envoi or car == "":
        if pulses_joueur > 0:
            valider_node(ligne_curseur)
            pulses_joueur -= 1
            afficher_interface()


    # Tour IA toutes les secondes
    if time.time() - dernier_deplacement_ia >= 1:
        if etat_ia == "deplacement":
            ligne_ia = random.randint(0, total_nodes - 1)
            etat_ia = "tir"
            dernier_deplacement_ia = time.time()
        elif etat_ia == "tir":
            if pulses_ia > 0:
                invalider_node(ligne_ia)
                pulses_ia -= 1
                afficher_interface()
            etat_ia = "deplacement"
            dernier_deplacement_ia = time.time()

    # Vérifications fin de jeu
    if all(nodes_valides):
        m.pos(HEIGHT, 1)
        m._print("ACCES ACCORDE")
        time.sleep(3)
        jeu_termine = True
    elif pulses_joueur == 0 and not any(nodes_valides):
        m.pos(HEIGHT, 1)
        m._print("ACCES REFUSE")
        time.sleep(3)
        os.execv("/usr/bin/python3", ["python3", "police_menu.py"])
