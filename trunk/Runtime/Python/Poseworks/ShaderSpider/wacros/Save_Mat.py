import os, sys, poser

os.chdir( os.path.dirname(poser.AppLocation()) )
if float(poser.Version()) >= 7:
    sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data","24"))
else:
    sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data","22"))

import ss6Node, ss6Parse, ss6Gui, ss6Materials

actor, material = ss6Node.getSelection()

names = ss6Gui.askMaterials(actor)
if names:
    materials = ss6Materials.namesToMaterials(actor, names)
    matOptions = ss6Gui.askSetMatOptions()
    if matOptions:
        paths = ss6Gui.askPosePaths()
        if paths:
            ss6Parse.createSelectPz2(actor, materials)
