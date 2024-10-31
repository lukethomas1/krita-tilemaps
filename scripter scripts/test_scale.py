from krita import *

doc = Krita.instance().activeDocument()
root = doc.rootNode()
node = doc.activeNode()

node.scaleNode(node.position(), 256, 256, "Bicubic")