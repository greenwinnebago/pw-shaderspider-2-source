import poser, os, sys

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

import ss6Gui

from ss6Constants import *

start = 1

scene = poser.Scene()
actor = scene.CurrentActor()
if not actor.IsBodyPart() and not actor.IsProp():
	if actor.IsCamera():
		actor = scene.CurrentFigure()
	else:
		actor = None
	if not actor:
		start = poser.DialogSimple.YesNo("SS6 may not run properly without a\nfigure or prop selected. Continue anyways?")
else:
	start = 1

if start:
        base = ":Runtime:Python:PoseWorks:ShaderSpider:wacros:"
	poser.DefineMaterialWacroButton(1, base + "Copy_To_All.py", "Copy to All")
	poser.DefineMaterialWacroButton(2, base + "Copy_To_Group.py", "Copy to Material Group")
	poser.DefineMaterialWacroButton(3, base + "Copy_To_Matching.py", "Copy to Matching")
	poser.DefineMaterialWacroButton(4, base + "Copy_To_Skin.py", "Smart Copy to Skin")
	poser.DefineMaterialWacroButton(5, base + "Edit_Groups.py", "Edit Material Groups")
	poser.DefineMaterialWacroButton(6, base + "Rename_Node.py", "Rename Node")
	poser.DefineMaterialWacroButton(7, base + "Save_Fx6.py", "Save Partial Shader (FX6)")
	poser.DefineMaterialWacroButton(8, base + "Load_Fx6.py", "Load Partial Shader (FX6)")
	poser.DefineMaterialWacroButton(9, base + "Save_Mat.py", "Save MAT Pose")
	poser.DefineMaterialWacroButton(10,":Runtime:Python:poserScripts:Wacros:mainWacros.py","Main Menu")
else:
        pass

ss6Gui.askConvertLegacy()
