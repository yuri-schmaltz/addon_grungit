import bpy, os
from bpy.props import (BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from .grungit import Grungit


class PBRBake(bpy.types.Operator):
    bl_idname = "object.pbrbake"
    bl_label = "PBR Bake"
    bl_description = "Bake PBR maps"
    bl_options = {'REGISTER', 'UNDO'}

    def validate_environment(self, context):
        if bpy.path.abspath("//") == "":
            self.report({'ERROR'}, "PBR Bake: salve o arquivo .blend antes de usar.")
            return False
        if not bpy.context.selected_objects:
            self.report({'WARNING'}, "PBR Bake: nenhum objeto selecionado.")
            return False
        if not any(obj and obj.type == "MESH" for obj in bpy.context.selected_objects):
            self.report({'WARNING'}, "PBR Bake: selecione pelo menos uma malha.")
            return False
        if not hasattr(context.scene, "cycles"):
            self.report({'ERROR'}, "PBR Bake: Cycles não disponível para bake.")
            return False
        return True

    def normalize_output_dir(self, context, raw_path, default="//Textures/"):
        path = raw_path.strip() if raw_path else default
        if len(path) == 0:
            path = default
        if not path.endswith("/"):
            path = path + "/"
        if path.startswith("//"):
            base_dir = bpy.path.abspath("//")
            abs_dir = bpy.path.abspath(path)
            if base_dir and abs_dir:
                try:
                    base_norm = os.path.normpath(base_dir)
                    abs_norm = os.path.normpath(abs_dir)
                    if os.path.commonpath([base_norm, abs_norm]) != base_norm:
                        self.report({'WARNING'}, "PBR Bake: caminho de saída inválido, usando padrão.")
                        return default
                except Exception:
                    return default
        return path
    
    def pbr_bake(self,context,materials,dir="Textures", create_subdirs = True, resolution = 2048, samples = 3, output_format="PNG", color_depth = 8):
        
        if len(dir)>0 and not dir.endswith("/"):
            dir = dir + "/"
        materials_filtered = []
        for material in materials:
            if material and material.name!="":
                if material not in materials_filtered:
                    materials_filtered.append(material)
        pbrbake = context.scene.pbrbake
        save_dir = PBRBake.normalize_output_dir(self, context, pbrbake.output_dir)
        samples = pbrbake.baking_samples
        resolution = int(pbrbake.resolution)
        

        #save render engine, samples, output format, bake settings 
        #don't forget use_pass_direct, use_pass_indirect, and use_pass_color
        image_settings = bpy.context.scene.render.image_settings
        scene = bpy.context.scene
        old_settings={
            "samples" : scene.cycles.samples,
            "engine" : scene.render.engine,
            "bake_type" : scene.cycles.bake_type,
            "bake_margin" : scene.render.bake.margin,
            "format" : image_settings.file_format,
            "color_mode" : image_settings.color_mode,
            "color_depth" : image_settings.color_depth,
            "view_transform" : bpy.context.scene.view_settings.view_transform

        }

        for material in materials_filtered:
            images=[]
            
            channels = []
            #channels = ["DIFFUSE_COLOR","AO","METALLIC","ROUGHNESS","NORMAL","CLEARCOAT","CLEARCOAT_NORMAL"]
            if pbrbake.bake_basecolor:
                channels.append("DIFFUSE_COLOR")
            if pbrbake.bake_metallic:
                channels.append("METALLIC")
            if pbrbake.bake_roughness:
                channels.append("ROUGHNESS")
            if pbrbake.bake_specular:
                channels.append("SPECULAR")
            if pbrbake.bake_clearcoat:
                channels.append("CLEARCOAT")
            if pbrbake.bake_normal:
                channels.append("NORMAL")
            if pbrbake.bake_clearcoat_normal:
                channels.append("CLEARCOAT_NORMAL")
            if pbrbake.bake_alpha:
                channels.append("ALPHA")
            if pbrbake.bake_ao:
                channels.append("AO")
            if pbrbake.bake_dirt_mask:
                channels.append("DIRT_MASK")
            if pbrbake.bake_grungit_mask:
                channels.append("GRUNGIT_MASK")
            material_name = material.name
            #sanitize name
            material_name = "".join(c for c in material_name if c.isalnum())
            for channel in channels:
                image = PBRBake.channel_bake(self,context,material, channel = channel, samples = samples, resolution = resolution, output_format=output_format , color_depth = color_depth, save_dir = save_dir, name = material_name)
                if image:
                    images.append(image)
            for image in images:
                print(image.name)
            PBRBake.reposition_nodes(self,context,material,images)

        #restore settings:
        scene.cycles.samples=old_settings["samples"]
        scene.render.engine=old_settings["engine"]
        scene.cycles.bake_type=old_settings["bake_type"]
        scene.render.bake.margin=old_settings["bake_margin"]
        image_settings.file_format=old_settings["format"]
        image_settings.color_mode=old_settings["color_mode"]
        image_settings.color_depth=old_settings["color_depth"]
        bpy.context.scene.view_settings.view_transform=old_settings["view_transform"]

    def channel_bake(self,context,material, channel = "DIFFUSE_COLOR", samples = 8, resolution = 2048, output_format="PNG", color_depth = 8, save_dir = "//Textures/", name = "out"):
        # DIFFUSE NORMAL ROUGHNESS EMIT AO

        # TODO : if input is an image, ignore it

        target_bake_type =	{
            "DIFFUSE_COLOR": "DIFFUSE",
            #"DIFFUSE_DIRECT": "DIFFUSE",
            #"DIFFUSE_INDIRECT":  "DIFFUSE", 
            "SPECULAR":"DIFFUSE",
            "METALLIC":"DIFFUSE",
            "NORMAL": "NORMAL",
            "ROUGHNESS": "DIFFUSE",
            "AO" : "AO",
            "CLEARCOAT" : "DIFFUSE",
            "CLEARCOAT_NORMAL" : "NORMAL",
            "ALPHA" : "DIFFUSE",
            "GRUNGIT_MASK" : "DIFFUSE",
            "DIRT_MASK" : "DIFFUSE"
        }
        channel_colorspace_name =	{
            "DIFFUSE_COLOR": "sRGB",
            #"DIFFUSE_DIRECT": "DIFFUSE",
            #"DIFFUSE_INDIRECT":  "DIFFUSE", 
            "SPECULAR":"Non-Color",
            "METALLIC":"Non-Color",#metallic not supported yet
            "NORMAL": "Non-Color",
            "ROUGHNESS": "Non-Color",
            "AO" : "Non-Color",
            "CLEARCOAT" : "Non-Color",
            "CLEARCOAT_NORMAL" : "Non-Color",
            "ALPHA" : "Non-Color",
            "GRUNGIT_MASK" : "Non-Color",
            "DIRT_MASK" : "Non-Color"
        }

        socket_name = {
            "DIFFUSE_COLOR": "Base Color",
            #"DIFFUSE_DIRECT": "DIFFUSE
            "SPECULAR":"Specular",
            "METALLIC":"Metallic",
            "NORMAL": "Normal",
            "ROUGHNESS": "Roughness",
            "AO" : None,
            "CLEARCOAT" : "Clearcoat",
            "CLEARCOAT_NORMAL" : "Clearcoat Normal",
            "ALPHA" : "Alpha",
            "GRUNGIT_MASK" : None,
            "DIRT_MASK" : None
        }
        output_suffix = {
            "DIFFUSE_COLOR": "basecolor",
            #"DIFFUSE_DIRECT": "DIFFUSE
            "SPECULAR":"specular",
            "METALLIC":"metallic",
            "ROUGHNESS": "roughness",
            "NORMAL": "normal",
            "AO" : "ao",
            "CLEARCOAT":"clearcoat",
            "CLEARCOAT_NORMAL":"clearcoat_normal",
            "ALPHA":"alpha",
            "GRUNGIT_MASK" : "grunge_mask",
            "DIRT_MASK" : "dirt_mask"
        }
        color_mode = {
            "DIFFUSE_COLOR": "RGB",
            #"DIFFUSE_DIRECT": "DIFFUSE
            "SPECULAR":"BW",
            "METALLIC":"BW",
            "ROUGHNESS": "BW",
            "NORMAL": "RGB",
            "AO" : "BW",
            "CLEARCOAT":"BW",
            "CLEARCOAT_NORMAL":"RGB",
            "ALPHA":"BW",
            "GRUNGIT_MASK" : "BW",
            "DIRT_MASK" : "BW"
        }
        #Get necessary nodes
        principled_BSDF_node = Grungit.get_BSDF_node(self,context,material)
        output_node = Grungit.get_output_node(self,context,material)
        if not principled_BSDF_node:
            print("No Principled BSDF node in "+material.name)
            return False
        if not output_node:
            print("No output node in "+material.name)
            return False
        
        tmp_bake_node = None


        material_name = material.name
            #sanitize name
        material_name = "".join(c for c in material_name if c.isalnum())
        
        image_name = material_name+"_"+output_suffix[channel]+"."+output_format.lower()
        bpy.ops.image.new(name=image_name, width=resolution, height=resolution, alpha=False)
        baker_image = bpy.data.images[image_name]
        
        scene = bpy.context.scene
        nodes = material.node_tree.nodes
        links = material.node_tree.links        
        bake_type = scene.cycles.bake_type
        
        pbrbake = context.scene.pbrbake

        bake_type = target_bake_type[channel]
        tmp_bake_node = nodes.new("ShaderNodeBsdfDiffuse")
        #if target_bake_type[channel] == "DIFFUSE":
        link_to_socket = None
        if not channel == "AO":
            for link in links:
                if link and link.to_node == principled_BSDF_node and link.to_socket.name == socket_name[channel]:
                    link_to_socket = link
                    break
            if link_to_socket:
                if target_bake_type[channel] == "DIFFUSE": #Everything else
                    links.new(link_to_socket.from_socket,tmp_bake_node.inputs["Color"])
                elif target_bake_type[channel] == "NORMAL": #Normal + Clearcoat Normal
                    links.new(link_to_socket.from_socket,tmp_bake_node.inputs["Normal"])
            else: #Unconnected socked
                node_found = False
                if channel=="GRUNGIT_MASK":
                    grungit_node = Grungit.get_grungit_node(self,context,material)
                    if grungit_node:
                        links.new(grungit_node.outputs["Mask"],tmp_bake_node.inputs["Color"])
                        node_found=True
                elif channel == "DIRT_MASK":
                    dirt_node = Grungit.get_dirt_node(self,context,material)
                    if dirt_node:
                        links.new(dirt_node.outputs["Mask"],tmp_bake_node.inputs["Color"])
                        node_found=True
                if pbrbake.skip_unconnected and not node_found:
                    if tmp_bake_node:
                        nodes.remove(tmp_bake_node)
                    return False
                if socket_name[channel]:
                    value = principled_BSDF_node.inputs[socket_name[channel]].default_value
                    if type(value) == float:
                        value = [value,value,value,1.0]
                    #tmp_bake_node.inputs["Color"].default_value = (value[0],value[1],value[2],value[3])
                    tmp_bake_node.inputs["Color"].default_value = (value[0],value[1],value[2],1.0)
            links.new(tmp_bake_node.outputs["BSDF"], output_node.inputs["Surface"])
        #Create image node
        baker_image_node = nodes.new("ShaderNodeTexImage")
        baker_image_node.image = baker_image
        nodes.active = baker_image_node

        #bake
        scene.render.engine = "CYCLES"
        scene.cycles.samples = samples
        scene.render.bake.margin = scene.pbrbake.baking_margin
        scene.cycles.bake_type = target_bake_type[channel]
        scene.view_settings.view_transform = 'Standard'

        if target_bake_type[channel] == "DIFFUSE":
            scene.render.bake.use_pass_indirect = False
            scene.render.bake.use_pass_direct = False
            scene.render.bake.use_pass_color = True
        baker_image.colorspace_settings.name = channel_colorspace_name[channel]
        baker_image.source = "GENERATED"
        baker_image.filepath = bpy.path.abspath(save_dir)+ image_name
        image_settings = bpy.context.scene.render.image_settings
        image_settings.color_mode = color_mode[channel]
        image_settings.color_depth = str(color_depth)
        image_settings.file_format = output_format
        
        use_selected_to_active_initial_state = False
        if context.scene.render.bake.use_selected_to_active:
            context.scene.render.bake.use_selected_to_active = False
            use_selected_to_active_initial_state = True

        bpy.ops.object.bake(type=target_bake_type[channel])

        context.scene.render.bake.use_selected_to_active = use_selected_to_active_initial_state
        
        #save
        if not os.path.exists(bpy.path.abspath(save_dir)):
            os.makedirs(bpy.path.abspath(save_dir))

        baker_image.save()

        baker_image.source = "FILE"
        baker_image.filepath = bpy.path.abspath(save_dir)+ image_name
        baker_image.colorspace_settings.name = channel_colorspace_name[channel]
        #Connect

        links.new(principled_BSDF_node.outputs["BSDF"],output_node.inputs["Surface"])
        
        if target_bake_type[channel] == "NORMAL":
            normal_map=nodes.new("ShaderNodeNormalMap")
            links.new(normal_map.outputs["Normal"],principled_BSDF_node.inputs[socket_name[channel]])
            links.new(baker_image_node.outputs["Color"],normal_map.inputs["Color"])
        elif socket_name[channel]: #Not AO, dirt or grunge mask texture and needs to be connected
            links.new(baker_image_node.outputs["Color"],principled_BSDF_node.inputs[socket_name[channel]])
        

        if tmp_bake_node:
            nodes.remove(tmp_bake_node)
        
        return baker_image_node
    
    def reposition_nodes(self,context,material,nodes):
        #TODO check if image is connected to "normal map" node and offset by two.
        bsdf_height = 630
        bsdf_node = Grungit.get_BSDF_node(self,context,material)
        bsdf_location = bsdf_node.location
        offset = 300
        total_height = len(nodes) * offset
        origin =  [bsdf_location[0] - offset, bsdf_location[1] + (total_height - bsdf_height)/2]
        for i, node in enumerate(nodes) :
            links = node.outputs["Color"].links 
            if len(links) and links[0].to_node.type == "NORMAL_MAP":
                node.location = [origin[0]-offset,origin[1] - offset * i]
                links[0].to_node.location = [origin[0],origin[1] - offset * i] #position normal map node
            else:
                node.location = [origin[0] - offset,origin[1] - offset * i]

    def execute(self,context):
        if not PBRBake.validate_environment(self, context):
            return {'CANCELLED'}
        Grungit.selected_objects = [obj for obj in bpy.context.selected_objects if obj and obj.type == "MESH"]
        if not Grungit.selected_objects:
            self.report({'WARNING'}, "PBR Bake: selecione pelo menos uma malha.")
            return {'CANCELLED'}
        materials = Grungit.get_materials(self,context, Grungit.selected_objects)
        if not materials:
            self.report({'WARNING'}, "PBR Bake: nenhum material válido encontrado.")
            return {'CANCELLED'}
        PBRBake.pbr_bake(self,context,materials)
        print("done!")
        return {'FINISHED'}


    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        ui_scale = bpy.context.preferences.view.ui_scale
        return context.window_manager.invoke_props_dialog(self, width = int(550 * ui_scale))

    def draw(self, context):
        layout=self.layout
        pbrbake = context.scene.pbrbake

        row = self.layout

        row.label(text="Experimental feature. Make sure you have saved your files first.")
