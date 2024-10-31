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
   <cameraPos z="CAMERA_SIZE" type="vector3d" x="0" y="0"/>
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

def generate_default_mask():
    doc = Krita.instance().activeDocument()
    
    # Determine tile size based on the first mask
    first_mask = doc.nodeByName("mask_outer_corner")
    if not first_mask:
        print("Error: mask_outer_corner not found. Make sure all mask layers are present.")
        return
    
    tile_width = first_mask.bounds().width()
    tile_height = first_mask.bounds().height()
    tilemap_width = tile_width * 4
    tilemap_height = tile_height * 4

    # Check if document is large enough
    if doc.width() < tilemap_width or doc.height() < tilemap_height:
        print(f"Error: Document size must be at least {tilemap_width}x{tilemap_height} pixels.")
        return

    group_layer = doc.createGroupLayer("clone_group")
    doc.rootNode().addChildNode(group_layer, None)

    # Define mask types and their corresponding locations
    mask_config = {
        "mask_outer_corner": [(0, 0, 0), (0, 2, 180), (1, 3, 270), (3, 3, 90)],
        "mask_edge_connector": [(0, 1, 0), (2, 3, 90)],
        "mask_inner_corner": [(1, 1, 0), (2, 0, 90), (3, 1, 180), (2, 2, 270)],
        "mask_border": [(1, 0, 0), (3, 0, 90), (1, 2, 270), (3, 2, 180)],
        "mask_fill": [(2, 1, 0)]
    }

    # Get all mask nodes
    mask_nodes = {name: doc.nodeByName(name) for name in mask_config.keys()}

    # Check if all nodes are present
    if None in mask_nodes.values():
        missing_nodes = [name for name, node in mask_nodes.items() if node is None]
        print(f"Nodes not found: {', '.join(missing_nodes)}")
        print("Please make sure all nodes are present in the document.")
        return

    # Clone, move, and rotate all masks
    for mask_name, locations in mask_config.items():
        for loc in locations:
            clone_move_rotate(mask_nodes[mask_name], loc, group_layer, tile_width, tile_height)

def clone_move_rotate(node, loc, group_layer, tile_width, tile_height) -> Node:
    doc = Krita.instance().activeDocument()
    
    # Calculate offset for the clone
    offset_x = loc[0] * tile_width - node.bounds().x()
    offset_y = loc[1] * tile_height - node.bounds().y()
    
    # Create a unique name for the clone
    name = f"{node.name()}_{loc[0]}_{loc[1]}"
    
    # Create and position the clone
    clone = doc.createCloneLayer(name, node)
    clone.move(offset_x, offset_y)
    
    # If rotation is needed
    if loc[2] != 0:
        # Create and apply transform mask
        transform_mask = doc.createTransformMask(name + "_transform_mask")
        transform_mask.rotateNode(pi / 2 * loc[2])
        
        # Add clone to group and mask to clone
        group_layer.addChildNode(clone, None)
        clone.addChildNode(transform_mask, None)
        
        # Prepare transform mask template
        template = MASK_TEMPLATE
        
        # Calculate center point of the transform mask
        center_x = transform_mask.bounds().x() + transform_mask.bounds().width() / 2
        center_y = transform_mask.bounds().y() + transform_mask.bounds().height() / 2
        
        # Replace placeholder values in the template
        template = template.replace("X_VALUE", str(center_x))
        template = template.replace("Y_VALUE", str(center_y))
        template = template.replace("RADIANS", str(2 * pi * (loc[2] / 360)))
        
        # Calculate and set camera size
        camera_size = max(transform_mask.bounds().width(), transform_mask.bounds().height())
        template = template.replace("CAMERA_SIZE", str(camera_size * 4))
        
        # Apply the transform mask
        success = transform_mask.fromXML(template)
    else:
        # If no rotation, simply add the clone to the group
        group_layer.addChildNode(clone, None)
    
    return clone

generate_default_mask()