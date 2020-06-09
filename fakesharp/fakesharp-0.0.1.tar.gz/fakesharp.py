def inpt(text):
    print(text,"\n")
    a = input(": ")
    print(a)
def println(text):
    print(text)
def imprt(im):
    if im == "requests":
        import requests
def pip_install(library):
    import pip
    pip.main(['install', library])