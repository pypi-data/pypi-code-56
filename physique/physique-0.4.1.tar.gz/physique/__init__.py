# -*- coding: utf-8 -*-
"""
Librairie Python 3 pour les sciences physiques au lycée.

Modules disponibles de la librairie (package) physique :

- modelisation :
    Modélisation de courbes (linéaire, affine, parabolique, exponentielle, ...)

    Exemple :
    >>> from physique import ajustementParabolique

- csv :
    Importation et exportation de données au format CSV pour Avimeca3, Regavi, Regressi, Latis, ...

    Exemple :
    >>> from physique import importAvimeca3Txt

- pyboard :
    Exécution d'un programme MicroPython sur un microcontrôleur (Micro:bit, Pyboard, ESP32, ...)
    à partir d'un ordinateur par le port série (mode REPL RAW) à partir d'un fichier .py ou d'un
    script sous forme d'une chaîne de caractères sur plusieurs lignes

    Exemple :
    >>> from physique import Pyboard
    >>> pyboard = Pyboard("/dev/ttyACM0")
    >>> reponse = pyboard.execFile("hello.py")
    >>> print(reponse)


@author: David Thérincourt - 2020
"""

from physique.modelisation import *
from physique.csv import *
from physique.pyboard import *
