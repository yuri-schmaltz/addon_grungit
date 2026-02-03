import bpy, os
from .grungit import Grungit, UpdateProps
from .properties import GrungitProperties
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

class GrungitPanel(Panel):
    bl_label = "Grungit"
    bl_idname = "OBJECT_PT_grungit_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Grungit"
    bl_context = "objectmode"   
    if bpy.app.version_string[:4:]=='2.80':
        bl_category = "Tool"
         #2.80 doesn't support custom categories

    scale_before = None
    overall_before = None
    simplified_mode_before = None

    
    @classmethod
    def poll(self,context):
        
        return context.object is not None


    def draw(self, context):
        Grungit.active_object = bpy.context.active_object
        Grungit.selected_objects = bpy.context.selected_objects
        selected_objects = Grungit.selected_objects
        #materials = Grungit.get_materials(self,context,selected_objects)
        layout = self.layout
        scene = context.scene
        grungit = scene.grungit
        active_object = Grungit.active_object
        selected_objects = Grungit.selected_objects
        dimensions = [0,0,0]
        

        # if grungit.overall_amount != GrungitPanel.overall_before:
        #     print("change triggered : "+ str(grungit.overall_amount))
        #     #bpy.ops.object.update_grungit_props()
                
        #         #if dirt_node:
        #         #    dirt_node.inputs["Overall Amount"].default_value = grungit.overall_amount
        #     GrungitPanel.overall_before = grungit.overall_amount


        if not os.path.exists(Grungit.grungit_data_path):
            layout.label(text="Arquivos de dados ausentes. Reinstale o Grungit.")
        elif not grungit.quick_mode and not hasattr(scene, "cycles"):
            layout.label(text="Cycles não disponível para bake")
        elif not grungit.quick_mode and bpy.path.abspath("//")=="":
            layout.label(text="Salve o arquivo .blend primeiro")
        elif len(selected_objects) == 0:
            layout.label(text="Nenhum objeto selecionado")

        elif not any(obj.type=="MESH" for obj in selected_objects):
            layout.label(text="Selecione pelo menos uma malha")

        elif active_object.type=="MESH":
            if grungit.grungit_type.find("grungit") >= 0 and Grungit.grungit_node not in bpy.data.node_groups:
                layout.label(text="NodeGroup Grungit ausente")
            if grungit.grungit_type.find("dirt") >= 0 and Grungit.dirt_node not in bpy.data.node_groups:
                layout.label(text="NodeGroup Dirt ausente")
            dimensions = active_object.dimensions
            if not grungit.quick_mode:
                layout.label(text="Resolution:")
                layout.prop(grungit, "resolution", text="") 
                layout.row()
                layout.label(text="Output Dir:")
                layout.prop(grungit, "output_dir", text="")
                layout.label(text="Quality:")
                layout.prop(grungit, "quality", text="") 
                layout.row()
                col=layout.column()
                col.enabled=False
                layout.prop(grungit, "scale_factor")
            
            layout.prop(grungit, "quick_mode")
            
            #else:
            layout.prop(grungit, "overall_amount")
            layout.operator(Grungit.bl_idname)
            layout.separator()
            if Grungit.debug:
                layout.label(text="Debug mode on")
                layout.prop(grungit, "baker_only")
                layout.label(text="scale :" + str((dimensions[0]+dimensions[1]+dimensions[2])/3/Grungit.scale_factor*bpy.context.scene.grungit.scale_factor))
            #layout.operator(UpdateProps.bl_idname)
        # elif active_object.type=="MESH" and active_object != selected_objects[0]:
        #     layout.label(text="Selected object is not active")
        else:
            layout.label(text="Invalid selection")
        
        