import poser, os, sys, string

if float(poser.Version()) >= 7:
    import re
else:
    import pre as re

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

from ss6Constants import *

headerDs = os.path.join(DIR_DATA, "header.ds")
footerDs = os.path.join(DIR_DATA, "footer.ds")

def Runtime(path):
	run_pattern = re.compile("""\WRuntime\W.+""")
	results = run_pattern.search(path)
	if results:
		results = results.group()
		results = os.path.normpath(results)
		results = string.join(string.split(results,"\\"),"/")
		results = string.join(string.split(results,":"),"/")
		if not results[0] == "/": results = "/" + results
		return results.strip()
	else:
		return os.path.normpath(path)

def getNodeColor(node):
	colors = []
	for ip in node.Inputs():
		if ip.Type() == poser.kNodeInputCodeCOLOR:
			colors.append(ip.Value())
	R, G, B = 1, 1, 1
	for r, g, b in colors:
		R = R * r
		G = G * g
		B = B * b
	return R, G, B

def getInputMap(input):
	map = None
	node = input.InNode()
	if node:
		if node.Type() == poser.kNodeTypeCodeIMAGEMAP:
			if node.InputByInternalName("Image_Source"):
				map = ', "%s"' % Runtime(node.InputByInternalName("Image_Source").Value())
		else:
			for ip in node.Inputs():
				map = getInputMap(ip)
				if map:	break
	return map

def rgb255(x):
	return int(255*x)

def getInputColor(input):
	if input.Type() != poser.kNodeInputCodeCOLOR:
		return None
	r, g, b = input.Value()
	return rgb255(r), rgb255(g), rgb255(b)

def getInputValue(input):
	if input.Type() != poser.kNodeInputCodeFLOAT:
		return None
	return input.Value()

def getInputRefraction(input):
	eta = 1
	node = input.InNode()
	if not node:
		return eta
	if node.Type() == poser.kNodeTypeCodeREFRACT:
		eta = node.Input(1).Value()
	return eta

def getDSProperties(material):
	ps = material.ShaderTree().Node(0)
	if ps.Type() != poser.kNodeTypeCodePOSERSURFACE:
		return 0
	KD_R, KD_G, KD_B = getInputColor( ps.InputByInternalName("Diffuse_Color") )
	KD_CM = getInputMap( ps.InputByInternalName("Diffuse_Color") )
	KD = getInputValue( ps.InputByInternalName("Diffuse_Value") )
	KD_VM = getInputMap( ps.InputByInternalName("Diffuse_Value") )
	NS = 1 - getInputValue( ps.InputByInternalName("Roughness") )
	NS_VM = getInputMap( ps.InputByInternalName("Roughness") )
	KS_R, KS_G, KS_B = getInputColor( ps.InputByInternalName("Highlight_Color") )
	KS_CM = getInputMap( ps.InputByInternalName("Highlight_Color") )
	KS = getInputValue( ps.InputByInternalName("Highlight_Value") )
	KS_VM = getInputMap( ps.InputByInternalName("Highlight_Value") )
	KA_R, KA_G, KA_B = getInputColor( ps.InputByInternalName("Ambient_Color") )
	KA_CM = getInputMap( ps.InputByInternalName("Ambient_Color") )
	KA = getInputValue( ps.InputByInternalName("Ambient_Value") )
	KA_VM = getInputMap( ps.InputByInternalName("Ambient_Value") )
	OS = 1 - getInputValue( ps.InputByInternalName("Transparency_Max") )
	OS_VM = getInputMap( ps.InputByInternalName("Transparency_Max") )
	if OS_VM: OS = 1
	BU = getInputValue( ps.InputByInternalName("Bump") )
	BU_VM = getInputMap( ps.InputByInternalName("Bump") )
	DI = getInputValue( ps.InputByInternalName("Displacement") )
	DI_VM = getInputMap( ps.InputByInternalName("Displacement") )
	KR_R, KR_G, KR_B = getInputColor( ps.InputByInternalName("Reflection_Color") )
	KR_CM = getInputMap( ps.InputByInternalName("Reflection_Color") )
	KR = getInputValue( ps.InputByInternalName("Reflection_Value") )
	KR_VM = getInputMap( ps.InputByInternalName("Reflection_Value") )
	ETA = getInputRefraction( ps.InputByInternalName("Refraction_Color") )
	KT_R, KT_G, KT_B = getInputColor( ps.InputByInternalName("Refraction_Color") )
	KT_CM = getInputMap( ps.InputByInternalName("Refraction_Color") )
	KT = getInputValue( ps.InputByInternalName("Refraction_Value") )
	KT_VM = getInputMap( ps.InputByInternalName("Refraction_Value") )

def lookForNode( shaderTree, nodeType ):
	for node in shaderTree.Nodes():
		if node.Type() == nodeType:
			return 1
	return 0

def getLightingModel( material ):
	st = material.ShaderTree()
	if lookForNode( st, poser.kNodeTypeCodeSKIN ):
		return 2
	elif lookForNode( st, poser.kNodeTypeCodeGLOSSY ):
		return 3
	elif lookForNode( st, poser.kNodeTypeCodePHONG ):
		return 1
	elif lookForNode( st, poser.kNodeTypeCodeBLINN ):
		return 1
	else:
		return 0

class DsMaterialProperties:
	def __init__(self):
		fi = open(headerDs,'r')
		self.header = fi.read()
		fi.close()
		fi = open(footerDs, 'r')
		self.footer = fi.read()
		fi.close()
		self.cases = ""
	def get(self):
		return self.header + self.cases + self.footer
	def addMaterial(self, material):
		self.add( 'case "%s":' % material.Name() )
		ps = material.ShaderTree().Node(0)
		if ps.Type() != poser.kNodeTypeCodePOSERSURFACE:
			return 0
		KD_R, KD_G, KD_B = getInputColor( ps.InputByInternalName("Diffuse_Color") )
		KD_CM = getInputMap( ps.InputByInternalName("Diffuse_Color") )
		if not KD_CM: KD_CM = ""
		KD = getInputValue( ps.InputByInternalName("Diffuse_Value") )
		KD_VM = getInputMap( ps.InputByInternalName("Diffuse_Value") )
		if not KD_VM: KD_VM = ""
		NS = 1 - getInputValue( ps.InputByInternalName("Roughness") )
		NS_VM = getInputMap( ps.InputByInternalName("Roughness") )
		if not NS_VM: NS_VM = ""
		KS_R, KS_G, KS_B = getInputColor( ps.InputByInternalName("Highlight_Color") )
		KS_CM = getInputMap( ps.InputByInternalName("Highlight_Color") )
		if not KS_CM: KS_CM = ""
		KS = getInputValue( ps.InputByInternalName("Highlight_Value") )
		KS_VM = getInputMap( ps.InputByInternalName("Highlight_Value") )
		if not KS_VM: KS_VM = ""
		KA_R, KA_G, KA_B = getInputColor( ps.InputByInternalName("Ambient_Color") )
		KA_CM = getInputMap( ps.InputByInternalName("Ambient_Color") )
		if not KA_CM: KA_CM = ""
		KA = getInputValue( ps.InputByInternalName("Ambient_Value") )
		KA_VM = getInputMap( ps.InputByInternalName("Ambient_Value") )
		if not KA_VM: KA_VM = ""
		OS = 1 - getInputValue( ps.InputByInternalName("Transparency_Max") )
		OS_VM = getInputMap( ps.InputByInternalName("Transparency_Max") )
		if not OS_VM: OS_VM = ""
		else: OS = 1
		BU = getInputValue( ps.InputByInternalName("Bump") )
		BU_VM = getInputMap( ps.InputByInternalName("Bump") )
		if not BU_VM: BU_VM = ""
		DI = getInputValue( ps.InputByInternalName("Displacement") )
		DI_VM = getInputMap( ps.InputByInternalName("Displacement") )
		if not DI_VM: DI_VM = ""
		KR_R, KR_G, KR_B = getInputColor( ps.InputByInternalName("Reflection_Color") )
		KR_CM = getInputMap( ps.InputByInternalName("Reflection_Color") )
		if not KR_CM: KR_CM = ""
		KR = getInputValue( ps.InputByInternalName("Reflection_Value") )
		if not ps.InputByInternalName("Reflection_Value").InNode(): KR = 0
		KR_VM = getInputMap( ps.InputByInternalName("Reflection_Value") )
		if not KR_VM: KR_VM = ""
		ETA = getInputRefraction( ps.InputByInternalName("Refraction_Color") )
		KT_R, KT_G, KT_B = getInputColor( ps.InputByInternalName("Refraction_Color") )
		KT_CM = getInputMap( ps.InputByInternalName("Refraction_Color") )
		if not KT_CM: KT_CM = ""
		KT = getInputValue( ps.InputByInternalName("Refraction_Value") )
		if not ps.InputByInternalName("Refraction_Value").InNode(): KT = 0
		KT_VM = getInputMap( ps.InputByInternalName("Refraction_Value") )
		if not KT_VM: KT_VM = ""
		KS_MUL = 0
		LT_MODEL = getLightingModel(material)
		#print KD_R, KD_G, KD_B, KD_CM
		#print KD, KD_VM
		#print NS, NS_VM
		#print KS_R, KS_G, KS_B, KS_CM
		#print KS_MUL
		#print KA_R, KA_G, KA_B, KA_CM
		#print KA, KA_VM
		#print OS, OS_VM
		#print BU, BU_VM
		#print DI, DI_VM
		#print KR_R, KR_G, KR_B, KR_CM
		#print KR, KR_VM
		#print KT_R, KT_G, KT_B, KT_CM
		#print KT, KT_VM
		#print ETA
		#print LT_MODEL
		for item in [	'\tm_sMaterialType = "DzDefaultMaterial";',
				'\tm_sDefinitionFile = undefined;',
				'\tprepareMaterial();',
				'\tsetColorProperty( "Diffuse Color", [ [ %i, %i, %i ] ] %s);' % (KD_R, KD_G, KD_B, KD_CM),
				'\tsetNumericProperty( "Diffuse Strength", [ %f ] %s);' % (KD, KD_VM),
				'\tsetNumericProperty( "Glossiness", [ %f ] %s);' % (NS, NS_VM),
				'\tsetColorProperty( "Specular Color", [ [ %i, %i, %i ] ] %s);' % (KS_R, KS_G, KS_B, KS_CM),
				'\tsetNumericProperty( "Specular Strength", [ %f ] %s);' % (KS, KS_VM),
				'\tsetNumericProperty( "Multiply Specular Through Opacity", [ %i ]);' % KS_MUL,
				'\tsetColorProperty( "Ambient Color", [ [ %i, %i, %i ] ] %s);' % (KA_R, KA_G, KA_B, KA_CM),
				'\tsetNumericProperty( "Ambient Strength", [ %f ] %s);' % (KA, KA_VM),
				'\tsetNumericProperty( "Opacity Strength", [ %f ] %s);' % (OS, OS_VM),
				'\tsetNumericProperty( "Bump Strength", [ %f ] %s);' % (BU, BU_VM),
				'\tsetNumericProperty( "Negative Bump", [ %f ] );' % (BU * -1),
				'\tsetNumericProperty( "Positive Bump", [ %f ] );' % (BU),
				'\tsetNumericProperty( "Displacement Strength", [ %f ] %s);' % (1.0, DI_VM),
				'\tsetNumericProperty( "Minimum Displacement", [ %f ] );' % (0),
				'\tsetNumericProperty( "Maximum Displacement", [ %f ] );' % (DI),
				'\tsetColorProperty( "Reflection Color", [ [ %i, %i, %i ] ] %s);' % (KR_R, KR_G, KR_B, KR_CM),
				'\tsetNumericProperty( "Reflection Strength", [ %f ] %s);' % (KR, KR_VM),
				'\tsetColorProperty( "Refraction Color", [ [ %i, %i, %i ] ] %s);' % (KT_R, KT_G, KT_B, KT_CM),
				'\tsetNumericProperty( "Refraction Strength", [ %f ] %s);' % (KT, KT_VM),
				'\tsetNumericProperty( "Index of Refraction", [ %f ] );' % ETA,
				'\tsetNumericProperty( "Lighting Model", [ %i ] );' % LT_MODEL,
				'\tbreak;'	]:
			self.add(item)
	def add(self, data):
		self.cases = self.cases + "\n\t\t\t" + data

if __name__ == '__main__':
	dsPropBuilder = DsMaterialProperties()
	dsPropBuilder.addMaterial( poser.Scene().CurrentMaterial() )
	print dsPropBuilder.get()

pass
