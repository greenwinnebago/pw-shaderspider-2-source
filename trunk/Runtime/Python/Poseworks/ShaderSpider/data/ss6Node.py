import os, sys, poser

if float(poser.Version()) >= 7:
    import re
else:
    import pre as re

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

import ss6Materials

class PwPoserShaderTree(object):
    def __init__(self, st):
        self.nodes = []
        for node in st.Nodes():
            self.nodes.append( PwPoserNode(node) )
    def Nodes(self):
        return self.nodes

class PwPoserNode(object):
    def __init__(self, node):
        self.inputs = []
        for ip in node.Inputs():
            self.inputs.append( PwPoserInput(ip) )
        self.inputscollapsed = node.InputsCollapsed()
        self.internalname = node.InternalName()
        self.location = node.Location()
        self.name = node.Name()
        self.previewcollapsed = node.PreviewCollapsed()
        self.type = node.Type()
    def Inputs(self):
        return self.inputs
    def InputsCollapsed(self):
        return self.inputscollapsed
    def InternalName(self):
        return self.internalname
    def Location(self):
        return self.location
    def Name(self):
        return self.name
    def PreviewCollapsed(self):
        return self.previewcollapsed
    def Type(self):
        return self.type

class PwPoserInput(object):
    def __init__(self, ip):
        self.animated = ip.Animated()
        self.canbeanimated = ip.CanBeAnimated()
        self.innode = ip.InNode()
        if self.innode:
            self.innode = self.innode.InternalName()
        self.internalname = ip.InternalName()
        self.itsnode = ip.ItsNode().InternalName()
        self.name = ip.Name()
        self.parameters = ip.Parameters()
        self.type = ip.Type()
        self.value = ip.Value()
    def Animated(self):
        return self.animated
    def CanBeAnimated(self):
        return self.canbeanimated
    def InNode(self):
        return self.innode
    def InternalName(self):
        return self.internalname
    def ItsNode(self):
        return self.itsnode
    def Name(self):
        return self.name
    def Parameters(self):
        return self.parameters
    def Type(self):
        return self.type
    def Value(self):
        return self.value

def collectShader(source):
    return PwPoserShaderTree(source.ShaderTree())

def createFromStored(stored, material):
    equivs = {}
    st = material.ShaderTree()
    for node in st.Nodes():
        if node.Type() == poser.kNodeTypeCodePOSERSURFACE:
            continue
        else:
            node.Delete()
    for node in stored.Nodes():
        newNode = None
        if node.Type() == poser.kNodeTypeCodePOSERSURFACE:
            newNode = st.Node(0)
        else:
            newNode = st.CreateNode(node.Type())
        equivs[ node.InternalName() ] = newNode.InternalName()
        newNode.SetName(node.Name())
        newNode.SetLocation(node.Location()[0], node.Location()[1])
        newNode.SetInputsCollapsed(node.InputsCollapsed())
        newNode.SetPreviewCollapsed(node.PreviewCollapsed())
        for ip in node.Inputs():
            newInput = newNode.InputByInternalName(ip.InternalName())
            newInput.SetAnimated( ip.Animated() )
            newInput.SetName( ip.Name() )
            kind = ip.Type()
            value = ip.Value()
            if kind == poser.kNodeInputCodeCOLOR or kind == poser.kNodeInputCodeVECTOR:
                r, g, b = value
                newInput.SetColor( r, g, b )
            elif kind == poser.kNodeInputCodeSTRING:
                if value == None:
                    value = ""
                newInput.SetString( value )
            else:
                newInput.SetFloat( value )
    for node in stored.Nodes():
        for ip in node.Inputs():
            inNode = ip.InNode()
            if inNode:
                outNode = st.NodeByInternalName( equivs[inNode] )
                inNode = st.NodeByInternalName( equivs[ip.ItsNode()] )
                outNode.ConnectToInput( inNode.InputByInternalName(ip.InternalName()) )
    root = st.Node(0)
    r, g, b = root.InputByInternalName("Diffuse_Color").Value()
    material.SetDiffuseColor(r, g, b)
    r, g, b = root.InputByInternalName("Ambient_Color").Value()
    material.SetAmbientColor(r, g, b)
    r = root.InputByInternalName("Transparency_Max").Value()
    material.SetTransparencyMax(r)
    st.UpdatePreview()

def copyFrom(source, destinations):
    src = collectShader(source)
    for dest in destinations:
       createFromStored(src, dest)
    poser.Scene().Draw()

def getSelection():
    actor = poser.Scene().CurrentActor()
    material = poser.Scene().CurrentMaterial()
    if not material:
        raise "No material selected."
    if actor.IsBodyPart():
        return actor.ItsFigure(), material
    elif actor.IsProp():
        return actor, material
    elif actor.IsCamera():
    	actor = poser.Scene().CurrentFigure()
    	if actor:
    		return actor, material
	raise "Invalid selection. Please select a body part or prop."

def copyToAll():
    actor, material = getSelection()
    targets = actor.Materials()
    copyFrom(material, targets)

def copyToMatching(exp):
    actor, material = getSelection()
    names = ss6Materials.getMaterialNames(actor)
    use = []
    pattern = re.compile(exp, re.I)
    for name in names:
        if pattern.search(name):
            use.append(name)
    materials = ss6Materials.namesToMaterials(actor, use)
    copyFrom(material, materials)

def copyToGroup(group):
    actor, material = getSelection()
    materials = ss6Materials.namesToMaterials(actor, group)
    copyFrom(material, materials)

def copyToNamed(names):
    actor, material = getSelection()
    targets = ss6Materials.namesToMaterials(actor, names)
    copyFrom(material, targets)

def debug():
    pass
