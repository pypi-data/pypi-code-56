
import sys
import os

sys.path.append(os.path.dirname(__file__))
import context
import framework

def main(plugin_dir):
    plcontext = context.context()
    pl = framework.framework()
    pl.load(plcontext, [os.path.dirname(__file__) + "\\plugins", plugin_dir])

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
#main()