# -*- coding: utf-8 -*-
"""
Module d'importation et d'exportation de tableaux de données au format CSV.
Logiciels pris en compte : Latis, Regressi, RegAvi, AviMeca3

@author: David Thérincourt
"""

import numpy as np
from io import StringIO

def normalisefileName(fileName, encodage = 'utf-8') :
    """
    Normalise les séparateurs décimaux dans un fichier CSV en remplaçant les virgules par des points.
    """
    f = open(fileName,'r', encoding = encodage)
    data = f.read()
    f.close()
    return StringIO(data.replace(",","."))

def importCsv(fileName, sep = ';', skip = 1, commentChar = '') :
    """
    Importe des données au format CSV à partir du logiciel AviMéca 3
    Paramètre :
        fileName (str) : nom du fichier CSV
    Paramètre optionnel :
        sep (str) : caractère de séparation des colonnes de données (";" par défaut)
        skip (integer) : nombre de ligne à sauter au début du fichier
        commentChar (str) : caractère définissant un commentaire
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    return np.genfromtxt(fileName, delimiter = sep, unpack = True, skip_header = skip, comments = commentChar)

def importAvimeca3Txt(fileName, sep = '\t') :
    """
    Importe des données au format CSV à partir du logiciel AviMéca 3
    Paramètre :
        fileName (str) : nom du fichier CSV
    Paramètre optionnel :
        sep (str) : caractère de séparation des colonnes de données (tabulation '\t' par défaut)
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    data = normalisefileName(fileName, encodage = 'cp1252') # iso-8859-1 ou CP1252
    return np.genfromtxt(data, delimiter = sep, unpack = True, skip_header = 3, comments = '#')

def importRegaviTxt(fileName, sep = '\t') :
    """
    Importe des données au format CSV à partir du logiciel RegAvi
    Paramètre :
        fileName (str) : nom du fichier CSV
    Paramètre optionnel :
        sep (str) : caractère de séparation des colonnes de données (tabulation '\t' par défaut)
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    data = normalisefileName(fileName, encodage = 'ascii')
    return np.genfromtxt(data, delimiter = sep, unpack = True, skip_header = 2, comments = '#')

def importRegressiTxt(fileName) :
    """
    Importe des données au format TXT à partir du logiciel Regressi
    Paramètre :
        fileName (str) : nom du fichier CSV
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """

    return np.genfromtxt(fileName, delimiter = "\t", unpack = True, skip_header = 2, comments = '')

def importRegressiCsv(fileName) :
    """
    Importe des données au format CSV à partir du logiciel Regressi
    Paramètre :
        fileName (str) : nom du fichier CSV
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    data = normalisefileName(fileName, encodage = 'ascii')
    return np.genfromtxt(data, delimiter = ";", unpack = True, skip_header = 2, comments = '')

#######################################
# Exportation
#######################################

def exportTxt(data, fileName = "data.txt", sep = ";", headerLine = ''):
    """
    Exporte des données au format CSV dans un fichier texte (txt) compatible Regressi, Latis, Libre office. Ecrase le fileName existant.
    Paramètre :
        data (tuple) : tuple de tableaux de données
    Paramètres optionnels :
        fileName (str) : nom du fichier CSV à exporter ("data.txt" par défaut)
        sep (str) : caractère de séparation des colonnes de données (";" par défaut)
        headerLine (str) : noms des variables des données séparatés par la caractère de séparation (sep)
    """
    data = np.transpose(data)
    np.savetxt(fileName, data, delimiter = sep, header = headerLine, comments='')
    return 0
