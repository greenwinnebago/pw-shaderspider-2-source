import os, sys, poser

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

from ss6Xml import *
import ss6Materials, ss6Node

def askSelectInputs():
    actor, material = ss6Node.getSelection()
    root = material.ShaderTree().Node(0)
    inputs = []
    for ip in root.Inputs():
        inputs.append( ip.InternalName() )
    selector = SelectInput(inputs)
    if selector.Show():
        return selector.get()
    else:
        return None

def askSetMatOptions():
    return SetMATOptions().Show()

def askEditGroups():
    actor, material = ss6Node.getSelection()
    editor = GroupEditor(actor)
    return editor.Show()

def askSaveFx6Path():
    path = AskSaveAs(ext=".fx6",
                     types=[("Firefly Effect","*.fx6")],
                     dir=DIR_MANAGER.get("fx6"),
                     title="Save as...")
    if path:
        DIR_MANAGER.set("fx6", os.path.dirname(path))
    return path

def askLoadFx6Path():
    path = AskOpen(ext=".fx6",
                   types=[("Firefly Effect","*.fx6")],
                   dir=DIR_MANAGER.get("fx6"))
    if path:
        DIR_MANAGER.set("fx6", os.path.dirname(path))
    return path

def askPosePaths():
    return AskPosePaths().Show()

def askMaterials(actor):
    methods = ["All materials.", "Material group...", "Specific materials...", "Matching materials...", "Current material."]
    selector = AskSelectMethod("Include...", methods=methods)
    if selector.Show():
        method = selector.get()
        if method == methods[0]:
            return ss6Materials.getMaterialNames(actor)
        elif method == methods[1]:
            return askGroup(actor)
        elif method == methods[2]:
            return askSpecificMaterials(actor)
        elif method == methods[3]:
            return askMatchingMaterials(actor)
        else:
            return [poser.Scene().CurrentMaterial().Name()]
    else:
        return []

def askGroup(actor):
    preset = ss6Materials.getPreset(actor)
    use = []
    if preset:
        groups = preset.keys()
        groups.sort()
        group = poser.DialogSimple.AskMenu("Select a group...","Select group", groups)
        if group:
            use = preset[group]
    else:
        ErrorBox("No material groups defined for this object.\n\nYou can use the Edit Groups wacro to\ncreate new material groups.")
    return use

def askSpecificMaterials(actor):
    materials = ss6Materials.getMaterialNames(actor)
    use = []
    selector = SelectMaterial(materials)
    if selector.Show():
        use = selector.get()
    return use

def askMatchingMaterials(actor):
    use = []
    dlg = poser.DialogTextEntry(message="""\n\nEnter matching terms.\n\n\nExample: "skin lash" matches\nboth "SkinHead" and "Eyelashes".\n\n\n""")
    if dlg.Show():
        #import pre as re
        import re
        import string
        text = dlg.Text()
        words = text.split()
        terms = []
        for word in words:
            terms.append( "(" + re.sub("\W","",word) + ")" )
        pattern = re.compile(string.join(terms, "|"), re.I)
        for name in ss6Materials.getMaterialNames(actor):
            if pattern.search(name):
                use.append(name)
    return use

def askConvertLegacy():
    legacy = os.listdir(DIR_PRESET)
    oldPresets = 0
    for f in legacy:
            if f[-3:] == "ss6":
                    oldPresets = 1
    if oldPresets:
            if poser.DialogSimple.YesNo("Would you like to convert your old\n.SS6 presets into new .MAT presets?"):
                    ss6Materials.convertLegacyFiles()
