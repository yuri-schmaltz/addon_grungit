import bpy, os

class UpdateProps(bpy.types.Operator):
    bl_idname = "object.update_grungit_props"
    bl_label = "update grungit props"
    bl_description = "update grungit props"
    bl_options = {'REGISTER'}
    def execute(self,context):
        #update prop
        selected_objects = bpy.context.selected_objects
        materials = Grungit.get_materials(self,context,selected_objects)
        grungit = bpy.context.scene.grungit
        for material in materials:
            node = Grungit.get_grungit_node(self,context,material)
            if node :
                node.inputs["Global Control"].default_value = grungit.overall_amount
            node = Grungit.get_dirt_node(self,context,material)
            if node : 
                node.inputs["Overall Amount"].default_value = grungit.overall_amount
        return {'FINISHED'}

class Grungit(bpy.types.Operator):
    bl_idname = "object.grungit"
    bl_label = "Apply Grungit"
    bl_description = "Generate Grunge"
    bl_options = {'REGISTER', 'UNDO'}

    active_object = None
    selected_objects: list = []
    UV_layer_name="Grungit"
    baker_node= "Baker v1.8.3"
    grungit_node = "Grungit v1.9.1"
    dirt_node = "Grungit Dirt v1.9.1"
    debug = False
    scale_factor = 2
    
    grungit_data_path = os.path.realpath(__file__)
    grungit_data_path = os.path.dirname(grungit_data_path)
    if grungit_data_path.endswith(".blend"): #Debug, running inside a blend file, not as an addon
        grungit_data_path = os.path.dirname(grungit_data_path)
        debug = True
    grungit_data_path = bpy.path.abspath(grungit_data_path + "/grungit_data/Materials.blend")

    def validate_environment(self, context):
        if not os.path.exists(Grungit.grungit_data_path):
            self.report({'ERROR'}, "Grungit: arquivos de dados ausentes. Reinstale o add-on.")
            return False
        if not context.scene.grungit.quick_mode and bpy.path.abspath("//") == "":
            self.report({'ERROR'}, "Grungit: salve o arquivo .blend antes de usar.")
            return False
        if not context.scene.grungit.quick_mode and not hasattr(context.scene, "cycles"):
            self.report({'ERROR'}, "Grungit: Cycles não disponível para bake.")
            return False
        return True
    
    def reload_images(self,context):
        images = bpy.data.images
        for image in images:
            try:
                image.reload()
            except Exception:
                pass

    def normalize_output_dir(self, context, raw_path, default="//Textures/Grungit/"):
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
                        self.report({'WARNING'}, "Grungit: caminho de saída inválido, usando padrão.")
                        return default
                except Exception:
                    return default
        return path

    def ensure_nodegroup(self, context, nodegroup_name):
        if nodegroup_name in bpy.data.node_groups:
            return True
        Grungit.append_nodetree(self, context, nodegroup_name)
        if nodegroup_name in bpy.data.node_groups:
            return True
        self.report({'ERROR'}, f"Grungit: NodeGroup ausente: {nodegroup_name}")
        return False
    
    def get_materials(self,context, objects, make_single_user = False, ignore_unused = True):
        materials = []
        for obj in objects:
            if not obj or obj.type != "MESH":
                continue
            bpy.context.view_layer.objects.active = obj
            active_object = bpy.context.active_object
            Grungit.debug and print("get materials")
            used_material_indices = None
            if ignore_unused:
                used_material_indices = {poly.material_index for poly in obj.data.polygons}
            for index, material_slot in enumerate(active_object.material_slots):
                if material_slot.name.startswith("."):
                    material_used = False
                elif ignore_unused:
                    material_used = index in used_material_indices
                else:
                    material_used = True
                if material_slot.material and material_slot.material.name!="": # make sure it's not an empty slot, before checking
                    if material_used and make_single_user and material_slot.material.users > 1 and not material_slot.name.startswith("."):
                        material_slot.material = material_slot.material.copy()
                        Grungit.debug and print("duplicated "+material_slot.material.name)

                    if material_used and material_slot.material not in materials and not material_slot.name.startswith("."):
                        Grungit.debug and print("appended "+material_slot.material.name)
                        materials.append(material_slot.material)
                    if not material_used:
                        Grungit.debug and print("found unused material : ",material_slot.material.name)
        if Grungit.debug :
            print("material list")
            for material in materials:
                print(material.name)
        return materials

    def merge_selected(self,context,objects):
        #TODO
        # Check for models with duplicated mesh data? unnecessary if duplicating
        # create empty temp objet
        # get selection
        # duplicate 1 model
        # apply all modifiers
        # join with temp model
        # repeat last 3 steps

        

        # return temp_bake_object
        pass

    def update_props(self,context):
        #update prop
        selected_objects = bpy.context.selected_objects
        materials = Grungit.get_materials(self,context,selected_objects)
        for material in materials:
            node = Grungit.get_grungit_node(self,context,material)
            if node :
                node.inputs["Global Control"].default_value = bpy.context.scene.grungit.overall_amount
            node = Grungit.get_dirt_node(self,context,material)
            if node : 
                node.inputs["Overall Amount"].default_value = bpy.context.scene.grungit.overall_amount
        pass
    
    def select_by_material(self,context,objects,material_name):
        prev_mode = bpy.context.mode
        if prev_mode != "EDIT":
            bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')


        for obj in objects:
            if not obj or obj.type != "MESH":
                continue
            bpy.context.view_layer.objects.active = obj
            active_object = bpy.context.active_object
            material_slots = active_object.material_slots
            for index, material in enumerate(material_slots):
                if material.name == material_name :
                    active_object.active_material_index = index
                    bpy.ops.object.material_slot_select()
        bpy.ops.object.mode_set(mode='OBJECT')
        if prev_mode != "OBJECT":
            try:
                bpy.ops.object.mode_set(mode=prev_mode)
            except Exception:
                pass
    
    def create_texture(self,context,name,resolution):
         #list of default color spaces in order
        bpy.ops.image.new(name=name, width=resolution, height=resolution)
        try:
            bpy.data.images[name].colorspace_settings.name="Non-Color"
        except TypeError:
            bpy.data.images[name].colorspace_settings.name="Utility - Linear - sRGB" # ACES
        
        Grungit.debug and print("created image texture : "+name+" at "+str(resolution))
        
    def add_UV(self,context,selected_objects,materials):
            texture_size = int(bpy.context.scene.grungit.resolution)
            margin_distance = 8
            angle_limit = 1.39626
            user_area_weight = 1
            grungit = context.scene.grungit
            prev_mode = bpy.context.mode
            for obj in [o for o in selected_objects if o and o.type == "MESH"]:
                has_grungit= False
                if grungit.separate_uv_channel and len(obj.data.uv_layers)>0:
                    # active_render = obj.data.uv_layers[0]
                    for layer in obj.data.uv_layers:
                        if layer.name == Grungit.UV_layer_name:
                            has_grungit = True
                            break
                        # if layer.active_render:
                        #     active_render = layer
                if len(obj.data.uv_layers)==0 or not has_grungit:
                    obj.data.uv_layers.new(name=Grungit.UV_layer_name)
                    #obj.data.uv_layers[UV_layer_name].active_render = True
                obj.data.uv_layers[Grungit.UV_layer_name].active = True
                #for layer in obj.data.uv_layers:
                #    if layer.active_render:
                #        layer.active = True
                #        break

            materials = Grungit.get_materials(self,context,selected_objects,ignore_unused = grungit.ignore_unused)

            for material in materials:
                Grungit.select_by_material(self,context,selected_objects,material.name)
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.reveal()
                bpy.ops.uv.smart_project(
                    angle_limit = angle_limit,
                    island_margin = margin_distance / texture_size,
                    area_weight = user_area_weight
                    )

                #Island margin does not seem to work properly. A bug in Blender?
                bpy.ops.uv.pack_islands(rotate = True, margin = margin_distance / texture_size)

            bpy.ops.object.mode_set(mode='OBJECT')
            if prev_mode != "OBJECT":
                try:
                    bpy.ops.object.mode_set(mode=prev_mode)
                except Exception:
                    pass

    def append_nodetree(self,context,name):
        grungit_data_path = Grungit.grungit_data_path+"/NodeTree" 
        #print("appending "+name+" from "+ Grungit.grungit_data_path)
        bpy.ops.wm.append(directory=grungit_data_path, link = False, filename=name)
        #print('appended "'+ name+'" Successfully')

        
    def get_output_node(self,context,material):
        nodes = material.node_tree.nodes
        for node in nodes:
            if node.type=="OUTPUT_MATERIAL":
                return node
        output_node = nodes.new("ShaderNodeOutputMaterial")
        return output_node
        
    def get_BSDF_node(self,context,material):
        nodes = material.node_tree.nodes
        for node in nodes:
            if node.type=="BSDF_PRINCIPLED":
                return node
        BSDF_node = nodes.new("ShaderNodeBsdfPrincipled")
        return BSDF_node
    
    def get_grungit_node(self,context,material):
        nodes = material.node_tree.nodes
        for node in nodes:
            if node.type=="GROUP" and node.node_tree.name == Grungit.grungit_node:
                return node
        return None

    def get_dirt_node(self,context,material):
        nodes = material.node_tree.nodes
        for node in nodes:
            if node.type=="GROUP" and node.node_tree.name == Grungit.dirt_node:
                return node
        return None

    def create_materials(self,context,objects):
        for obj in objects: 
            material_slots=obj.material_slots
            if len(material_slots) == 0:
                Grungit.debug and print("no material slots")
                new_material = bpy.data.materials.new(name=obj.name)
                obj.data.materials.append(new_material)
                new_material.use_nodes = True
                Grungit.debug and print("created and appended"+ new_material.name)
            else:
                for material in material_slots :
                    if not material.material: #empty slot
                        material = bpy.data.materials.new(name=obj.name)
                        material.use_nodes = True

    def prepare_bake(self,context,objects):
        #grungit_node = Grungit.grungit_node 
        baker_node_name = Grungit.baker_node
        grungit = context.scene.grungit
        #dirt_node = Grungit.dirt_node
        dimensions=[0.0,0.0,0.0]
        objects = [o for o in objects if o and o.type == "MESH"]
        if not objects:
            return
        if Grungit.debug :
            print("objects handed to prepare_bake are")
            for obj in objects:
                print(obj.name)
        
        for obj in objects:
            dimensions[0]=dimensions[0] + obj.dimensions[0]
            dimensions[1]=dimensions[1] + obj.dimensions[1]
            dimensions[2]=dimensions[2] + obj.dimensions[2]
        #loop
        dimensions[0] = dimensions[0]/len(objects)
        dimensions[1] = dimensions[1]/len(objects)
        dimensions[2] = dimensions[2]/len(objects)

        materials = Grungit.get_materials(self,context,objects,ignore_unused = grungit.ignore_unused)
        for material in materials:
            baker=None
            image_node = None
            if not material.use_nodes:
                material.use_nodes = True
                Grungit.restore_selection(self,context,objects)

            nodes = material.node_tree.nodes
            nodegroups = bpy.data.node_groups
            images=bpy.data.images
            material_name = material.name
            #sanitize name
            material_name = "".join(c for c in material_name if c.isalnum())
            grungit_image_name = material_name + "_Grungit"
            # grungit_image_resolution = int(bpy.context.scene.grungit.resolution[:-1:])*1024
            grungit_image_resolution = int(bpy.context.scene.grungit.resolution)
            baker = None 
            if not Grungit.ensure_nodegroup(self, context, baker_node_name):
                continue
            for node in nodes:
                if node.type=="GROUP" and node.node_tree.name ==baker_node_name:
                    baker=node
                    break
            if not baker:
                baker = nodes.new("ShaderNodeGroup")
                baker.node_tree=bpy.data.node_groups[baker_node_name]
                baker.name=baker_node_name
                baker.location[0]=-250

            nodes = material.node_tree.nodes
            #Add image
            if grungit_image_name not in images:
                Grungit.create_texture(self,context,grungit_image_name,grungit_image_resolution)
            else:
                #print("image "+grungit_image_name+" found")
                if images[grungit_image_name].size[0]==grungit_image_resolution:
                    #print("same resolution")
                    pass
                else:
                    #print("resolution changed")
                    images[grungit_image_name].source = "GENERATED"
                    images[grungit_image_name].generated_width=grungit_image_resolution
                    images[grungit_image_name].generated_height=grungit_image_resolution
                    try :
                        images[grungit_image_name].colorspace_settings.name="Non-Color"
                    except TypeError:
                        images[grungit_image_name].colorspace_settings.name="Utility - Linear - sRGB"
                    pass #set iamge source to generated, change resolution, set to linear 
            images = bpy.data.images
            for node in nodes:
                if node.type=="TEX_IMAGE" and node.image and node.image.name==grungit_image_name:
                    image_node = node
                    break

            principled_BSDF_node = Grungit.get_BSDF_node(self,context,material)
            
            if not image_node:
                image_node = nodes.new("ShaderNodeTexImage")
                image_node.image = images[grungit_image_name]
                if bpy.context.scene.grungit.uv_unwrap:
                    print("Grungit: UV map node created")
                    uv_node = nodes.new("ShaderNodeUVMap")
                    uv_node.uv_map = Grungit.UV_layer_name
                    material.node_tree.links.new(uv_node.outputs["UV"],image_node.inputs["Vector"])

            output_node=Grungit.get_output_node(self,context,material)
            nodes.active=image_node
            image_node.select = True
            image_node.location[0]=-600
            #output_node.location[0]=100 
            
            baker.inputs["Scale"].default_value=(dimensions[0]+dimensions[1]+dimensions[2])/3/Grungit.scale_factor*bpy.context.scene.grungit.scale_factor

            surface_input = output_node.inputs["Surface"]
            baker_output = baker.outputs["Output"]
            material.node_tree.links.new(baker_output,surface_input)

            if principled_BSDF_node and principled_BSDF_node.inputs['Normal'].is_linked:
                from_node = principled_BSDF_node.inputs['Normal'].links[0].from_node 
                if from_node == Grungit.get_dirt_node(self,context,material) :
                    #handle grungit already applied
                    grungit_node = Grungit.get_grungit_node(self,context,material)
                    if grungit_node and grungit_node.inputs['Normal'].is_linked:
                        normal = grungit_node.inputs['Normal'].links[0].from_socket
                        baker_normal_input = baker.inputs["Normal"]
                        material.node_tree.links.new(normal,baker_normal_input)
                    
                else :
                    normal = principled_BSDF_node.inputs['Normal'].links[0].from_socket
                    baker_normal_input = baker.inputs["Normal"]
                    material.node_tree.links.new(normal,baker_normal_input)

            ##return baker

    def simplify_nodes(self,context,material, simplify = True):
        dirt_node = Grungit.get_dirt_node(self,context,material)
        grungit_node = Grungit.get_grungit_node(self,context,material)
        grungit_sockets = [
            "Randomness Map Scale",
            "Scratch Map Scale",
            "Edge Wear Spread",
            "Additional Roughness",
            "Secondary Mask",
            "Transition Color",
            "Coat Weight",
            "Coat Normal",
            "Grunge Map Scale",
            "Cracks Map Scale",
            "Cracks Map Scale",
            "Occlusion",
            "Edge Wear Spread",
            "Transition Amount"
            ]
        dirt_sockets = [
            "AO",
            "Top",
            "Sides",
            "Top-down",
            "Bottom-up",
            "Dirt Texture",
            "Texture Stretching (sides)",
            "Bump Strength",
            "Secondary Mask",
            "Dirt Metallic",
            "Dirt Roughness"
            
        ]
        if grungit_node:
                for socket in grungit_sockets:
                    grungit_node.inputs[socket].hide = simplify

        if dirt_node:
            for socket in dirt_sockets:
                dirt_node.inputs[socket].hide = simplify

    def setup_grungit_nodetree(self,context,materials,quick = False):

        grungit_node_name = Grungit.grungit_node
        dirt_node_name = Grungit.dirt_node
        baker_node_name = Grungit.baker_node
        #--------Iterate through materials--------#
        for material in materials:
            if not material: #empty slot
                continue
            nodes = material.node_tree.nodes
            nodegroups = bpy.data.node_groups
            material_name = material.name
            #sanitize name
            material_name = "".join(c for c in material_name if c.isalnum())
            grungit_image_name = material_name + "_Grungit"
            #--------Nodes--------#
            output_node = Grungit.get_output_node(self,context,material)
            principled_BSDF_node = Grungit.get_BSDF_node(self,context,material)
            grungit_node = Grungit.get_grungit_node(self,context,material)
            dirt_node = Grungit.get_dirt_node(self,context,material)
            image_node = None
            uv_node = None        
            offset = 350
            grungit_mode = context.scene.grungit.grungit_type

            if "grungit" in grungit_mode:
                if not Grungit.ensure_nodegroup(self, context, grungit_node_name):
                    continue

            if "dirt" in grungit_mode:
                if not Grungit.ensure_nodegroup(self, context, dirt_node_name):
                    continue
            
            if not grungit_node and "grungit" in grungit_mode:

                grungit_node = nodes.new("ShaderNodeGroup")
                grungit_node.node_tree=bpy.data.node_groups[grungit_node_name]
                grungit_node.name=grungit_node_name
                grungit_node.width = 200
                grungit_node.location[0]=principled_BSDF_node.location[0]
                grungit_node.location[1]=principled_BSDF_node.location[1]
            
            if not dirt_node and "dirt" in grungit_mode:

                dirt_node = nodes.new("ShaderNodeGroup")
                dirt_node.node_tree=bpy.data.node_groups[dirt_node_name]
                dirt_node.name=dirt_node_name
                dirt_node.width = 200
                dirt_node.location[0]=principled_BSDF_node.location[0]+offset*1
                dirt_node.location[1]=principled_BSDF_node.location[1]


            
            if not quick:
                for node in nodes:
                    if node.type=="TEX_IMAGE" and node.image and node.image.name==grungit_image_name:
                        image_node = node
                    elif node.type=="UVMAP":
                        uv_node = node

            links = material.node_tree.links

            if not image_node and not quick:
                if grungit_image_name not in bpy.data.images:
                    grungit_image_resolution = int(bpy.context.scene.grungit.resolution)
                    Grungit.create_texture(self,context,grungit_image_name,grungit_image_resolution)
                image_node = nodes.new("ShaderNodeTexImage")
                image_node.image = bpy.data.images[grungit_image_name]
            
            if not uv_node and not quick and bpy.context.scene.grungit.uv_unwrap:
                print("Grungit: UV map node created")     
                uv_node = nodes.new("ShaderNodeUVMap")
                uv_node.uv_map = Grungit.UV_layer_name
                links.new(uv_node.outputs["UV"],image_node.inputs["Vector"])

            if not quick:
                grungit_image = bpy.data.images[grungit_image_name]
                try:
                    grungit_image.colorspace_settings.name="Non-Color"
                except TypeError:
                    grungit_image.colorspace_settings.name="Utility - Linear - sRGB"
            
            if grungit_node:
                location_node = grungit_node
            elif dirt_node:
                location_node = dirt_node
            else :
                location_node = principled_BSDF_node
            if image_node :
                image_node.location[0]=location_node.location[0]-offset
                image_node.location[1]=location_node.location[1]+offset
                if uv_node:
                    uv_node.location[0]=image_node.location[0] - offset
                    uv_node.location[1]=image_node.location[1]

            output_node.location[0]= principled_BSDF_node.location[0]+offset*3
            output_node.location[1]= principled_BSDF_node.location[1]
            if "dirt" in grungit_mode:
                principled_BSDF_node.location[0] = dirt_node.location[0] + offset
            else:
                principled_BSDF_node.location[0] = grungit_node.location[0] + offset
            

            #nodes : output_node principled_BSDF_node image_node dirt_node grungit_node 
            base_color=None
            normal=None
            metallic = None
            roughness = None
            clearcoat = None
            clearcoat_normal = None
            for link in links:
                if link.to_node == principled_BSDF_node and not link.from_node == dirt_node and not link.from_node == grungit_node :
                    if link.to_socket.name == "Base Color":
                        base_color = link.from_socket
                    elif link.to_socket.name == "Metallic":
                        metallic = link.from_socket
                    elif link.to_socket.name == "Roughness":
                        roughness = link.from_socket
                    elif link.to_socket.name == "Normal":
                        normal = link.from_socket
                    elif link.to_socket.name == "Coat Weight":
                        clearcoat = link.from_socket
                    elif link.to_socket.name == "Coat Normal":
                        clearcoat_normal = link.from_socket
                    
            
            links.new(principled_BSDF_node.outputs["BSDF"],output_node.inputs["Surface"])
            
            if not quick:
                if "grungit" in grungit_mode:
                    links.new(image_node.outputs["Color"],grungit_node.inputs["Grungit Mask"])
                if "dirt" in grungit_mode:
                    links.new(image_node.outputs["Color"],dirt_node.inputs["Grungit Mask"])
            
            if "dirt" in grungit_mode and "grungit" in grungit_mode:
                links.new(grungit_node.outputs["Base Color"],dirt_node.inputs["Base Color"])
                links.new(grungit_node.outputs["Metallic"],dirt_node.inputs["Metallic"])
                links.new(grungit_node.outputs["Roughness"],dirt_node.inputs["Roughness"])
                links.new(grungit_node.outputs["Normal"],dirt_node.inputs["Normal"])
                if context.scene.grungit.use_clearcoat:
                    links.new(grungit_node.outputs["Coat Weight"],dirt_node.inputs["Coat Weight"])
                    links.new(grungit_node.outputs["Coat Normal"],dirt_node.inputs["Coat Normal"])
            
            elif "grungit" in grungit_mode:
                links.new(grungit_node.outputs["Base Color"],principled_BSDF_node.inputs["Base Color"])
                links.new(grungit_node.outputs["Metallic"],principled_BSDF_node.inputs["Metallic"])
                links.new(grungit_node.outputs["Roughness"],principled_BSDF_node.inputs["Roughness"])
                links.new(grungit_node.outputs["Normal"],principled_BSDF_node.inputs["Normal"])
                if context.scene.grungit.use_clearcoat:
                    links.new(grungit_node.outputs["Coat Weight"],principled_BSDF_node.inputs["Coat Weight"])
                    links.new(grungit_node.outputs["Coat Normal"],principled_BSDF_node.inputs["Coat Normal"])
            
            if "dirt" in grungit_mode:
                links.new(dirt_node.outputs["Color"],principled_BSDF_node.inputs["Base Color"])
                links.new(dirt_node.outputs["Metallic"],principled_BSDF_node.inputs["Metallic"])
                links.new(dirt_node.outputs["Roughness"],principled_BSDF_node.inputs["Roughness"])
                links.new(dirt_node.outputs["Normal"],principled_BSDF_node.inputs["Normal"])
                if context.scene.grungit.use_clearcoat:
                    links.new(dirt_node.outputs["Coat Weight"],principled_BSDF_node.inputs["Coat Weight"])
                    links.new(dirt_node.outputs["Coat Normal"],principled_BSDF_node.inputs["Coat Normal"])
            
            # Default values, if the sockets are not connected
            overall_amount = bpy.context.scene.grungit.overall_amount
            
            if "grungit" in grungit_mode:
                grungit_node.inputs["Base Color 1"].default_value = principled_BSDF_node.inputs["Base Color"].default_value
                grungit_node.inputs["Roughness 1"].default_value = principled_BSDF_node.inputs["Roughness"].default_value
                grungit_node.inputs["Metallic 1"].default_value = principled_BSDF_node.inputs["Metallic"].default_value
                grungit_node.inputs["Coat Weight"].default_value = principled_BSDF_node.inputs["Coat Weight"].default_value
                grungit_node.inputs["Global Control"].default_value =  overall_amount
            
            if "dirt" in grungit_mode:
                dirt_node.inputs["Base Color"].default_value = principled_BSDF_node.inputs["Base Color"].default_value
                dirt_node.inputs["Roughness"].default_value = principled_BSDF_node.inputs["Roughness"].default_value
                dirt_node.inputs["Metallic"].default_value = principled_BSDF_node.inputs["Metallic"].default_value
                dirt_node.inputs["Coat Weight"].default_value = principled_BSDF_node.inputs["Coat Weight"].default_value
                dirt_node.inputs["Overall Amount"].default_value =  overall_amount
            
            
            
            if quick:
                if "dirt" in grungit_mode:
                    dirt_node.inputs["Bump Strength"].default_value = 0.1 
                    dirt_node.inputs["AO"].default_value = 0.1 
                    dirt_node.inputs["Contrast"].default_value = 0.2
                    dirt_node.inputs["Top"].default_value = 0.2 

                if "grungit" in grungit_mode:
                    grungit_node.inputs["Scratch Amount"].default_value = 0.3
                    grungit_node.inputs["Grunge Amount"].default_value = 0.25
                    grungit_node.inputs["Cracks Amount"].default_value = 0.1

                    grungit_node.inputs["Additional Roughness"].default_value =  overall_amount ** 0.5
                    grungit_node.inputs["Occlusion"].default_value = 0.0
                

            if base_color :
                if "grungit" in grungit_mode:
                    links.new(base_color,grungit_node.inputs["Base Color 1"])    
                else :
                    links.new(base_color,dirt_node.inputs["Base Color"])    
            if roughness :
                if "grungit" in grungit_mode:
                    links.new(roughness,grungit_node.inputs["Roughness 1"])
                else :
                    links.new(roughness,dirt_node.inputs["Roughness"])    

            if metallic :
                if "grungit" in grungit_mode:
                    links.new(metallic,grungit_node.inputs["Metallic 1"])
                else :
                    links.new(metallic,dirt_node.inputs["Metallic"])    

            if normal :
                if "grungit" in grungit_mode:
                    links.new(normal,grungit_node.inputs["Normal"])
                else :
                    links.new(normal,dirt_node.inputs["Normal"])    
            
            if context.scene.grungit.use_clearcoat:
                if clearcoat :
                    if "grungit" in grungit_mode:
                        links.new(clearcoat,grungit_node.inputs["Coat Weight"])
                    else :
                        links.new(clearcoat,dirt_node.inputs["Coat Weight"])    

                if clearcoat_normal :
                    if "grungit" in grungit_mode:
                        links.new(clearcoat_normal,grungit_node.inputs["Coat Normal"])
                    else :
                        links.new(clearcoat_normal,dirt_node.inputs["Coat Normal"])    
            
            if bpy.context.scene.grungit.advanced_mode :
                Grungit.simplify_nodes(self,context,material, simplify = False)
            else:
                Grungit.simplify_nodes(self,context,material, simplify = True)


            baker = None 
            for node in nodes:
                if node.type=="GROUP" and node.node_tree.name == baker_node_name:
                    baker=node

                    break
            ####
            #### Scale Unnecessary?
            if baker:
                material.node_tree.nodes.remove(baker)
            #     if grungit_node_created:
            #         grungit_node.inputs["Scratch Map Scale"].default_value=baker.inputs["Scale"].default_value
            #         grungit_node.inputs["Grunge Map Scale"].default_value=baker.inputs["Scale"].default_value
            #         grungit_node.inputs["Randomness Map Scale"].default_value=baker.inputs["Scale"].default_value
            #         grungit_node.inputs["Cracks Map Scale"].default_value=baker.inputs["Scale"].default_value
            #     if dirt_node_created:
            #         dirt_node.inputs["Dirt Texture Scale"].default_value=baker.inputs["Scale"].default_value
            #print("setup grungit nodetree")
 
    def bake(self,context,materials,selected_objects):
        if not selected_objects:
            return
        prev_mode = bpy.context.mode
        if prev_mode != "OBJECT":
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
            except Exception:
                pass
        use_selected_to_active_initial_state = False
        if context.scene.render.bake.use_selected_to_active:
            context.scene.render.bake.use_selected_to_active = False
            use_selected_to_active_initial_state = True
        
            
        active_object=bpy.context.active_object
        #materials=active_object.material_slots
        textures_path = Grungit.normalize_output_dir(self, context, context.scene.grungit.output_dir)
        Grungit.debug and print("restore selection in bake????")
        Grungit.restore_selection(self,context,selected_objects)

        Grungit.debug and print("baking")
        render_engine_before = bpy.context.scene.render.engine
        bpy.context.scene.render.engine = "CYCLES"
        baking_samples={"Medium":2,"High":4,"Very_High":8,"Ultra":16}[bpy.context.scene.grungit.quality]

        samples_before_bake = bpy.context.scene.cycles.samples
        margin_before_bake = bpy.context.scene.render.bake.margin

        bake_type_before = bpy.context.scene.cycles.bake_type
        bpy.context.scene.cycles.samples = baking_samples
        bpy.context.scene.cycles.bake_type = "EMIT"
        bpy.context.scene.render.bake.margin = 2
        
        #Object get deselected for some reason. Investigate!
        if active_object:
            bpy.context.view_layer.objects.active = active_object
            active_object.select_set(True)


        # temp_bake_object = Grungit.merge_selected(self,context,selected_objects)
        # Hide everything except temp_bake_object
        bpy.ops.object.bake(type='EMIT')
        Grungit.debug and print("bake invoke done")
        #save
        image_settings = bpy.context.scene.render.image_settings
        old_file_format = image_settings.file_format 
        old_color_mode = image_settings.color_mode 
        old_color_depth = image_settings.color_depth
        old_exr_codec = image_settings.exr_codec

        image_settings.file_format = "OPEN_EXR"
        image_settings.color_mode = "RGB"
        image_settings.color_depth = "16"
        #image_settings.exr_codec = "ZIP"
        image_settings.exr_codec = "DWAA"

        if not os.path.exists(bpy.path.abspath(textures_path)):
            os.makedirs(bpy.path.abspath(textures_path))
        
        for material in materials:
            material_name = material.name
            #sanitize name
            material_name = "".join(c for c in material_name if c.isalnum())
            grungit_image_name = material_name + "_Grungit"
            if grungit_image_name not in bpy.data.images:
                continue
            grungit_image = bpy.data.images[grungit_image_name] 
            grungit_image.save_render(bpy.path.abspath(textures_path)+ grungit_image_name+".exr")
            grungit_image.source = "FILE"
            grungit_image.filepath=bpy.path.abspath(textures_path)+ grungit_image_name+".exr"
            try:
                grungit_image.colorspace_settings.name="Non-Color"
            except TypeError:
                grungit_image.colorspace_settings.name="Utility - Linear - sRGB"
            
            
            
        image_settings.file_format = old_file_format
        if old_color_mode !="": #Bug. Probably with old 2.7x files?
            image_settings.color_mode = old_color_mode
        if old_color_depth !="":
            image_settings.color_depth = old_color_depth
        if old_exr_codec !="":
            image_settings.exr_codec = old_exr_codec
        
        bpy.context.scene.render.engine = render_engine_before
        bpy.context.scene.cycles.samples = samples_before_bake
        bpy.context.scene.cycles.bake_type = bake_type_before
        bpy.context.scene.render.bake.margin = margin_before_bake
        
        #restore selected_to_active state
        context.scene.render.bake.use_selected_to_active = use_selected_to_active_initial_state
        if prev_mode != "OBJECT":
            try:
                bpy.ops.object.mode_set(mode=prev_mode)
            except Exception:
                pass
        
    def restore_selection(self,context,selection):
        #TODO : deselect all first, when I figure out why objects are deselected
        for obj in selection:
            if not obj.select_get():
                print(obj.name + " was  not selected!!")
                obj.select_set(True)

    def execute(self,context):
        if not Grungit.validate_environment(self, context):
            return {'CANCELLED'}
        Grungit.active_object = bpy.context.active_object
        selected_objects = [obj for obj in bpy.context.selected_objects if obj and obj.type == "MESH"]
        if not selected_objects:
            self.report({'WARNING'}, "Grungit: selecione pelo menos uma malha.")
            return {'CANCELLED'}
        if not Grungit.active_object or Grungit.active_object.type != "MESH":
            bpy.context.view_layer.objects.active = selected_objects[0]
            Grungit.active_object = bpy.context.active_object
        # Validação: todos os objetos devem ter pelo menos um material
        for obj in selected_objects:
            if not getattr(obj.data, 'materials', None) or len(obj.data.materials) == 0:
                self.report({'WARNING'}, f"Grungit: o objeto '{obj.name}' não possui material. Adicione um material antes de aplicar o bake.")
                return {'CANCELLED'}
        Grungit.create_materials(self,context,selected_objects)
        make_single_user = context.scene.grungit.make_single_user
        ignore_unused = context.scene.grungit.ignore_unused
        
        materials = Grungit.get_materials(self,context,selected_objects, ignore_unused = ignore_unused)
        if not materials:
            self.report({'WARNING'}, "Grungit: nenhum material válido encontrado.")
            return {'CANCELLED'}
        
        if not bpy.context.scene.grungit.quick_mode:
            Grungit.restore_selection(self,context,selected_objects)
            materials = Grungit.get_materials(self,context,selected_objects, make_single_user = make_single_user, ignore_unused = ignore_unused)
            Grungit.restore_selection(self,context,selected_objects)
            for obj in selected_objects:
                if len(obj.data.uv_layers)==0:
                    Grungit.debug and print("object does not have UV's, ADD UV enabled")
                    bpy.context.scene.grungit.uv_unwrap=True
            if bpy.context.scene.grungit.uv_unwrap:
                Grungit.add_UV(self,context,selected_objects,materials)
            Grungit.restore_selection(self,context,selected_objects) #???
            Grungit.debug and print("prepare bake now")
            Grungit.prepare_bake(self,context,selected_objects)
            Grungit.restore_selection(self,context,selected_objects) #???
            Grungit.debug and print("bake now")
            if not Grungit.debug:
                Grungit.bake(self,context,materials,selected_objects)
                Grungit.restore_selection(self,context,selected_objects) #???
                #materials = Grungit.get_materials(self,context,selected_objects, make_single_user = make_single_user, ignore_unused = ignore_unused)
                Grungit.debug and print("setup grungit nodetree now")
                Grungit.setup_grungit_nodetree(self,context,materials)
        else:
            Grungit.setup_grungit_nodetree(self,context,materials,quick = True)
        Grungit.reload_images(self,context)
        Grungit.debug and print("done!")
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        ui_scale = bpy.context.preferences.view.ui_scale
        return context.window_manager.invoke_props_dialog(self, width = int(400 * ui_scale))

    def draw(self, context):
        grungit = context.scene.grungit
        layout = self.layout
        layout.prop(grungit, "make_single_user")
        layout.prop(grungit, "ignore_unused")
        layout.prop(grungit, "uv_unwrap")
        layout.prop(grungit, "advanced_mode")
        layout.prop(grungit, "use_clearcoat")
        layout.prop(grungit, "grungit_type")
        layout.label(text="Apply Grungit")
