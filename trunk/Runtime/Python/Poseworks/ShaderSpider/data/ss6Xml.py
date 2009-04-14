import poser, string, os, sys, re

if float(poser.Version()) >= 7:
    import re
else:
    import pre as re

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

from ss6Constants import *
import ss6Node, ss6Materials

class PzrRect:
	def __init__(self, id=1, left=43, top=96, right=53, bottom=106):
		self.id = id
		self.top = top
		self.left = left
		self.right = right
		self.bottom = bottom

class PzrText:
	def __init__(self, color=-16777216, size=14, align=0, font=0, italic=0, antialiased=1, offsetX=0, offsetY=0):
		self.color = color
		self.size = size
		self.align = align
		self.font = font
		self.italic = italic
		self.antialiased = antialiased
		self.offsetX = offsetX
		self.offsetY = offsetY

class PzrPillow:
	def __init__(self, left=-1, middle=-1, right=-1, lbtn=26020, mbtn=26019, rbtn=26018):
		self.left = left
		self.middle = middle
		self.right = right
		self.lbtn = lbtn
		self.mbtn = mbtn
		self.rbtn = rbtn

class XMLTag:
	def __init__(self, type="Widget", opener="<", closer="/>", spacer=" "):
		self.type = type
		self.closer = closer
		self.spacer = spacer
		self.string = opener + type + spacer
	def addValue(self, arg, value):
		if value == "none": return None
		if type(arg) != type("string"):
			arg = repr(arg)
		if type(value) != type("string"):
			value = repr(value)
		self.string = self.string + arg + '="' + value + '"' + self.spacer
	def close(self):
		self.string = self.string + self.closer
		return self.string
	def get(self):
		return self.string

class PzrWidgetList:
	def __init__(self, file, PSDFiles=["./runtime/ui/26000_utility.psd"], margin_left=20, margin_top=30, margin_right=20, margin_bottom=30):
		self.xml = """<?xml version="1.0"?>"""
		self.addXML( self.addTag("WidgetList", {"XmlFile":file}, closer=">"), indent=0)
		for PSD in PSDFiles:
			self.addXML( self.addTag("PSDFile", {"name":PSD}), indent=1 )
		self.addXML( PzrBackground("Background").place(-10,-10), indent=1)
		self.addXML( PzrTopLeftBorder(width=margin_left, height=margin_top).place(0,0), indent=1)
		self.addXML( PzrTopCenterBorder(width=margin_left, height=margin_top).place(0,0), indent=1)
		self.addXML( PzrTopRightBorder(width=margin_right, height=margin_top).place(0,0), indent=1)
		self.addXML( PzrLeftBorder(width=margin_left, height=margin_top).place(0,0), indent=1)
		self.addXML( PzrRightBorder(width=margin_right, height=margin_top).place(0,0), indent=1)
		self.addXML( PzrBottomLeftBorder(width=margin_left, height=margin_bottom).place(0,0), indent=1)
		self.addXML( PzrBottomCenterBorder(width=margin_left, height=margin_bottom).place(0,0), indent=1)
		self.addXML( PzrBottomRightBorder(width=margin_right, height=margin_bottom).place(0,0), indent=1)
		#self.addXML( PzrWidget("topLeftDlgBorder", pictRes=26084, rect=PzrRect(0,0,20,30)).place(0,0)
	def addXML(self, tag, indent=0):
		txt = self.xml + "\n\n"
		for i in range(indent):
			txt = txt + "\t"
		txt = txt + tag
		self.xml = txt
	def addTag(self, type, values, opener="<", closer="/>"):
		tag = XMLTag(type=type, opener=opener, closer=closer)
		for key in values.keys():
			tag.addValue(key, values[key])
		tag.close()
		return tag.get()
	def close(self):
		self.addXML( self.addTag("StringResIDs", {"major":0}), indent=1)
		self.addXML( self.addTag("WidgetList", {}, opener="</",closer=">"), indent=0)
		return self.xml

class PzrWidget:
	command = "none"
	groupID = "none"
	pictRes = "none"
	hiliteRes = "none"
	behaviorProcID = "none"
	preliteAction = "none"
	bb = "none"
	persistBetweenRooms = "none"
	rect = "none"
	useRectClick = "none"
	pin = "none"
	color = "none"
	fadeMax = "none"
	tile = "none"
	isStringID = "none"
	text = "none"
	padding = "none"
	pillow = "none"
	widgetText = "none"
	useAlpha = "none"
	widgetProcID = "none"
	def AddButtonCallback(self, dialog, callback):
		dialog.AddButtonCallback(name=self.widgetName, callback=callback)
	def SetButtonValue(dialog, value):
		dialog.SetButtonValue(name=self.widgetName, value=value)
	def SetText(self, dialog, message):
		dialog.SetText(name=self.widgetName, text=message)
	def __init__(self, widgetName, command=command, groupID=groupID, pictRes=pictRes, hiliteRes=hiliteRes, behaviorProcID=behaviorProcID, preliteAction=preliteAction, bb=bb, persistBetweenRooms=persistBetweenRooms, rect=rect, useRectClick=useRectClick, pin=pin, color=color, fadeMax=fadeMax, tile=tile, isStringID=isStringID, text=text, padding=padding, pillow=pillow, widgetText=widgetText, useAlpha=useAlpha, widgetProcID=widgetProcID):
		self.widgetName = widgetName
		self.command = command
		self.groupID = groupID
		self.pictRes = pictRes
		self.hiliteRes = hiliteRes
		self.behaviorProcID = behaviorProcID
		self.preliteAction = preliteAction
		self.bb = bb
		self.persistBetweenRooms = persistBetweenRooms
		self.rect = rect
		self.useRectClick = useRectClick
		self.pin = pin
		self.color = color
		self.fadeMax = fadeMax
		self.tile = tile
		self.isStringID = isStringID
		self.text = text
		self.padding = padding
		self.pillow = pillow
		self.widgetText = widgetText
		self.useAlpha = useAlpha
		self.widgetProcID = widgetProcID
	def place(self, x, y):
		self.xml = XMLTag(type="Widget")
		self.xml.addValue("name", self.widgetName)
		self.xml.addValue("command", self.command)
		self.xml.addValue("groupID", self.groupID)
		self.xml.addValue("pictRes", self.pictRes)
		self.xml.addValue("hiliteRes", self.hiliteRes)
		self.xml.addValue("behaviorProcID", self.behaviorProcID)
		self.xml.addValue("widgetProcID", self.widgetProcID)
		self.xml.addValue("preliteAction", self.preliteAction)
		if self.bb != "none":
			self.xml.addValue("left",self.bb.left + x)
			self.xml.addValue("top", self.bb.top + y)
			self.xml.addValue("right", self.bb.right + x)
			self.xml.addValue("bottom", self.bb.bottom + y)
		self.xml.addValue("persistBetweenRooms", self.persistBetweenRooms)
		self.xml.addValue("useRectClick", self.useRectClick)
		if self.rect != "none":
			self.xml.addValue("rect.left", self.rect.left + x)
			self.xml.addValue("rect.top", self.rect.top + y)
			self.xml.addValue("rect.right", self.rect.right + x)
			self.xml.addValue("rect.bottom", self.rect.bottom + y)
		if self.pin != "none":
			self.xml.addValue("pinID", self.pin.id)
			self.xml.addValue("pinTop", self.pin.top)
			self.xml.addValue("pinLeft", self.pin.left)
			self.xml.addValue("pinBottom", self.pin.bottom)
			self.xml.addValue("pinRight", self.pin.right)
		self.xml.addValue("color", self.color)
		self.xml.addValue("fadeMax", self.fadeMax)
		self.xml.addValue("tile", self.tile)
		self.xml.addValue("isStringID", self.isStringID)
		if self.text != "none":
			self.xml.addValue("textColor", self.text.color)
			self.xml.addValue("textSize", self.text.size)
			self.xml.addValue("textAlign", self.text.align)
			self.xml.addValue("textFont", self.text.font)
			self.xml.addValue("textItalic", self.text.italic)
			self.xml.addValue("textAntialiased", self.text.antialiased)
			self.xml.addValue("textOffsetX", self.text.offsetX)
			self.xml.addValue("textOffsetY", self.text.offsetY)
		self.xml.addValue("padding", self.padding)
		if self.pillow != "none":
			self.xml.addValue("leftPillowID", self.pillow.left)
			self.xml.addValue("middlePillowID", self.pillow.middle)
			self.xml.addValue("rightPillowID", self.pillow.right)
			self.xml.addValue("leftButtonID", self.pillow.lbtn)
			self.xml.addValue("middleButtonID", self.pillow.mbtn)
			self.xml.addValue("rightButtonID", self.pillow.rbtn)
		self.xml.addValue("widgetText", self.widgetText)
		self.xml.addValue("useAlpha", self.useAlpha)
		self.xml.close()
		return self.xml.get()

def PzrBackground(widgetName, command=0, pictRes=26076, behaviorProcID=4, bb=PzrRect(left=0, top=0, right=26, bottom=26), persistBetweenRooms=1, rect=PzrRect(left=0, top=0, right=480, bottom=400), pin=PzrRect(id=1, left=1, top=3, right=2, bottom=4), color=-1, fadeMax=0, tile=1):
	return PzrWidget(widgetName, command=command, pictRes=pictRes, behaviorProcID=behaviorProcID, bb=bb, persistBetweenRooms=persistBetweenRooms, rect=rect, pin=pin, color=color, fadeMax=fadeMax, tile=tile)

def PzrBorder(widgetName="topLeftDlgBorder",  command=0,  pictRes=26084,  behaviorProcID=4,  pin=PzrRect(id=1,left=1,top=3,right=1,bottom=3),  bb=PzrRect(left=0,top=0,bottom=30,right=20),  persistBetweenRooms=1, rect=PzrRect(left=0,top=0,right=20,bottom=30),  color=-1,  fadeMax=0, tile="none"):
	return PzrWidget(widgetName,  command=command,  pictRes=pictRes,  behaviorProcID=behaviorProcID,  pin=pin,  bb=bb,  persistBetweenRooms=persistBetweenRooms, rect=rect,  color=color,  fadeMax=fadeMax, tile=tile)

def PzrTopLeftBorder(width=20, height=30):
	return PzrBorder(widgetName="topLeftDlgBorder",  pictRes=26084,  pin=PzrRect(id=1,left=1,top=3,right=1,bottom=3),  bb=PzrRect(left=0,top=0,bottom=height,right=width), rect=PzrRect(left=0,top=0,right=20,bottom=30))

def PzrTopCenterBorder(height=30, width=20):
	return PzrBorder(widgetName="topCenterDlgBorder",  pictRes=26083,  pin=PzrRect(id=1,left=1,top=3,right=2,bottom=3),  bb=PzrRect(left=width,top=0,bottom=height-3,right=width+40), rect=PzrRect(left=20,top=0,right=560,bottom=27), tile=1)

def PzrTopRightBorder(width=20, height=30):
	return PzrBorder(widgetName="topRightDlgBorder",  pictRes=26082,  pin=PzrRect(id=1,left=2,top=3,right=2,bottom=3),  bb=PzrRect(left=-1*width,top=0,bottom=height,right=0), rect=PzrRect(left=-20,top=0,right=0,bottom=30))

def PzrLeftBorder(width=20, height=30):
	return PzrBorder(widgetName="leftDlgBorder",  pictRes=26081,  pin=PzrRect(id=1,left=1,top=3,right=1,bottom=4),  bb=PzrRect(left=0,top=height,bottom=-1*height,right=width-6), rect=PzrRect(left=0,top=80,right=14,bottom=420), tile=1)

def PzrRightBorder(width=20, height=30):
	return PzrBorder(widgetName="rightDlgBorder",  pictRes=26080,  pin=PzrRect(id=1,left=2,top=3,right=2,bottom=4),  bb=PzrRect(left=-1*width+6,top=height,bottom=-1*height,right=0), rect=PzrRect(left=486,top=80,right=500,bottom=420), tile=1)

def PzrBottomLeftBorder(width=20, height=30):
	return PzrBorder(widgetName="bottomLeftDlgBorder",  pictRes=26079,  pin=PzrRect(id=1,left=1,top=4,right=1,bottom=4),  bb=PzrRect(left=0,top=-1*height-10,bottom=0,right=width), rect=PzrRect(left=0,top=410,right=20,bottom=450))

def PzrBottomCenterBorder(width=20, height=30):
	return PzrBorder(widgetName="bottomMiddleDlgBorder",  pictRes=26078,  pin=PzrRect(id=1,left=1,top=4,right=2,bottom=4),  bb=PzrRect(left=width,top=-1*height-5,bottom=0,right=-1*width), rect=PzrRect(left=20,top=415,right=480,bottom=450), tile=1)

def PzrBottomRightBorder(width=-20,height=30):
	return PzrBorder(widgetName="bottomRightDlgBorder",  pictRes=26077,  pin=PzrRect(id=1,left=2,top=4,right=2,bottom=4),  bb=PzrRect(left=-1*width,top=-1*height-10,bottom=0,right=0), rect=PzrRect(left=480,top=410,right=500,bottom=450))

def PzrRadiobutton(widgetName, command=10002, groupID=23, pictRes=26072, hiliteRes=26071, behaviorProcID=3, preliteAction=1, bb=PzrRect(left=0,top=0,right=10,bottom=10), rect=PzrRect(left=0,top=0,right=10,bottom=10), useRectClick=1, pin=PzrRect(id=1,left=1,top=3,right=1,bottom=3), color=-1, fadeMax=0):
	return PzrWidget(widgetName, command=command, groupID=groupID, pictRes=pictRes, hiliteRes=hiliteRes, behaviorProcID=behaviorProcID, preliteAction=preliteAction, bb=bb, rect=rect, useRectClick=useRectClick, pin=pin, color=color, fadeMax=fadeMax)

def PzrCheckbutton(widgetName, command=10002, groupID=23, pictRes=26105, hiliteRes=26104, behaviorProcID=3, preliteAction=1, bb=PzrRect(left=0,top=0,right=17,bottom=18), rect=PzrRect(left=0,top=0,right=17,bottom=18), useRectClick=1, pin=PzrRect(id=1,left=1,top=3,right=1,bottom=3), color=-1, fadeMax=0):
	return PzrWidget(widgetName, command=command, groupID=groupID, pictRes=pictRes, hiliteRes=hiliteRes, behaviorProcID=behaviorProcID, preliteAction=preliteAction, bb=bb, rect=rect, useRectClick=useRectClick, pin=pin, color=color, fadeMax=fadeMax)

def PzrMessage(widgetName, command=0, groupID=23, widgetProcID=3, widgetText="0:2", isStringID=1, text=PzrText(), preliteAction=6, pin=PzrRect(id=1,top=3,left=1,bottom=3,right=1), rect=PzrRect(left=0,top=0,right=116,bottom=21), bb=PzrRect(left=0,top=0,right=116,bottom=21), color=-1, fadeMax=0):
	return PzrWidget(widgetName, command=command, groupID=groupID, widgetProcID=widgetProcID, widgetText=widgetText, isStringID=isStringID, text=text, preliteAction=preliteAction, pin=pin, rect=rect, bb=bb, color=color, fadeMax=fadeMax)

def PzrButtonWidget(widgetName, command=10001, groupID=4, pictRes=26019, widgetProcID=23, padding=12, pillow=PzrPillow(), widgetText="0:2", isStringID=1, text=PzrText(color=-16777216,size=16,align=0), behaviorProcID=1, useAlpha=0, preliteAction=1, pin=PzrRect(id=1,top=3,left=1,bottom=3,right=1), bb=PzrRect(left=0,top=0,right=60,bottom=20), persistBetweenRooms=1, rect=PzrRect(left=0,top=0,right=60,bottom=20), color=-16777216, fadeMax=0):
	return PzrWidget(widgetName, command=command, groupID=4, pictRes=pictRes, widgetProcID=widgetProcID, padding=padding, pillow=pillow, widgetText=widgetText, isStringID=isStringID, text=text, behaviorProcID=behaviorProcID, useAlpha=useAlpha, preliteAction=preliteAction, pin=pin, bb=bb, persistBetweenRooms=persistBetweenRooms, rect=rect, color=color, fadeMax=fadeMax)

def PzrImage(widgetName, command=0, pictRes=26084, behaviorProcID=4, pin=PzrRect(id=1,left=1,top=3,right=1,bottom=3), bb=PzrRect(left=0,top=0,bottom=64,right=64), persistBetweenRooms=1, rect=PzrRect(left=0,top=0,right=64,bottom=64),  color=-1,  fadeMax=0, tile="none"):
	return PzrWidget(widgetName, command=command, pictRes=pictRes, behaviorProcID=behaviorProcID, pin=pin, bb=bb, persistBetweenRooms=persistBetweenRooms, rect=rect,  color=color,  fadeMax=fadeMax, tile=tile)

class PzrRadio:
	def __init__(self, widgetName, command=10002, groupID=23, width=126, height=21):
		self.widgetName = widgetName
		self.command = command
		self.groupID = groupID
		self.btn = PzrRadiobutton(widgetName, command=command, groupID=groupID)
		self.msg = PzrMessage(widgetName + "Message", command=command, groupID=groupID, bb=PzrRect(left=6,top=-12,right=width-10,bottom=height-10))
		self.width = width
		self.height = height
	def place(self, x, y):
		return "\t" + self.btn.place(x, y) + "\n\t" + self.msg.place(x+10,y+10)
	def SetText(self, dialog, message):
		self.msg.SetText(dialog, message)

class PzrCheck:
	def __init__(self, widgetName, command=10002, groupID=23, width=126, height=21):
		self.widgetName = widgetName
		self.command = command
		self.groupID = groupID
		self.btn = PzrCheckbutton(widgetName, command=command, groupID=groupID)
		self.msg = PzrMessage(widgetName + "Message", command=command, groupID=groupID, bb=PzrRect(left=8,top=-8,right=width-10,bottom=height-10))
		self.width = width
		self.height = height
	def place(self, x, y):
		return "\t" + self.btn.place(x, y) + "\n\t" + self.msg.place(x+10,y+10)
	def SetText(self, dialog, message):
		self.msg.SetText(dialog, message)

class PzrRadioPane:
	def __init__(self, groupID=23, initCommand=10002, itemsPerCol=13):
		self.buttons = []
		self.var = 0
		self.initCommand = initCommand
		self.curCommand = initCommand
		self.groupID = groupID
		self.itemsPerCol = itemsPerCol
	def AddRadiobutton(self, widgetName):
		command = self.curCommand
		self.curCommand = command + 1
		self.buttons.append( PzrRadio(widgetName, command=command, groupID=self.groupID) )
	def SetText(self, dialog):
		for button in self.buttons:
			button.SetText(dialog, button.widgetName)
	def place(self, x, y):
		self.xml = ""
		curx = x
		cury = y
		i = 1
		for button in self.buttons:
			self.xml = self.xml + "\n" + button.place(curx, cury)
			curx = x + int(i / self.itemsPerCol) * button.width
			cury = y + int(i % self.itemsPerCol) * button.height
			i = i + 1
		return self.xml
	def get(self):
		return self.var
	def set(self, dialog, value):
		self.var = value
		for button in self.buttons:
			if button.widgetName == value: continue
			dialog.SetButtonValue(name=button.widgetName, value=0)
		dialog.SetButtonValue(name=value, value=1)
	def SetValues(self, dialog):
		self.dialog = dialog
		for button in self.buttons:
			dialog.AddButtonCallback(name=button.widgetName, callback=lambda v, s=self, d=dialog, n=button.widgetName: s.set(d,n))
			dialog.SetButtonValue(name=button.widgetName, value=0)
		try:
        		dialog.SetButtonValue(self.buttons[0].widgetName, value=1)
        	except:
                        pass

class PzrCheckPane:
	def __init__(self, groupID=23, initCommand=10002, itemsPerCol=13):
		self.buttons = []
		self.selected = []
		self.initCommand = initCommand
		self.curCommand = initCommand
		self.groupID = groupID
		self.itemsPerCol = itemsPerCol
	def AddCheckbutton(self, widgetName, width=126, height=21):
		command = self.curCommand
		self.curCommand = command + 1
		return self.AddButton( PzrCheck(widgetName, command=command, groupID=self.groupID, width=width, height=height) )
	def AddButton(self, button):
		self.buttons.append(button)
		return button
	def SetText(self, dialog):
		for button in self.buttons:
			button.SetText(dialog, button.widgetName)
	def place(self, x, y):
		self.xml = ""
		curx = x
		cury = y
		i = 1
		for button in self.buttons:
			self.xml = self.xml + "\n" + button.place(curx, cury)
			curx = x + int(i / self.itemsPerCol) * button.width
			cury = y + int(i % self.itemsPerCol) * button.height
			i = i + 1
		return self.xml
	def get(self):
		return self.selected
	def select(self, dialog, widgetName):
		if not widgetName in self.selected:
			self.selected.append(widgetName)
		dialog.SetButtonValue(name=widgetName, value=1)
	def deselect(self, dialog, widgetName):
		if widgetName in self.selected:
			self.selected.remove(widgetName)
		dialog.SetButtonValue(name=widgetName, value=0)
	def set(self, dialog, value):
		if value in self.selected:
			self.selected.remove(value)
			dialog.SetButtonValue(name=value, value=0)
		else:
			self.selected.append(value)
			dialog.SetButtonValue(name=value, value=1)
	def SetValues(self, dialog):
		self.dialog = dialog
		for button in self.buttons:
			dialog.AddButtonCallback(name=button.widgetName, callback=lambda v, s=self, d=dialog, n=button.widgetName: s.set(d,n))
			dialog.SetButtonValue(name=button.widgetName, value=0)

def xmlFormatPath(path):
	path = string.join(string.split(path,"\\"),"/")
	if path[0] == "r" or path[0] == "R":
                path = "./" + path
	return path

def writeXML(path, data):
	fi = open(path,'w')
	fi.write(data)
	fi.close()
	return path

def OkButton():
	return PzrWidget(widgetName="okBtn",  command=7001,  groupID=4,  pictRes=26016,  behaviorProcID=1,  preliteAction=1,  pin=PzrRect(id=1,top=3,left=1,bottom=3,right=1),  bb=PzrRect(left=0,top=0,bottom=19,right=58),  persistBetweenRooms=1,  rect=PzrRect(left=0,top=0,right=58,bottom=19),  color=-1,  fadeMax=0)

def CancelButton():
	return PzrWidget(widgetName="cancelBtn",  command=7002,  groupID=4,  pictRes=26017,  behaviorProcID=1,  preliteAction=1,  pin=PzrRect(id=1,top=3,left=1,bottom=3,right=1),  bb=PzrRect(left=0,top=0,bottom=19,right=58),  persistBetweenRooms=1,  rect=PzrRect(left=0,top=0,right=58,bottom=19),  color=-1,  fadeMax=0)

class PzrButton:
	def __init__(self, widgetName, command=10002, groupID=4):
		self.btn = PzrButtonWidget(widgetName, command=command, groupID=groupID)
		self.widgetName = widgetName
	def Function(self, value, dialog):
		dialog.Destroy()
		print self.widgetName
	def AddButtonCallback(self,dialog):
		dialog.AddButtonCallback(name=self.widgetName, callback=lambda v, s=self, d=dialog: s.Function(v,d))
	def SetText(self, dialog):
		dialog.SetText(self.widgetName, text=self.widgetName)
	def place(self, x, y):
		return self.btn.place(x, y)
	
class SelectInput:
	def __init__(self, inputs, title="Select an input...", text="Check all inputs to include in the selection."):
		path = os.path.join(DIR_TEMP,"selectMaterial.xml")

		xmlManager = PzrWidgetList(xmlFormatPath(path))

		self.checkPane = PzrCheckPane()
		for input in inputs:
			self.checkPane.AddCheckbutton(input, width=148)

		self.text = PzrMessage("TextBox", text=PzrText(size=18))

		xmlManager.addXML( self.text.place(60, 40), indent=1 )
		xmlManager.addXML( self.checkPane.place(20,80) )
		xmlManager.addXML( OkButton().place(390, 373) )
		xmlManager.addXML( CancelButton().place(320, 373) )
		xmlData = xmlManager.close()
		writeXML(path, xmlData)

		self.dlg = poser.Dialog( xmlFormatPath(path), title=title, message=" ", width=480, height=400)

		self.checkPane.SetText(self.dlg)
		self.checkPane.SetValues(self.dlg)

		self.dlg.SetText(name="TextBox", text=text)
	def Show(self):
		return self.dlg.Show()
	def get(self):
		return self.checkPane.get()

class SetMATOptions:
	def __init__(self, title="MAT Pose Options"):
		path = os.path.join(DIR_TEMP,"matOptions.xml")

		xmlManager = PzrWidgetList(xmlFormatPath(path))

		self.checkMap = {}
		self.opts = ["Create PNG thumbnails", "Create Poser 4 PZ2", "Create Poser Pro PZ2",
                             "Create Poser 5 PZ2", "Create Poser 6 MC6", "Create DAZ|Studio DS", "Clean up file paths"]

		self.optMap = {self.opts[0]:"doPng", self.opts[1]:"doP4", self.opts[2]:"doPP",
                               self.opts[3]:"doP5", self.opts[4]:"doP6", self.opts[5]:"doDS", self.opts[6]:"doClean"}

		self.checkPane = PzrCheckPane()
		for wN in self.opts:
			self.checkMap[wN] = self.checkPane.AddCheckbutton(wN)

		self.text = PzrMessage("TextBox", text=PzrText(size=18))

		xmlManager.addXML( self.text.place(90, 40), indent=1 )
		xmlManager.addXML( self.checkPane.place(60,80) )
		xmlManager.addXML( OkButton().place(230, 273) )
		xmlManager.addXML( CancelButton().place(160, 273) )
		xmlData = xmlManager.close()
		writeXML(path, xmlData)

		self.dlg = poser.Dialog( xmlFormatPath(path), title=title, message=" ", width=300, height=300)

		self.checkPane.SetText(self.dlg)
		self.checkPane.SetValues(self.dlg)

		self.dlg.SetText(name="TextBox", text="Save Options")
		for opt in self.opts:
                        if DIR_MANAGER.get(self.optMap[opt]):
                                self.set(opt, 1)
                                """
		if DIR_MANAGER.get("doPng"):
                        self.set(opts[0], 1)
                if DIR_MANAGER.get("doP4"):
                        self.set(opts[1], 1)
                if DIR_MANAGER.get("doPP"):
                        self.set(opts[2], 1)
                if DIR_MANAGER.get("doP5"):
                        self.set(opts[3], 1)
                if DIR_MANAGER.get("doP6"):
                        self.set(opts[4], 1)
                if DIR_MANAGER.get("doDS"):
                        self.set(opts[5], 1)
                if DIR_MANAGER.get("doClean"):
                        self.set(opts[6], 1)
                        """
	def set(self, opt, onOff):
		if onOff:
			self.checkPane.select(self.dlg, opt)
		else:
			self.checkPane.deselect(self.dlg, opt)
	def SetToMap(self, value_map):
		for widgetName in value_map.keys():
			self.set(widgetName, value_map[widgetName])
	def Show(self):
		if self.dlg.Show():
                        theGet = self.checkPane.get()
                        for opt in self.opts:
                                if opt in theGet:
                                        DIR_MANAGER.set(self.optMap[opt], 1)
                                else:
                                        DIR_MANAGER.set(self.optMap[opt], 0)
                        return 1
                else:
                        return 0
	def get(self):
		theGet = self.checkPane.get()
		ret = []
		for opt in self.opts:
			if opt in theGet:
                                DIR_MANAGER.set(self.optMap[opt], 1)
				ret.append(1)
			else:
                                DIR_MANAGER.set(self.optMap[opt], 0)
				ret.append(0)
		return ret

class SelectMaterial:
	def __init__(self, materials, title="Select materials...", text="Check all materials to include in the selection."):
		path = os.path.join(DIR_TEMP,"selectMaterial.xml")

		xmlManager = PzrWidgetList(xmlFormatPath(path))

		self.checkMap = {}

		self.checkPane = PzrCheckPane()
		for mat in materials:
			self.checkMap[mat] = self.checkPane.AddCheckbutton(mat)

		self.text = PzrMessage("TextBox", text=PzrText(size=18))

		xmlManager.addXML( self.text.place(60, 40), indent=1 )
		xmlManager.addXML( self.checkPane.place(20,80) )
		xmlManager.addXML( OkButton().place(390, 373) )
		xmlManager.addXML( CancelButton().place(320, 373) )
		xmlData = xmlManager.close()
		writeXML(path, xmlData)

		self.dlg = poser.Dialog( xmlFormatPath(path), title=title, message=" ", width=480, height=400)

		self.checkPane.SetText(self.dlg)
		self.checkPane.SetValues(self.dlg)

		self.dlg.SetText(name="TextBox", text=text)
	def set(self, material, onOff):
		if onOff:
			self.checkPane.select(self.dlg, material)
		else:
			self.checkPane.deselect(self.dlg, material)
	def SetToMap(self, value_map):
		for widgetName in value_map.keys():
			self.set(widgetName, value_map[widgetName])
	def Show(self):
		return self.dlg.Show()
	def get(self):
		return self.checkPane.get()

def SelectGroupMaterials(groupName, materials, value_map={}):
		matSelector = SelectMaterial(materials, text="Check all materials to include in %s." % groupName)
		matSelector.SetToMap(value_map)
		if matSelector.Show():
			return matSelector.get()
		else:
			return None

class GroupEditor:
	def __init__(self, actor, title="Group Editor", width=500, height=400, useDict=None):
		path = os.path.join(DIR_TEMP,"groupEditor.xml")

		self.actor = actor
		self.title = title
		self.width = width
		self.height = height

		self.suppressError = 0

                if useDict:
                        self.preset = useDict
                else:
        		self.preset = ss6Materials.getPreset(self.actor)
		self.presetPath = ss6Materials.getPresetPath(self.actor)
		
		self.all_groups = self.preset.keys()
		self.all_groups.sort()

		self.all_materials = ss6Materials.getMaterialNames(actor)

		self.action = 0

		xmlManager = PzrWidgetList(xmlFormatPath(path), PSDFiles=["./runtime/ui/26000_utility.psd","./runtime/python/poseworks/shaderspider/data/12000_groupEditor.psd"])

		self.radioPane = PzrRadioPane(itemsPerCol=15)
		try:
        		self.radioPane.var = self.all_groups[0]
        	except:
                        self.radioPane.var = -1
		for group in self.all_groups:
			self.radioPane.AddRadiobutton(group)

		self.actSave = "Save and Exit"
		self.actNewGroup = "New Material Group"
		self.actEdit = "Edit Selected Group"
		self.actDelete = "Delete Selected Group"

		self.actions = [self.actSave, self.actNewGroup, self.actEdit, self.actDelete]
		self.actionPane = PzrRadioPane(groupID=24, initCommand=10100)
		self.actionPane.var = self.actions[0]
		for action in self.actions:
			self.actionPane.AddRadiobutton(action)

		self.text = PzrMessage("Label", text=PzrText(size=18))

		self.saveBtn = PzrButton("Save", command=10201)

		xmlManager.addXML( PzrImage("DecoSquare", pictRes=12001, bb=PzrRect(left=0,top=0,right=193,bottom=400)).place(width-193,0) )
		xmlManager.addXML( self.text.place(width-170, 40), indent=1 )
		xmlManager.addXML( self.radioPane.place(20,40) )
		xmlManager.addXML( self.actionPane.place(width-170,80) )
		xmlManager.addXML( OkButton().place(width-90, height-27) )
		xmlManager.addXML( CancelButton().place(width-160, height-27) )
		xmlData = xmlManager.close()
		writeXML(path, xmlData)

		if len(self.all_groups) == 0:
                        msg = "No groups found."
		else:
                        msg = " "
		self.dlg = poser.Dialog(xmlFormatPath(path), title=title, message=msg, width=width, height=height)

		self.radioPane.SetText(self.dlg)
		self.radioPane.SetValues(self.dlg)

		self.actionPane.SetText(self.dlg)
		self.actionPane.SetValues(self.dlg)

		self.dlg.SetText(name="Label", text=title)
	def Save(self):
                ss6Materials.writePresetFor(self.actor, self.preset)
	def New(self):
		group = AskText()
		if group:
                        self.preset[group] = []
                        self.suppressError = 1
			self.Edit(group)
		else:
			self.Redraw()
	def Edit(self, group):
                if self.radioPane.var != -1 or self.suppressError:
                        mats = SelectGroupMaterials(group, self.all_materials, self.GetInGroup(group, self.all_materials))
                        if mats:
                                self.preset[group] = mats
                        self.suppressError = 0
                        self.Redraw()
	def Delete(self, group):
                if self.radioPane.var != -1:
                        del self.preset[group]
                        self.Redraw()
	def Redraw(self):
		GroupEditor(self.actor, title=self.title, width=self.width, height=self.height, useDict=self.preset).Show()
	def GetInGroup(self, group, materials):
                key = {}
                for mat in materials:
                        key[mat] = mat in self.preset[group]
                        
                return key
	def Show(self):
		if self.dlg.Show():
			group, act = self.get()
			if act == self.actSave:
				self.Save()
			elif act == self.actNewGroup:
				self.New()
			elif act == self.actEdit:
				self.Edit(group)
			elif act == self.actDelete:
				self.Delete(group)
			else:
				ErrorBox("Bad action type %s" % act)
	def get(self):
		return (self.radioPane.get(), self.actionPane.get())

def ErrorBox(message="Error!"):
	poser.DialogSimple.MessageBox(message)

class AskConnectNode:
	def __init__(self, inputs, possibleNodes, actionMap={}):
		self.inputs = inputs
		self.possibleNodes = possibleNodes
		self.translator = {}
		self.actionMap = actionMap
		for input in inputs:
			self.translator[input.Name()] = input
			if input.Name() not in self.actionMap:
				self.actionMap[input.Name()] = "DISCONNECT"
	def Dialog(self):
		path = os.path.join(DIR_TEMP,"askStitchNode.xml")
		xmlpath = xmlFormatPath(path)
		xmlManager = PzrWidgetList(xmlpath)

		topmsg = """Please choose an action for any node connected to these inputs."""
		botmsg = """Example: If a texture map is plugged into Diffuse_Color, when someone loads the FX6, you can"""
		botmsg2 = """have the texture automatically disconnected or plugged into another node created by the FX6."""
		topMessage = PzrMessage("topMsg",text=PzrText(size=18),rect=PzrRect(left=0,top=0,right=570,bottom=360),bb=PzrRect(left=0,top=0,right=570,bottom=360))
		xmlManager.addXML(topMessage.place(80,40))

		botMessage = PzrMessage("botMsg",rect=PzrRect(left=0,top=0,right=570,bottom=360),bb=PzrRect(left=0,top=0,right=570,bottom=360))
		xmlManager.addXML(botMessage.place(35,397))

		botMessage2 = PzrMessage("botMsg2",rect=PzrRect(left=0,top=0,right=570,bottom=360),bb=PzrRect(left=0,top=0,right=570,bottom=360))
		xmlManager.addXML(botMessage2.place(35,415))

		btns = []
		command = 10001
		for input in self.inputs:
			name = input.Name()
			label = PzrMessage(name,command=1001)
			button = PzrButtonWidget(name+"B",command=command)
			btns.append( (label, button) )
			command = command + 1
		curx = 35
		cury = 80
		i = 1
		for label, button in btns:
			xmlManager.addXML( label.place(curx, cury) )
			xmlManager.addXML( button.place(curx + 140, cury) )
			curx = 35 + int(i / 15) * 300
			cury = 80 + int(i % 15) * button.rect.bottom
			i = i + 1

		xmlManager.addXML( OkButton().place(550, 480-27) )
		xmlManager.addXML( CancelButton().place(480, 480-27) )

		xmlData = xmlManager.close()
		writeXML(path, xmlData)

		self.dlg = poser.Dialog(xmlpath, title="Reconnect nodes from...", width=640, height=480)
		self.dlg.SetText("topMsg", topmsg)
		self.dlg.SetText("botMsg", botmsg)
		self.dlg.SetText("botMsg2", botmsg2)
		for label, button in btns:
			name = label.widgetName
			self.dlg.SetText(name, name)
			self.dlg.SetText(button.widgetName, self.actionMap[name])
			self.dlg.AddButtonCallback(name=button.widgetName, callback=lambda v, s=self, n=name: s.AskConnectToWhat(n))
	def Show(self):
		self.Dialog()
		retdict = {}
		if self.dlg.Show():
			for key, value in self.actionMap.items():
				if value == "DISCONNECT":
					retdict[key] = 0
				else:
					retdict[key] = string.split(value, " : ")
		return retdict
	def AskConnectToWhat(self, inputName):
		action = self.actionMap[inputName]
		nodeList = []
		nodes = self.possibleNodes.keys()
		nodes.sort()
		st = poser.Scene().CurrentMaterial().ShaderTree()
		for key in nodes:
			for input in self.possibleNodes[key]["Inputs"].keys():
				nodeList.append( key + " : " + input)
		chosenInput = poser.DialogSimple.AskMenu("Plug connected nodes into...", "Connect to...", nodeList)
		if chosenInput:
			self.actionMap[inputName] = chosenInput
			self.dlg.SetText(inputName+"B",chosenInput)

def AskStitchNode(input, possibleNodes):
	message = "Would you like to have nodes connected to %s plugged into this effect?" % input.Name()
	if poser.DialogSimple.YesNo(message):
		return AskStitchToWhat(input, possibleNodes)
	else:
		return 0

def AskStitchToWhat(input, possibleNodes):
	nodeList = []
	nodes = possibleNodes.keys()
	nodes.sort()
	for key in nodes:
		for input in possibleNodes[key]["Inputs"].keys():
			nodeList.append( key + " : " + input)
	chosenInput = poser.DialogSimple.AskMenu("Plug connected nodes into...", "Connect to...", nodeList)
	if chosenInput:
		stitchTuple = string.split(chosenInput, " : ")
		return stitchTuple
	else:
		return 0

def AskText(message="\nEnter the name for\nthe new group."):
	txt = poser.DialogTextEntry(message=message)
	if txt.Show():
        	return txt.Text()
        else:
                return None

def AskDirectory(dir=os.path.dirname(poser.AppLocation()),title="Open...",parent=None):
	askdir = poser.DialogDirChooser(parentDialog=parent, message=title, startDir=dir)
	if askdir.Show():
		folder = askdir.Path()
		os.chdir(os.path.dirname(poser.AppLocation()))
		if not os.path.isdir(folder):
			return None
		else:
			return folder
	else:
		return None

def AskOpen(ext=".fx6",types=[("Firefly Effect","*.fx6")],dir=DIR_FX,title="Load Firefly Effect..."):
	askfile = poser.DialogFileChooser(type=poser.kDialogFileChooserOpen,message=title,startDir=dir)
	askfile.Show()
	file = askfile.Path()
	os.chdir(os.path.dirname(poser.AppLocation()))
	if not os.path.isfile(file):
		return None
	elif not string.lower(file[-4:]) == string.lower(ext):
		ErrorBox("""Bad file type: Must be %s""" % ext)
		return AskOpen(ext=ext, types=types, dir=dir, title=title)
	return file

def AskSaveAs(ext=".fx6",types=[("Firefly Effect","*.fx6")],dir=DIR_FX,title="Save as..."):
	askfile = poser.DialogFileChooser(type=poser.kDialogFileChooserSave,message="Save as...",startDir=dir)
	askfile.Show()
	file = askfile.Path()
	if os.path.isdir(file):
		file = None
	elif not string.lower(file[-4:]) == ext:
		file = file + ext
	os.chdir(os.path.dirname(poser.AppLocation()))
	return file

def AskSelectInputs(node):
	inputs = []
	for input in node.Inputs():
		inputs.append(input.InternalName())
	InputSelector = SelectInput(inputs)
	if InputSelector.Show():
		return InputSelector.get()
	else:
		return []

class AskSelectMethod:
	def __init__(self, title="Apply to...", methods=["All materials.", "Mapping group...", "Surface group...", "Specific materials...", "Matching materials...", "Current material."], width=200, height=260):
		path = os.path.join(DIR_TEMP, "askSelectMethod.xml")

		xmlManager = PzrWidgetList(xmlFormatPath(path))

		self.radioPane = PzrRadioPane()
		self.radioPane.var = methods[0]
		for method in methods:
			self.radioPane.AddRadiobutton(method)

		self.text = PzrMessage("TextBox", text=PzrText(size=18))

		xmlManager.addXML( self.text.place(60, 40), indent=1 )
		xmlManager.addXML( self.radioPane.place(20,80) )
		xmlManager.addXML( OkButton().place(width-90, height-27) )
		xmlManager.addXML( CancelButton().place(width-160, height-27) )
		xmlData = xmlManager.close()
		writeXML(path, xmlData)

		self.dlg = poser.Dialog( xmlFormatPath(path), title="Select method...", message=" ", width=width, height=height)

		self.radioPane.SetText(self.dlg)
		self.radioPane.SetValues(self.dlg)

		self.dlg.SetText(name="TextBox", text=title)
	def Show(self):
		return self.dlg.Show()
	def get(self):
		return self.radioPane.get()

class AskPosePaths:
	def __init__(self):
                self.fileName = DIR_MANAGER.get("matFileName")
                self.pz2p = DIR_MANAGER.get("pz2")
                self.mc6p = DIR_MANAGER.get("mc6")
                self.dsp = DIR_MANAGER.get("ds")
        def addPathButton(self, labelName, btnName, command):
                label = PzrMessage(labelName, command=1001)
                btn = PzrButtonWidget(btnName, command=command)
                self.btns.append( (label, btn) )
	def Dialog(self):
		path = os.path.join(DIR_TEMP,"askFilePaths.xml")
		xmlpath = xmlFormatPath(path)
		xmlManager = PzrWidgetList(xmlpath)
		
		topMessage = PzrMessage("topMsg",text=PzrText(size=18),rect=PzrRect(left=0,top=0,right=570,bottom=360),bb=PzrRect(left=0,top=0,right=570,bottom=360))
		xmlManager.addXML(topMessage.place(260,40))

		self.btns = []
		self.addPathButton("FI-L", "FI", 10001)
		self.addPathButton("PZ-L", "PZ", 10002)
		self.addPathButton("P6-L", "P6", 10003)
		self.addPathButton("DS-L", "DS", 10004)

		curx = 35
		cury = 80
		i = 1
		for label, button in self.btns:
			xmlManager.addXML( label.place(curx, cury) )
			xmlManager.addXML( button.place(curx + 210, cury) )
			curx = 35
			cury = 80 + (i % 15) * 35
			i = i + 1

		xmlManager.addXML( OkButton().place(550, 260-27) )
		xmlManager.addXML( CancelButton().place(480, 260-27) )

		xmlData = xmlManager.close()
		writeXML(path, xmlData)

		self.dlg = poser.Dialog(xmlpath, title="Reconnect nodes from...", width=640, height=260)
		self.dlg.SetText("topMsg", "Output Paths")

                self.dlg.SetText("FI-L", "Name")
                self.dlg.SetText("FI", self.fileName)
                self.dlg.AddButtonCallback(name="FI", callback=self.askFilename)
		self.dlg.SetText("PZ-L", "MAT Pose (PZ2) Folder")
		self.dlg.SetText("PZ", self.shorten(self.pz2p))
		self.dlg.AddButtonCallback(name="PZ", callback=self.askPz2)
		self.dlg.SetText("P6-L", "Material Collection (MC6) Folder")
		self.dlg.SetText("P6", self.shorten(self.mc6p))
		self.dlg.AddButtonCallback(name="P6", callback=self.askMc6)
		self.dlg.SetText("DS-L", "DAZ|Script (DS) Folder")
		self.dlg.SetText("DS", self.shorten(self.dsp))
		self.dlg.AddButtonCallback(name="DS", callback=self.askDs)
		return self.dlg
	def Show(self):
		return self.Dialog().Show()
        def shorten(self, path):
                if len(path) > 50:
                        path = "..." + path[-47:]
                return path
        def askFilename(self, v=None):
                name = AskText(message="Please enter the base file name for the MAT.\n\n\n\n\n(\"Blue\" results in \"Blue PP.pz2\"\nand \"Blue P6.mc6\")")
                if name:
                        DIR_MANAGER.set("matFileName", name)
                        self.fileName = name
                        self.dlg.SetText("FI", self.fileName)
	def askPz2(self, v=None):
                path = AskDirectory(dir=DIR_MANAGER.get("pz2"),
                                    title="Select PZ2 Folder...",
                                    parent=self.dlg)
                if path:
                        DIR_MANAGER.set("pz2", path)
                        self.pz2p = path
                        self.dlg.SetText("PZ", self.shorten(self.pz2p))
	def askMc6(self, v=None):
                path = AskDirectory(dir=DIR_MANAGER.get("mc6"),
                                    title="Select MC6 Folder...",
                                    parent=self.dlg)
                if path:
                        DIR_MANAGER.set("mc6", path)
                        self.mc6p = path
                        self.dlg.SetText("P6", self.shorten(self.mc6p))
	def askDs(self, v=None):
                path = AskDirectory(dir=DIR_MANAGER.get("ds"),
                                    title="Select DS Folder...",
                                    parent=self.dlg)
                if path:
                        DIR_MANAGER.set("ds", path)
                        self.dsp = path
                        self.dlg.SetText("DS", self.shorten(self.dsp))

if __name__ == '__main__':
	#print AskMaterials(poser.Scene().CurrentFigure())
	ge = GroupEditor(poser.Scene().CurrentFigure())
	ge.Show()
	#AskConnectNode(poser.Scene().CurrentMaterial().ShaderTree().Node(0).Inputs(), [], actionMap={"Diffuse_Color":"Apeshit"}).Dialog()
pass
