import bpy
from bpy.props import (BoolProperty,
                       IntProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       PointerProperty
                       )
from bpy.types import PropertyGroup

class GrungitProperties(PropertyGroup):


    quality: EnumProperty(
        name="Quality:",
        description="Quality.",
        items=[ ("Medium", "Medium", "m"),
                ("High", "High", "h"),
                ("Very_High", "Very High", "vh"),
                ("Ultra", "Ultra", "u"),
               ],
        default = "Medium"
        )

    imperfections_amount_before = 0.0

    baker_only: BoolProperty(
        name="Baker only",
        description="Baker only(debug)",
        default = False
        )
    
    separate_uv_channel: BoolProperty(
        name="separate_uv_channel",
        description="separate_uv_channel",
        default = True
    )
    
    
    make_single_user: BoolProperty(
        name="Duplicate multi-user materials",
        description="Make all multi-user materials single-user",
        default = False
        )

    ignore_unused: BoolProperty(
        name="Ignore unused materials",
        description="Ignore unused materials",
        default = True
        )

    advanced_mode: BoolProperty(
        name="Advanced mode",
        description="Reveal non-essensial node sockets for advanced adjustment and fine-tuning",
        default = True
        )

    uv_unwrap: BoolProperty(
        name="(Re)create UV maps",
        description="Auto UV unwrap the mesh to save time.\nThis option will be ignored if the active object doesn't have a valid UV map, one will be created automatically.",
        default = True
        )

    uv_unwrap_separate: BoolProperty(
        name="Make new UV",
        description="Auto UV unwrap the mesh to save time.\nThis option will be ignored if the active object doesn't have a valid UV map, one will be created automatically.",
        default = False
        )

    quick_mode: BoolProperty(
        name="Quick mode (no edge wear)",
        description="Quick mode, useful if you don't need edge wear or you only need it to add imperfections",
        default = False
        )

    use_clearcoat: BoolProperty(
        name="Use clearcoat (slightly slower)",
        description='Use the "Clearcoat" and the "Clearcoat Normal" properties. Slightly slower to render, especially with EEVEE',
        default = False
        )
    
    overall_amount: FloatProperty(
        name="Overall amount",
        description="Amount of imperfections to add",
        default = 0.6,
        min = 0.0,
        max = 1.0
        )

    scale_factor: FloatProperty(
        name = "Edge wear scale",
        description="Edge wear scale",
        default = 2.0,
        min = 0.0,
        max = 10.0
        )
    

    
    grungit_type: EnumProperty(
        name="Nodes to use",
        description="Nodes to use",
        items=[ ("dirt", "dirt", ""),
                ("grungit", "grungit", ""),
                ("dirt_grungit", "dirt+grungit", ""),
               ],
        default = "dirt_grungit"
        )

    resolution: EnumProperty(
        name="Resolution:",
        description="Resolution.",
        items=[ ("256", "256x256", "256"),
                ("512", "512x512", "512"),
                ("1024", "1K", "1024"),
                ("2048", "2K", "2048"),
                ("4096", "4K", "4096"),
                ("8192", "8K", "8192"),
                ("16384", "16K", "16384"),
               ],
        default = "1024"
        )

    output_dir: StringProperty(
        name="Output Dir",
        description="Diretório de saída para o bake do Grungit (relativo ao .blend)",
        default="//Textures/Grungit/",
        subtype="DIR_PATH"
    )

class PBRBakeProperties(PropertyGroup):
    output_dir: StringProperty(
        name="Output Dir",
        description="Diretório de saída para os mapas (relativo ao .blend)",
        default="//Textures/",
        subtype="DIR_PATH"
    )
    skip_unconnected: BoolProperty(
        name="Skip unconnected sockets",
        description="Skip unconnected sockets",
        default = True
        )

    uv_unwrap: BoolProperty(
        name="(Re)create UV maps",
        description="Auto UV unwrap the mesh to save time.\nThis option will be ignored if the active object doesn't have a valid UV map, one will be created automatically.",
        default = False
        )

    bake_basecolor: BoolProperty(
        name="Base Color",
        description="",
        default = True
        )
    bake_specular: BoolProperty(
        name="Specular",
        description="",
        default = False
        )
    bake_metallic: BoolProperty(
        name="Metallic",
        description="",
        default = True
        )

    bake_roughness: BoolProperty(
        name="Roughness",
        description="",
        default = True
        )

    bake_ao: BoolProperty(
        name="Ambient Occlusion",
        description="",
        default = False
        )
    bake_alpha: BoolProperty(
        name="Alpha",
        description="",
        default = False
        )

    bake_normal: BoolProperty(
        name="Normal",
        description="",
        default = True
        )

    bake_clearcoat: BoolProperty(
        name="Clearcoat",
        description="",
        default = False
        )
    
    bake_clearcoat_normal: BoolProperty(
        name="Clearcoat Normal",
        description="",
        default = False
        )
    
    bake_grungit_mask: BoolProperty(
        name="Grunge Mask",
        description="",
        default = False
        )
    
    bake_dirt_mask: BoolProperty(
        name="Dirt Mask",
        description="",
        default = False
        )
    
    baking_samples: IntProperty(
        name="Samples",
        description="Number of samples used for baking",
        default = 16,
        min = 1,
        max = 128
        )
    baking_margin: IntProperty(
        name="Margin",
        description="Margin",
        default = 16,
        min = 1,
        max = 128
        )
        
    resolution: EnumProperty(
        name="Resolution:",
        description="Resolution.",
        items=[ ("256", "256x256", ""),
                ("512", "512x512", ""),
                ("1024", "1K", ""),
                ("2048", "2K", ""),
                ("4096", "4K", ""),
                ("8192", "8K", ""),
                ("16384", "16K", ""),
               ],
        default = "1024"
        )
