import packageupload
import sys

def main():
    if 'nocleanup' in sys.argv:
        cleanup = False
    else:
        cleanup = True
    
    if 'keepsetup' in sys.argv:
        keepsetup = True
    else:
        keepsetup = False
    
    if 'customclassifiers' in sys.argv:
        customclassifiers = True
    else:
        customclassifiers = False
    
    if 'customurl' in sys.argv:
        customurl = True
    else:
        customurl = False
    
    if 'forceupgrade' in sys.argv:
        upgrade = True
    else:
        upgrade = False

    if 'customsetup' in sys.argv:
        customsetup = True
    else:
        customsetup = False

    print(packageupload.start(cleanup=cleanup, keepsetup=keepsetup, customclassifiers=customclassifiers, customurl=customurl, upgrade=upgrade, customsetup=customsetup))