from krita import *
from math import pi

MASK_TEMPLATE = """
<!DOCTYPE transform_params>
<transform_params>
 <main id="tooltransformparams"/>
 <data mode="0">
  <free_transform>
   <transformedCenter type="pointf" x="X_VALUE" y="Y_VALUE"/>
   <originalCenter type="pointf" x="X_VALUE" y="Y_VALUE"/>
   <rotationCenterOffset type="pointf" x="0" y="0"/>
   <transformAroundRotationCenter type="value" value="0"/>
   <aX type="value" value="0"/>
   <aY type="value" value="0"/>
   <aZ type="value" value="RADIANS"/>
   <cameraPos z="1024" type="vector3d" x="0" y="0"/>
   <scaleX type="value" value="1"/>
   <scaleY type="value" value="1"/>
   <shearX type="value" value="0"/>
   <shearY type="value" value="0"/>
   <keepAspectRatio type="value" value="0"/>
   <flattenedPerspectiveTransform m31="0" m33="1" m22="1" m23="0" type="transform" m12="0" m13="0" m21="0" m11="1" m32="0"/>
   <filterId type="value" value="Bicubic"/>
  </free_transform>
 </data>
</transform_params>
"""

class MyExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        # action = window.createAction("clone_selected_to_tilemap", "~Clone active node into Tilemap~")
        # action.triggered.connect(self.clone_selected_to_tilemap)
        action = window.createAction("generate_tilemap", "~Generate TileMap~")
        action.triggered.connect(self.generate_default_mask)

    def print_test(self):
        print("Hello world")

    def clone_selected_to_tilemap(self):
        doc = Krita.instance().activeDocument()
        root = doc.rootNode()
        node = doc.activeNode()
        bounds = node.bounds()

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

        for row in range(len(tile_locations)):
            for column in range(len(tile_locations)):
                if tile_locations[row][column] == 1:
                    clone = doc.createCloneLayer(f"{node.name()}_{row}_{column}", doc.activeNode())
                    offset_x = row * tile_w - bounds.x() 
                    offset_y = column * tile_h - bounds.y()
                    print(f"Row, column, offset_x, offset_y: {row}, {column}, {offset_x}, {offset_y}")
                    clone.move(offset_y, --offset_x)
                    root.addChildNode(clone, None)

    def generate_default_mask(self):
        # There are 5 different tiles, each 256x256 pixels. The final tilemap will be 1024x1024 pixels.
        # The tiles are named "mask_outer_corner", "mask_edge_connector", "mask_inner_corner", "mask_border", and "mask_fill".
        # The following tuple arrays contain the locations of each tile and the rotation (clockwise, 90 degrees per rotation) of each tile in the final tilemap.
        # The first number indicates how far to the right the tile is, the second number is how far down, and the third number is the rotation.
        outer_corner_locations = [(0, 0, 0), (0, 2, 180), (1, 3, 270), (3, 3, 90)]
        edge_connector_locations = [(0, 1, 0), (2, 3, 90)]
        inner_corner_locations = [(1, 1, 0), (2, 0, 90), (3, 1, 180), (2, 2, 270)]
        border_locations = [(1, 0, 0), (3, 0, 90), (1, 2, 270), (3, 2, 180)]
        mask_fill_locations = [(2, 1, 0)]

        doc = Krita.instance().activeDocument()
        group_layer = doc.createGroupLayer("clone_group")
        doc.rootNode().addChildNode(group_layer, None)

        mask_outer_corner = doc.nodeByName(f"mask_outer_corner")
        mask_edge_connector = doc.nodeByName(f"mask_edge_connector")
        mask_inner_corner = doc.nodeByName(f"mask_inner_corner")
        mask_border = doc.nodeByName(f"mask_border")
        mask_fill = doc.nodeByName(f"mask_fill")

        if any(node is None for node in [mask_outer_corner, mask_edge_connector, mask_inner_corner, mask_border, mask_fill]):
            print("One or more nodes not found. Please make sure all nodes are present in the document.")
            print("Required node names: mask_outer_corner, mask_edge_connector, mask_inner_corner, mask_border, mask_fill")
            return
        
        clones = []
        for loc in outer_corner_locations:
            clones.append(self.clone_move_rotate(mask_outer_corner, loc, group_layer))
        for loc in edge_connector_locations:
            clones.append(self.clone_move_rotate(mask_edge_connector, loc, group_layer))
        for loc in inner_corner_locations:
            clones.append(self.clone_move_rotate(mask_inner_corner, loc, group_layer))
        for loc in border_locations:
            clones.append(self.clone_move_rotate(mask_border, loc, group_layer))
        for loc in mask_fill_locations:
            clones.append(self.clone_move_rotate(mask_fill, loc, group_layer))

    def clone_move_rotate(self, node, loc, group_layer) -> Node:
        doc = Krita.instance().activeDocument()
        offset_x = loc[0] * 256 - node.bounds().x()
        offset_y = loc[1] * 256 - node.bounds().y()
        name = f"{node.name()}_{loc[0]}_{loc[1]}"
        clone = doc.createCloneLayer(name, node)
        clone.move(offset_x, offset_y)
        if loc[2] != 0:
            transform_mask = doc.createTransformMask(name + "_transform_mask")
            transform_mask.rotateNode(pi / 2 * loc[2])
            group_layer.addChildNode(clone, None)
            clone.addChildNode(transform_mask, None)
            template = MASK_TEMPLATE
            template = template.replace("X_VALUE", str(transform_mask.bounds().x() + transform_mask.bounds().width() / 2))
            template = template.replace("Y_VALUE", str(transform_mask.bounds().y() + transform_mask.bounds().height() / 2))
            template = template.replace("RADIANS", str(2 * pi * (loc[2] / 360)))
            success = transform_mask.fromXML(template)
            if success:
                print("Successfully applied rotation mask")
        else:
            
            group_layer.addChildNode(clone, None)
        return clone

# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(MyExtension(Krita.instance()))
