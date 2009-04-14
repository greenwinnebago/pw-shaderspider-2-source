import poser, os, sys

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

from ss6Constants import *
import ss6Node, ss6Xml, ss6Materials

sys.path.append(os.path.join("Runtime","Python","poserScripts","Wacros"))
import removeOrphans

def quickCompress(path, data):
	import gzip
	zfi = gzip.GzipFile(path,'wb')
	zfi.write(data)
	zfi.close()

def quickDecompress(path):
	import gzip
	zfi = gzip.open(path)
	r = zfi.read()
	zfi.close()
	return r

def loadFx6(path, actor, names):
        targets = ss6Materials.namesToMaterials(actor, names)
        if not path:
                return None
        DIR_MANAGER.set('fx6', os.path.dirname(path))
        fx6 = eval( quickDecompress(path) )
        for mat in targets:
                st = mat.ShaderTree()
                processEffectDict(st, fx6)
                removeOrphans.removeOrphans(mat)
                st.UpdatePreview()
        poser.Scene().Draw()

def saveFx6(path, inputs):
        actor, material = ss6Node.getSelection()
        if not path:
                return None
        DIR_MANAGER.set('fx6', os.path.dirname(path))
        fx6 = makeEffectDict(material.ShaderTree(), inputs)
        if fx6:
                data = repr(fx6)
                quickCompress(path, data)

def makeEffectDict(shaderTree, inputs):
	poserSurface = shaderTree.Node(0)
	shaderType = getSurfaceType(shaderTree)
	if inputs:
		inputTrees = {}
		nodeDicts = []
		for ip in inputs:
			i = poserSurface.InputByInternalName(ip)
			iT = InputTree(i).get()
			nodeDicts.append(findNodes(iT))
		newNodes = reconcileNodeDicts(nodeDicts)
		ips = []
		for ip in inputs:
			ips.append( poserSurface.InputByInternalName(ip) )
		nodeConnector = ss6Xml.AskConnectNode(ips, newNodes, actionMap={})
		connections = nodeConnector.Show()
		if connections:
			for ip in inputs:
				psIpName = ip
				for psIp in poserSurface.Inputs():
					if (psIp.InternalName() == ip):
						psIpName = psIp.Name()
						break
				iT = InputTree( poserSurface.InputByInternalName(ip) ).get()
				if connections.has_key(psIpName):
					iT["StitchTo"] = connections[psIpName]
				#if connections.has_key(psIpInternalName):
				#	iT["StitchTo"] = connections[ip]
				inputTrees[ip] = iT
			return { "Type":shaderType,"NodesToMake":newNodes, "Settings":inputTrees }
		else:
			return None
	else:
		return None

def popInput(st, ip):
	v = ip.Value()
	newNode = None
	newInput = None
	if ip.Type() == poser.kNodeInputCodeCOLOR:
		newNode = st.CreateNode( poser.kNodeTypeCodeSIMPLECOLOR )
		newNode.Input(0).SetColor( v[0], v[1], v[2] )
		newInput = newNode.Input(0)
	elif ip.Type() == poser.kNodeInputCodeFLOAT:
		newNode = st.CreateNode( poser.kNodeTypeCodeMATH )
		newNode.Input(1).SetFloat( v )
		newInput = newNode.Input(1)
	if ip.InNode() and newNode and newInput:
		ip.InNode().ConnectToInput( newInput )
		newNode.ConnectToInput( ip )

def stitch(st, nodeTable, psInput, inputDict):
	stitchTuple = hasStitch(inputDict)
	if stitchTuple:
		popInput(st, psInput)
	stitchNode = psInput.InNode()
	if stitchNode and stitchTuple:
		stitchInput = getStitchInput(st, nodeTable, stitchTuple)
		stitchNode.ConnectToInput(stitchInput)
		return 1
	else:
		return 0

def hasStitch(d):
	if d.has_key("StitchTo"):
		return d["StitchTo"]
	else:
		return 0

def getStitchInput(st, nodeTranslator, stitchTuple):
	iInput = stitchTuple[1]
	return nodeTranslator[ stitchTuple[0] ].InputByInternalName(iInput)

def processEffectDict(shaderTree, preset):
	newNodes = {}
	poserSurface = shaderTree.Node(0)
	if poserSurface.Type() != preset["Type"]:
		raise "This effect is not compatible with the selected material."
	nodesToMake = preset["NodesToMake"]
	for nodeToMake in nodesToMake.keys():
		newNodes[nodeToMake] = nodeFromDict(shaderTree, nodesToMake[nodeToMake])
	inputsToChange = preset["Settings"]
	for inputToChange in inputsToChange.keys():
		settingsFromDict(shaderTree, shaderTree.Node(0), newNodes, inputsToChange[inputToChange])

def settingsFromDict(shaderTree, curNode, newNodes, inputToChange):
	ip = curNode.InputByInternalName(inputToChange["InternalName"])
	stitch(shaderTree, newNodes, ip, inputToChange)
	inputType = inputToChange["Type"]
	inputValue = inputToChange["Value"]
	if inputType == poser.kNodeInputCodeCOLOR or inputType == poser.kNodeInputCodeVECTOR:
		ip.SetColor(inputValue[0],inputValue[1],inputValue[2])
	elif inputType == poser.kNodeInputCodeSTRING:
		ip.SetString(inputValue)
	else:
		ip.SetFloat(inputValue)
	inNode = inputToChange["InNode"]
	if inNode:
		nodeName = inNode["InternalName"]
		node = newNodes[nodeName]
		node.ConnectToInput(ip)
		for inputKey in inNode["Inputs"].keys():
			nodeInputDict = inNode["Inputs"][inputKey]
			settingsFromDict(shaderTree, node, newNodes, nodeInputDict)

def nodeFromDict(shaderTree, preset):
	newNode = shaderTree.CreateNode(preset["Type"])
	newNode.SetInputsCollapsed(preset["InputsCollapsed"])
	newNode.SetPreviewCollapsed(preset["PreviewCollapsed"])
	newNode.SetLocation(preset["Location"][0], preset["Location"][1])
	return newNode

def reconcileNodeDicts(dicts):
	master_dict = dicts[0]
	for d in dicts:
		for key in d.keys():
			if not key in master_dict.keys():
				master_dict[key] = d[key]
	return master_dict

def findNodes(inputdict, nodes={}):
	inNode = inputdict["InNode"]
	if inNode:
		if nodes.has_key(inNode["InternalName"]):
			return nodes
		else:
			nodes[inNode["InternalName"]] = inNode
			for i in inNode["Inputs"].keys():
				nodes = findNodes(inNode["Inputs"][i],nodes=nodes)
			return nodes
	else:
		return nodes

class InputTree:
	def __init__(self, root):
		self.root = root
		self.dict = self.CreateInputDict(self.root)
	def get(self):
		return self.dict
	def CreateNodeDict(self, node):
		nodeDict = { "Type":node.Type(), "InternalName":node.InternalName(), "InputsCollapsed":node.InputsCollapsed(), "Location":node.Location(), "PreviewCollapsed":node.PreviewCollapsed(), "Inputs":{} }
		for i in node.Inputs():
			nodeDict["Inputs"][i.InternalName()] = self.CreateInputDict(i)
		return nodeDict
	def CreateInputDict(self, ip):
		inputDict = { "Type":ip.Type(), "InternalName":ip.InternalName(), "Value":ip.Value(), "InNode":None }
		if ip.InNode():
			inputDict["InNode"] = self.CreateNodeDict(ip.InNode())
		return inputDict

def getSurfaceType(shaderTree):
	surface = shaderTree.Node(0)
	return surface.Type()

def getSurfaceTypeName(surface):
	if (surface.Type() == poser.kNodeTypeCodePOSERSURFACE):
		return "PoserSurface"
	elif (surface.Type() == poser.kNodeTypeCodeBACKGROUND):
		return "Background"
	elif (surface.Type() == poser.kNodeTypeCodeATMOSPHERE):
		return "Atmosphere"
	elif (surface.Type() == poser.kNodeTypeCodeLIGHT):
		return "Light"
	else:
		return "Unknown"

if __name__ == "__main__":
	SaveFX6()
	#LoadFX6([poser.Scene().CurrentMaterial()])

pass
