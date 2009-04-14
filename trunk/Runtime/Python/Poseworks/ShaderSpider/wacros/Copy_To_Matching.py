import os, sys, poser, string

os.chdir( os.path.dirname(poser.AppLocation()) )

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

import ss6Node

def askForTerms():
    dlg = poser.DialogTextEntry(message="""\n\nEnter matching terms.\n\n\nExample: "skin lash" matches\nboth "SkinHead" and "Eyelashes".\n\n\n""")
    if dlg.Show():
        return dlg.Text()
    else:
        return None

def makeRegex(text):
    words = string.split(text)
    terms = []
    for word in words:
        terms.append( "(" + re.sub("\W","",word) + ")" )
    return string.join(terms, "|")

text = askForTerms()
if text:
    terms = makeRegex(text)
    ss6Node.copyToMatching(terms)
else:
    pass
