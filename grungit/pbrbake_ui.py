import bpy
from .grungit import Grungit
from .pbrbake import PBRBake
from .properties import GrungitProperties
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

class PBRBakePanel(Panel):
    bl_label = "PBR Bake"
    bl_idname = "OBJECT_PT_pbrbake_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Grungit"
    bl_context = "objectmode"   
    if bpy.app.version_string[:4:]=='2.80':
        bl_category = "Tool"
         #2.80 doesn't support custom categories
    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        Grungit.active_object = bpy.context.active_object
        Grungit.selected_objects = bpy.context.selected_objects

        layout = self.layout
        scene = context.scene
        pbrbake = scene.pbrbake
        active_object = Grungit.active_object
        selected_objects = Grungit.selected_objects


        if bpy.path.abspath("//")=="":
            layout.label(text="Salve o arquivo .blend primeiro")
        elif not hasattr(scene, "cycles"):
            layout.label(text="Cycles não disponível para bake")
        elif len(selected_objects) == 0:
            layout.label(text="Nenhum objeto selecionado")

        elif not any(obj.type=="MESH" for obj in selected_objects):
            layout.label(text="Selecione pelo menos uma malha")

        elif active_object.type=="MESH":
            layout.label(text="Resolution:")
            layout.prop(pbrbake, "resolution", text="") 
            layout.row()
            layout.label(text="Output Dir:")
            layout.prop(pbrbake, "output_dir", text="")
            layout.label(text="Baking samples:")
            layout.prop(pbrbake, "baking_samples", text="") 
            layout.label(text="Margin:")
            layout.prop(pbrbake, "baking_margin", text="") 
            layout.prop(pbrbake, "skip_unconnected")
            layout.label(text="Channels:")
            layout.prop(pbrbake, "bake_basecolor")
            layout.prop(pbrbake, "bake_metallic")
            layout.prop(pbrbake, "bake_specular")
            layout.prop(pbrbake, "bake_roughness")
            layout.prop(pbrbake, "bake_ao")
            layout.prop(pbrbake, "bake_normal")
            layout.prop(pbrbake, "bake_clearcoat")
            layout.prop(pbrbake, "bake_clearcoat_normal")
            layout.prop(pbrbake, "bake_grungit_mask")
            layout.prop(pbrbake, "bake_dirt_mask")
            layout.prop(pbrbake, "bake_alpha")
            #layout.row()
            #layout.prop(pbrbake, "uv_unwrap") 
            #layout.row()
            #col=layout.column()
            #col.enabled=False;

            layout.operator("object.pbrbake")