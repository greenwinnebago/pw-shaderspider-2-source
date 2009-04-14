import string, os, shutil, poser, sys, gzip, tempfile

if float(poser.Version()) >= 7:
    import re
else:
    import pre as re

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

from ss6Constants import *

def runtime(path):
    run_pattern = re.compile("""\WRuntime\W.+""", re.I)
    results = run_pattern.search(path)
    if results:
        results = results.group()
        results = os.path.normpath( re.sub('"', '', results) )
        results = string.join(string.split(results,"\\"),":")
        if not results[0] == ":": results = ":" + results
        return '"%s"' % results.strip()
    else:
        return '"%s"' % os.path.normpath(path)

def p4Bump(path):
    p = re.sub("""\..+""",".bum",path)
    return runtime(p)

def createMatDs(mats, doClean=1):
    import ss6Ds
    dsBuilder = ss6Ds.DsMaterialProperties()
    for mat in mats:
        dsBuilder.addMaterial( mat )
    return dsBuilder.get()

def createSelectPz2(actor, mats):
    files = []

    for m in mats:
        m.SetSelected(1)
        outpath = os.path.abspath(m.Name() + ".mt5")
        m.SaveMaterialSet(outpath)
        files.append(outpath)
        files.append(os.path.abspath(m.Name() + ".mz5"))

    if hasattr(actor, "ConformTarget"):
        actorStr = "figure"
        p4ActorStr = actorStr
    else:
        actorStr = "actor $CURRENT"
        p4ActorStr = "actor %s" % actor.InternalName()

    mc6ActorStr = "mtlCollection"
    completeP4 = """{\n\nversion\n\t{\n\tnumber 4.01\n\t}\n%s\n\t{""" % p4ActorStr
    completePP = """{\n\nversion\n\t{\n\tnumber 4.01\n\t}\n%s\n\t{""" % actorStr
    completeP5 = """{\n\nversion\n\t{\n\tnumber 5\n\t}\n%s\n\t{""" % actorStr
    completeP6 = """{\n\nversion\n\t{\n\tnumber 6\n\t}\n%s\n\t{""" % mc6ActorStr

    for path in files:
        if not os.path.exists(path):
                        continue
        fir = ""
        if path.endswith(".mz5"):
            fi = gzip.open(path, "rb")
            fir = fi.read()
            fi.close()
        else:
            fi = open(path,"r")
            fir = fi.read()
            fi.close()
        cleaned = cleanMaterial(fir)
        completeP4 = completeP4 + cleaned[0]
        completePP = completePP + cleaned[1]
        completeP5 = completeP5 + cleaned[2]
        completeP6 = completeP6 + cleaned[2]

    completeP4 = completeP4 + """\n\t}\n}"""
    completePP = completePP + """\n\t}\n}"""
    completeP5 = completeP5 + """\n\t}\n}"""
    completeP6 = completeP6 + """\n\t}\n}"""
    completeDS = createMatDs( mats )
    
    invalidBracketPattern = re.compile('{\t{');
    completeP4 = invalidBracketPattern.sub('{', completeP4);
    completeP5 = invalidBracketPattern.sub('{', completeP5);
    completeP6 = invalidBracketPattern.sub('{', completeP6);
    
    invalidBracketPattern = re.compile('}\t{');
    completeP4 = invalidBracketPattern.sub('}', completeP4);
    completeP5 = invalidBracketPattern.sub('}', completeP5);
    completeP6 = invalidBracketPattern.sub('}', completeP6);
    
    invalidNoMapPattern = re.compile('"NO_MAP"');
    completeP4 = invalidNoMapPattern.sub('NO_MAP', completeP4);
    completeP5 = invalidNoMapPattern.sub('NO_MAP', completeP5);
    completeP6 = invalidNoMapPattern.sub('NO_MAP', completeP6);

    invalidNoMapPattern = re.compile('file (("+\s*:*NO_MAP\s*"+\s*"*)|(""))');
    completeP5 = invalidNoMapPattern.sub("file NO_MAP", completeP5)
    completeP6 = invalidNoMapPattern.sub("file NO_MAP", completeP6)
    
    invalidFilteringPattern = re.compile('\s*nodeInput "Filtering"\s*\{\s*name "Filtering"\s*value \d+ \d+ \d+\s*parmR \S+\s*parmG \S+\s*parmB \S+\s*node \S+\s*file \S+\s*\}');
    completeP5 = invalidFilteringPattern.sub("", completeP5)
    completeP6 = invalidFilteringPattern.sub("", completeP6)

    basePath = DIR_MANAGER.get("matFileName")
    outP4 = os.path.join(DIR_MANAGER.get("pz2"), basePath + " P4.pz2")
    outPP = os.path.join(DIR_MANAGER.get("pz2"), basePath + " PP.pz2")
    outP5 = os.path.join(DIR_MANAGER.get("pz2"), basePath + " P5.pz2")
    outP6 = os.path.join(DIR_MANAGER.get("mc6"), basePath + " P6.mc6")
    outDS = os.path.join(DIR_MANAGER.get("ds"), basePath + ".ds")
    
    pngPaths = []
    for doMat, outPath, outText in [ ("doP4", outP4, completeP4),
                                     ("doPP", outPP, completePP),
                                     ("doP5", outP5, completeP5),
                                     ("doP6", outP6, completeP6),
                                     ("doDS", outDS, completeDS) ]:
        if DIR_MANAGER.get(doMat):
                writeFile(outPath, outText)
                pngPaths.append( os.path.splitext(outPath)[0] + ".png" )

    if DIR_MANAGER.get("doPng"):
        png_path = "pose.png"
        poser.Scene().SaveLibraryCamera("pose.cm2")
        i = 0
        for png in pngPaths:
                        shutil.copyfile(png_path, png)
        files.append("pose.cm2")
        
    for path in files:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists( path[:-3]+"png" ):
            os.remove( path[:-3]+"png" )

    return (outP4,outPP,outP5,outP6,outDS)

def writeFile(path,data):
    fi = open(path,"w")
    fi.write(data)
    fi.close()

def cleanMaterial(data):
    doClean = DIR_MANAGER.get("doClean")
    tex_pattern = re.compile("""textureMap\s(?P<map>.+)\n""")
    bum_pattern = re.compile("""bumpMap\s(?P<map>.+)\n""")
    ref_pattern = re.compile("""reflectionMap\s(?P<map>.+)\n""")
    tra_pattern = re.compile("""transparencyMap\s(?P<map>.+)\n""")
    fil_pattern = re.compile("""file\s(?!\"\")(?P<map>.+)\n""")

    textures = tex_pattern.findall(data)
    bumps = bum_pattern.findall(data)
    reflects = ref_pattern.findall(data)
    transpares = tra_pattern.findall(data)
    ffmaps = fil_pattern.findall(data)

    map_refs = []
    for m in textures:
        if m != "NO_MAP" and not (m in map_refs): map_refs.append(m)
    for m in bumps:
        if m != "NO_MAP" and not (m in map_refs): map_refs.append(m)
    for m in reflects:
        if m != "NO_MAP" and not (m in map_refs): map_refs.append(m)
    for m in transpares:
        if m != "NO_MAP" and not (m in map_refs): map_refs.append(m)
    for m in ffmaps:
        if not (m in map_refs): map_refs.append(m)

    P5 = data
    for m in map_refs:
        if doClean: cleaned = runtime(m)
        else: cleaned = m
        P5 = string.join(string.split(P5,m),cleaned)

    P4 = P5
    bump_refs = []
    for b in bumps:
        if b != "NO_MAP" and not (b in bump_refs): bump_refs.append(b)
    for b in bump_refs:
        cleaned = p4Bump(b)
        P4 = string.join(string.split(P4, runtime(b)), cleaned)

    shaderTree = re.compile("""reflectionStrength\s\S*(?P<st>.*?)\n\t\t\}""", re.S)
    sts = shaderTree.findall(P4)
    for st in sts:
        P4 = string.join(string.split(P4, st), '')
    PP = P5
    sts = shaderTree.findall(PP)
    for st in sts:
        PP = string.join(string.split(PP, st), '')
    return (P4[44:-6],PP[44:-6],P5[44:-6])

if __name__ == '__main__':
    figure = poser.Scene().CurrentFigure()
    askfile = poser.DialogFileChooser(type=poser.kDialogFileChooserSave,message="Save as...",startDir=os.path.join("Runtime","libraries"))
    if(askfile.Show()):
        path = askfile.Path()
        #SaveMATPose(path)
        CreateSelectPZ2(figure, figure.Materials(), path)
pass