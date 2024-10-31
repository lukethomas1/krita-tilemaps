import inspect
def getInfo(target):
    [print(item) for item in inspect.getmembers(target) if not item[0].startswith('_')]


doc = Krita.instance().activeDocument()
root = doc.rootNode();

#clone = doc.activeNode().clone()
prefix = doc.activeNode().name()
clone = doc.createCloneLayer(f"{prefix}2", doc.activeNode())
root.addChildNode(clone, None)

clone.move(100, 100)

current_node = doc.activeNode()

target = 128
#if current_node.height() == target and current_node.width() == target:
    #print(f"Current doc is {target} HxW")
    # Copy current doc, create new 1024x1024, paste to new, clone

#getInfo(current_node)
print("valid5")

#getInfo(doc.activeNode())