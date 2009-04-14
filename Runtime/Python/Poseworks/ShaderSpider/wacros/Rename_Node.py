import poser

import re

def AskNode(shaderTree):
	nodes = shaderTree.Nodes()
	inames = {}
	for node in nodes:
		inames[node.InternalName()] = (node.Name(),node)
	nodeList = []
	for k in inames.keys():
		nodeList.append(inames[k][0] + " <" + k + ">")

	key = poser.DialogSimple.AskMenu("Rename node...","Choose a node.",nodeList)
	if key:
		iname = re.search("""\<(.*)\>""", key).groups()[0]
		return inames[iname][1]
	else:
		return 0

def AskName(node):
	txt = poser.DialogTextEntry(message="Enter new name for %s." % node.Name())
	txt.Show()
	return txt.Text()

def RenameNode(material):
	st = material.ShaderTree()
	node = AskNode(st)
	if node:
		newName = AskName(node)
		if newName:
			newName = re.sub("""\W""", '_', newName)
			node.SetName(newName)
	st.UpdatePreview()

if __name__ == '__main__':
        curmat = poser.Scene().CurrentMaterial()
        if curmat:
        	RenameNode(curmat)
        else:
                raise "No materials selected."

pass
