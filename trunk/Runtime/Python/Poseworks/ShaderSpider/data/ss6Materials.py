import poser, os, sys

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

from ss6Constants import *

def getMaterialNames(actor):
    materials = actor.Materials()
    names = []
    for material in materials:
        names.append(material.Name())
    names.sort()
    return tuple(names)

def namesToMaterials(actor, names):
    materials = []
    for name in names:
        try:
            materials.append(actor.Material(name))
        except:
            continue
    return materials

def getSS6Id(actor):
    matNames = getMaterialNames(actor)
    return repr(hash(matNames))

def getPresetPath(actor):
    ss6Id = getSS6Id(actor)
    presetPath = os.path.join(DIR_PRESET, ss6Id + ".mat")
    return presetPath

def readPreset(path):
    preset = {}
    fi = open(path, 'r')
    lines = fi.readlines()
    fi.close()
    section = None
    materials = None
    for line in lines:
        line = line.strip()
        if not section:
            section = line
        elif line == "{":
            materials = []
        elif line == "}":
            preset[section] = materials
            section = None
            materials = None
        elif not line:
            continue
        else:
            materials.append(line)
    return preset

def getPreset(actor):
    path = getPresetPath(actor)
    if not os.path.exists(path):
        return {}
    else:
        return readPreset(path)

def writePreset(outpath, preset):
    output = ""
    for section, materials in preset.items():
        output = output + section
        output = output + "\n\t{"
        for material in materials:
            output = output + "\n\t" + material
        output = output + "\n\t}\n"
    fi = open(outpath, "w")
    fi.write(output)
    fi.close()

def writePresetFor(actor, preset):
    outpath = getPresetPath(actor)
    writePreset(outpath, preset)

def readSS6(path):
    fi = open(path, 'r')
    dictionary = fi.read()
    fi.close()
    ss6 = eval(dictionary)
    preset = {}
    for section, materials in ss6["MapGroups"].items():
        preset["(Map)" + section] = materials
    for section, materials in ss6["SurGroups"].items():
        preset[section] = materials
    allmats = ss6["!ALL"]
    allmats.sort()
    ss6Id = repr(hash(tuple(allmats)))
    return ss6Id, preset

def convertLegacyFiles():
    ss6Files = os.listdir(DIR_PRESET)
    for ss6file in ss6Files:
        fullpath = os.path.join(DIR_PRESET, ss6file)
        base, ext = os.path.split(ss6file)
        if ss6file[-4:] == ".ss6":
            ss6Id, preset = readSS6(fullpath)
            outfile = os.path.join(DIR_PRESET, ss6Id + ".mat")
            print "Converting", ss6file, "to", ss6Id + ".mat"
            writePreset(outfile, preset)
            try:
                os.remove(fullpath)
            except:
                print "Unable to remove", ss6file
        else:
            continue
    print "Done."

pass
