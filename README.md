# Krita TileMaps
Python plugin for Krita to help with creating &amp; editing tilemaps

![](https://github.com/lukethomas1/krita-tilemaps/blob/main/krita-tilemaps_demo.gif)


# Getting Started:
1. Add `tilemaptool.desktop` and the `tilemaptool/` folder to your `pykrita` folder (find your krita install path [here](https://docs.krita.org/en/reference_manual/resource_management.html#resource-management)).
2. Create a new document of at least 1024x1024 pixels, recommended ~1500x1500.
3. Import/create 5 layers. They should be named:
  - mask_outer_corner
  - mask_edge_connector
  - mask_inner_corner
  - mask_border
  - mask_fill
4. Before generating the tilemap, move the layers to the location you'd like them to be in while you edit. Once the clones are created, the clones will move with your source layers.
4. Go to Tools -> Scripts -> Generate TileMap.
5. Make changes to your original layers and watch them be reflected in the generated tilemap.
6. When you're done editing the tiles, you can merge the clone group into one layer and then export that layer as an image. I use it to create transparency masks that can be applied to other textures created in Krita.
  
