import os, sys, poser

os.chdir( os.path.dirname(poser.AppLocation()) )

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

import ss6Node, ss6Fx, ss6Gui

actor, material = ss6Node.getSelection()

inpath = ss6Gui.askLoadFx6Path()

if inpath:
    names = ss6Gui.askMaterials(actor)
    if names:
        ss6Fx.loadFx6(inpath, actor, names)
