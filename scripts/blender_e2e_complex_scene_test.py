"""E2E bake com materiais mais complexos e multi-user data."""

# pyright: reportMissingImports=false

import sys
from pathlib import Path

import bpy  # type: ignore

ADDON_MODULE = "grungit"


def ensure_addon_enabled():
    prefs = bpy.context.preferences
    if ADDON_MODULE in prefs.addons:
        return

    try:
        bpy.ops.preferences.addon_enable(module=ADDON_MODULE)
    except Exception:
        pass

    if ADDON_MODULE in prefs.addons:
        return

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    try:
        module = __import__(ADDON_MODULE)
        if hasattr(module, "register"):
            module.register()
    except Exception as exc:
        raise RuntimeError(f"Falha ao habilitar o add-on Grungit: {exc}") from exc

    if ADDON_MODULE in prefs.addons:
        return
    if not hasattr(bpy.types.Scene, "grungit"):
        raise RuntimeError("Falha ao habilitar o add-on Grungit.")


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def build_complex_material(name: str):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf = None
    out = None
    for node in nodes:
        if node.type == "BSDF_PRINCIPLED":
            bsdf = node
        if node.type == "OUTPUT_MATERIAL":
            out = node
    if not bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    if not out:
        out = nodes.new("ShaderNodeOutputMaterial")
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-600, 200)
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-400, 200)
    bump = nodes.new("ShaderNodeBump")
    bump.location = (-200, 0)

    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Roughness"])
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    if "Clearcoat" in bsdf.inputs:
        bsdf.inputs["Clearcoat"].default_value = 0.4
    elif "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = 0.4

    if "Clearcoat Roughness" in bsdf.inputs:
        bsdf.inputs["Clearcoat Roughness"].default_value = 0.2
    elif "Coat Roughness" in bsdf.inputs:
        bsdf.inputs["Coat Roughness"].default_value = 0.2

    return mat


def create_objects():
    bpy.ops.mesh.primitive_cube_add()
    obj_a = bpy.context.active_object
    obj_a.name = "ComplexObjA"

    bpy.ops.object.duplicate(linked=True)
    obj_b = bpy.context.active_object
    obj_b.name = "ComplexObjB"
    obj_b.location.x = 2.5

    mat = build_complex_material("ComplexMat")
    obj_a.data.materials.append(mat)
    obj_b.data.materials.append(mat)

    bpy.ops.object.select_all(action="DESELECT")
    obj_a.select_set(True)
    obj_b.select_set(True)
    bpy.context.view_layer.objects.active = obj_a
    return [obj_a, obj_b]


def save_temp_blend():
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "e2e_complex_scene.blend"
    bpy.ops.wm.save_mainfile(filepath=str(blend_path))
    return blend_path


def run_grungit_bake():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.grungit.quick_mode = False
    scene.grungit.overall_amount = 0.5
    scene.grungit.output_dir = "//Textures/Grungit/"
    result = bpy.ops.object.grungit()
    if "FINISHED" not in result:
        raise RuntimeError(f"Grungit bake falhou: {result}")


def find_bake_output():
    output_dir = bpy.path.abspath("//Textures/Grungit/")
    output_path = Path(output_dir)
    if not output_path.exists():
        raise RuntimeError("Diretório de saída não foi criado.")
    exr_files = list(output_path.glob("*_Grungit.exr"))
    if len(exr_files) < 1:
        raise RuntimeError("Arquivo de bake não encontrado.")
    return exr_files


def main():
    ensure_addon_enabled()
    reset_scene()
    create_objects()
    save_temp_blend()
    run_grungit_bake()
    outputs = find_bake_output()
    print(f"E2E complex OK: {len(outputs)} arquivos")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"E2E complex FAIL: {exc}")
        sys.exit(1)
