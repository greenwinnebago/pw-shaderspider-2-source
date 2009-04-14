import poser, os

DIR_POSER = os.path.dirname(poser.AppLocation())
DIR_SCRIPT = os.path.join(DIR_POSER,"Runtime","Python","PoseWorks","ShaderSpider")
DIR_PRESET = os.path.join(DIR_SCRIPT,"Presets")
DIR_DATA = os.path.join(DIR_SCRIPT,"Data")
DIR_TEMP = os.path.join(DIR_SCRIPT,"Temp")
DIR_FX = os.path.join(DIR_SCRIPT,"FX")

for d in [DIR_SCRIPT, DIR_PRESET, DIR_DATA, DIR_TEMP, DIR_FX]:
    if not os.path.exists(d):
        os.makedirs(d)

defaultPaths = {
	'ss6':DIR_PRESET,
	'fx6':DIR_FX,
	'pz2':os.path.join("Runtime","libraries"),
	'ds':os.path.join("Runtime","libraries"),
	'mc6':os.path.join("Runtime","libraries","materials"),
        "matFileName":"MAT File Name",
        "doPng":1,
        "doP4":1,
        "doPP":1,
        "doP5":1,
        "doP6":0,
        "doDS":0,
        "doClean":1,
}

class CurDirs(object):
	def __init__(self):
		self.default = defaultPaths
		self.readDirs()
	def readDirs(self):
		try:
			pths = open(os.path.join(DIR_DATA, "last.pth"), 'r')
			data = pths.read()
			pths.close()
			self.curdirs = self.default
			self.curdirs.update(eval(data))
		except:
			self.curdirs = self.default
	def writeDirs(self):
		try:
			pths = open(os.path.join(DIR_DATA, "last.pth"), 'w')
			pths.write( repr(self.curdirs) )
			pths.close()
		except:
			pass
	def set(self, key, path):
		self.curdirs[key] = path
		self.writeDirs()
	def get(self, key):
		return self.curdirs[key]

DIR_MANAGER = CurDirs()
