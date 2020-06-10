from kobra import __version__
import argparse

class Kobra:
    def sendVersion():
        print("Kobra v" + __version__)

def kobra():

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    # parser.add_argument("-d", "--deploy", help="Deploy")
    parser.add_argument("-n", "--name", help="Enter module name")

    args = parser.parse_args()

    if args.version:
        Kobra.sendVersion()
        quit()

    if args.name == None:
        print("Enter name!")
        quit()
    else:
        print("Module name: " + args.name)
