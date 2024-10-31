from krita import *

import inspect
def getInfo(target):
    [print(item) for item in inspect.getmembers(target) if not item[0].startswith('_')]


doc = Krita.instance().activeDocument()
root = doc.rootNode();
node = doc.activeNode()

bounds = node.bounds()

#print(f"Bounds: {dir(node.bounds())}")
print(f"x, y: {bounds.x()}, {bounds.y()}")
print(f"height, width: {bounds.height()}, {bounds.width()}")

# 0 indicates no tile
tile_locations = [
                  [0, 0, 0, 1, 1, 0, 0, 0],
                   [1, 0, 0, 1, 1, 1, 1, 1],
                    [1, 0, 0, 1, 1, 1, 1, 1],
                     [0, 1, 1, 1, 1, 1, 1, 0],
                      [0, 1, 1, 1, 1, 1, 1, 0],
                       [0, 0, 0, 0, 0, 1, 1, 0],
                        [0, 0, 0, 0, 0, 1, 1, 0],
                         [0, 0, 0, 1, 1, 0, 0, 0]
]

tile_h = bounds.height()
tile_w = bounds.width()

#clone = doc.activeNode().clone()
prefix = doc.activeNode().name()
#clone = doc.createCloneLayer(f"{prefix}2", doc.activeNode())
#root.addChildNode(clone, None)

if False:
    for row in range(len(tile_locations)):
        for column in range(len(tile_locations)):
            if tile_locations[row][column] == 1:
                clone = doc.createCloneLayer(f"{prefix}_{row}_{column}", doc.activeNode())
                offset_x = row * tile_w - bounds.x() 
                offset_y = column * tile_h - bounds.y()
                print(f"Row, column, offset_x, offset_y: {row}, {column}, {offset_x}, {offset_y}")
                clone.move(offset_y, --offset_x)
                root.addChildNode(clone, None)

#rect = QRectF(0, 0, 128, 128)
#node.paintRectangle(rect)
#getInfo(node)

def copyToOrigin(node):
    clone = doc.createCloneLayer("clone", node)
    clone.move(0 - clone.bounds().x(), 0 - clone.bounds().y())
    root.addChildNode(clone, None)
    

border = doc.nodeByName("border")
copyToOrigin(border)

print("valid23")