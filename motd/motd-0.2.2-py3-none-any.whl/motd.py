import requests
import datetime
import json
from html.parser import HTMLParser
from urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def _liste_prenom_nom(chaine):
    liste = chaine.split(" ")
    nom = liste[-1]
    return [" ".join(liste[:-1]), nom.upper()]


class motd():
    def __init__(self, day=None, delta=0):
        MyHTMLParser.liste_evenements = []
        MyHTMLParser.evt_actuel = None
        MyHTMLParser.lien = 0
        MyHTMLParser.evenement = False
        MyHTMLParser.date = False
        self.parser = MyHTMLParser()
        #
        self.jour = day
        self.decalage = int(delta)
        self.sortie_json = {}
        self.j, self.jr, self.js = self._lejour()
        self.page_du_jour = ""
        self._requete()
        self._sortie()

    def _lejour(self):
        aujourdhui = datetime.date.today()
        if self.jour is None:
            jour_reference = aujourdhui
        else:
            date = self.jour.split('/')
            date = list(map(int, date))
            annee = aujourdhui.year
            jour_reference = datetime.date(annee, date[1], date[0])
        #
        jour_choisi = jour_reference + datetime.timedelta(days=self.decalage)
        jour_choisi_requete = jour_choisi.strftime("%m-%d")
        jour_choisi_sortie = jour_choisi.strftime("%d/%m")
        return [jour_choisi, jour_choisi_requete, jour_choisi_sortie]

    def _requete(self):
        url_le_jour = f"oftheday-{self.jr}/"
        site = "https://mathshistory.st-andrews.ac.uk/OfTheDay/"
        self.page_du_jour = requests.get(site + url_le_jour,
                                         verify=False)
        # on force l'encodage car mal détecté
        self.page_du_jour.encoding = 'utf-8'
        return self.page_du_jour.status_code

    def _sortie(self):
        self.parser.feed(self.page_du_jour.text)
        self.sortie_json = json.dumps({self.js: self.parser.liste_evenements})

    def sortie(self):
        return self.sortie_json

    def out(self):
        return self.sortie()


class Evt():
    id = 0

    def __init__(self):
        self.renseignements = {'year': None,
                               'fname': None,
                               'name': None,
                               'event': None}
        self.fourretout = []

    def annee(self, annee):
        self.renseignements['year'] = int(annee)

    def prenom(self, prenom):
        self.renseignements['fname'] = prenom

    def nom(self, nom):
        self.renseignements['name'] = nom

    def nmd(self, t):
        self.renseignements['event'] = t

    def liste(self):
        return self.renseignements


class MyHTMLParser(HTMLParser):
    # liste_evenements = []
    # evt_actuel = None
    # lien = 0
    # evenement = 2
    # date = False
    recuperation_data = False

    def handle_starttag(self, tag, attrs):
        if tag == "div" and attrs[0][1] == "col-md-6":
            MyHTMLParser.evenement = True
        #
        if (tag == "li" or tag == "a") and MyHTMLParser.evenement:
            MyHTMLParser.recuperation_data = True
        else:
            MyHTMLParser.recuperation_data = False

    def handle_endtag(self, tag):
        if tag == "div" and MyHTMLParser.evenement:
            MyHTMLParser.evenement = False
            MyHTMLParser.naissance = False
            MyHTMLParser.deces = False

    def handle_data(self, data):
        if MyHTMLParser.evenement:
            data = data.strip()
            if data == "Born:":
                MyHTMLParser.naissance = True
            elif data == "Died:":
                MyHTMLParser.deces = True
            #
            if MyHTMLParser.recuperation_data and \
               "poster" not in data and "(" not in data and \
               ")" not in data and data.strip("\n") != "":
                data = data.strip(":")
                if MyHTMLParser.evt_actuel is None:
                    MyHTMLParser.evt_actuel = Evt()
                if data.isdigit():
                    MyHTMLParser.evt_actuel.annee(data)
                else:
                    prenom, nom = _liste_prenom_nom(data)
                    MyHTMLParser.evt_actuel.prenom(prenom)
                    MyHTMLParser.evt_actuel.nom(nom)
                    if MyHTMLParser.naissance:
                        evt = "birth"
                    else:
                        evt = "death"
                    MyHTMLParser.evt_actuel.nmd(evt)
                    MyHTMLParser.liste_evenements.append(
                        MyHTMLParser.evt_actuel.liste())
                    MyHTMLParser.evt_actuel = None
