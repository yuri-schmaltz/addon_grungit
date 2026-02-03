bl_info = {
    "name": "Grungit",
    "description": "Grungit : 1-click wear and tear for Blender",
    "author": "Abdou Bouam",
    "version": (1, 9, 2),
    "blender": (5, 0, 0),
    "location": "3D View > Tools",
    "warning": "",
    "wiki_url": "",
    "category": "Material"
}


import bpy, os
from bpy.props import PointerProperty

from .grungit import Grungit, UpdateProps
from .properties import GrungitProperties, PBRBakeProperties
from .grungit_ui import GrungitPanel

from .pbrbake import PBRBake
from .pbrbake_ui import PBRBakePanel

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    Grungit,
    GrungitPanel,
    PBRBakePanel,
    GrungitProperties,
    PBRBakeProperties,
    UpdateProps,
    PBRBake
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.grungit = PointerProperty(type=GrungitProperties)
    bpy.types.Scene.pbrbake = PointerProperty(type=PBRBakeProperties)
    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    if hasattr(bpy.types.Scene, "grungit"):
        del bpy.types.Scene.grungit
    if hasattr(bpy.types.Scene, "pbrbake"):
        del bpy.types.Scene.pbrbake


if __name__ == "__main__":
    register()