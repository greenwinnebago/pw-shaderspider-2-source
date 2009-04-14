import os, sys, poser

os.chdir( os.path.dirname(poser.AppLocation()) )

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

import ss6Node, ss6Fx, ss6Gui

outpath = ss6Gui.askSaveFx6Path()

if outpath:
    inputs = ss6Gui.askSelectInputs()
    if inputs:
        ss6Fx.saveFx6(outpath, inputs)
