
import context
import framework

import sys
import os

def main():
    plcontext = context.context()
    pl = framework.framework()
    pl.load(plcontext, [os.path.dirname(__file__) + "\\plugins", sys.argv[1]])

    apps = plcontext.find_extension("PL::APP")
    app = None
    
    for a in apps:
        if a.name() == "MyApp":
            app = a
            break
    if app == None:
        print("PL::APP not match!")
    else:
        app.run(sys.argv)

#print(sys.argv)
main()