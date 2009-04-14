import os, sys, poser

os.chdir( os.path.dirname(poser.AppLocation()) )

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

import ss6Node, ss6Gui

actor, material = ss6Node.getSelection()

group = ss6Gui.askGroup(actor)
if group:
    ss6Node.copyToGroup(group)
