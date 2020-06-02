class Fournisseur:
    # attributs
    __nom = ""
    __email = ""

    # constructeurs
    def __init__(self, nom, email):
        self.__nom = nom
        self.__email = email

    @property
    def nom(self):
        return self.__nom

    @property
    def email(self):
        return self.__email

    def __str__(self):
        return f"{self.__nom} {self.__email}"