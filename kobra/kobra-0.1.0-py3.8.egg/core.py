from kobra import __version__
import argparse
import os

def getModuleName(filelist):
    folders = []
    for file in filelist:
        if os.path.isdir(file):
            folders.append(file)

    for folder in folders:
        files = os.listdir(folder)
        for file in files:
            if file == "__init__.py":
                return folder


def kobra():

    parser = argparse.ArgumentParser()

    parser.add_argument("command", nargs="?", default="install", help="Run command (deploy, install, develop)")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        Kobra.sendVersion()
        quit()

    if args.command == "deploy":
        cwd = os.getcwd()
        moduleName = getModuleName(os.listdir("."))
        if moduleName == None:
            print("Program can't find module folder")
            quit()
        else:
            version = input("Enter version (current: " + __version__ + ") ")
            with open(os.getcwd() + "\\" + moduleName + "\\__init__.py", "w") as init:
                init.write("__version__ = \"" + version + "\"")
            os.system("python setup.py sdist")
            os.system("twine upload dist\\*")
        print()
    elif args.command == "install":
        os.system("python setup.py install")
    elif args.command == "develop":
        os.system("python setup.py develop")
    else:
        print("Enter command!")
