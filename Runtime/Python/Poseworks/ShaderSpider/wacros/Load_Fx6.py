import os, sys, poser

os.chdir( os.path.dirname(poser.AppLocation()) )
if float(poser.Version()) >= 7:
    sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data","24"))
else:
    sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data","22"))

import ss6Node, ss6Fx, ss6Gui

actor, material = ss6Node.getSelection()

inpath = ss6Gui.askLoadFx6Path()

if inpath:
    names = ss6Gui.askMaterials(actor)
    if names:
        ss6Fx.loadFx6(inpath, actor, names)
