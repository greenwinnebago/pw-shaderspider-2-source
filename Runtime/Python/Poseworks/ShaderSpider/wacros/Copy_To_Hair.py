import os, sys, poser

os.chdir( os.path.dirname(poser.AppLocation()) )

sys.path.append(os.path.join("Runtime","Python","PoseWorks","ShaderSpider","Data"))

import ss6Node

ss6Node.copyToMatching("""(brow)|(lash)|(pubic)|(hair)""")
