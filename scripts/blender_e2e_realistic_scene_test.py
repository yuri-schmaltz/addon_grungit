"""E2E bake com cena mais realista (multi-objeto, modifiers, múltiplos materiais)."""

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


def make_material(name: str, use_image=False):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
    out = next((n for n in nodes if n.type == "OUTPUT_MATERIAL"), None)
    if not bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    if not out:
        out = nodes.new("ShaderNodeOutputMaterial")
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    if use_image:
        img = bpy.data.images.new(name=f"{name}_img", width=256, height=256)
        img_node = nodes.new("ShaderNodeTexImage")
        img_node.image = img
        img_node.location = (-400, 200)
        links.new(img_node.outputs["Color"], bsdf.inputs["Base Color"])

    bsdf.inputs["Roughness"].default_value = 0.5
    return mat


def create_scene():
    # Cube with modifiers
    bpy.ops.mesh.primitive_cube_add(location=(0.0, 0.0, 0.0))
    cube = bpy.context.active_object
    cube.name = "RealisticCube"
    cube.modifiers.new("Bevel", "BEVEL").width = 0.02
    cube.modifiers.new("Subsurf", "SUBSURF").levels = 1

    # Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(location=(2.5, 0.0, 0.0))
    sphere = bpy.context.active_object
    sphere.name = "RealisticSphere"

    # Plane with two material slots
    bpy.ops.mesh.primitive_plane_add(location=(0.0, -2.5, 0.0))
    plane = bpy.context.active_object
    plane.name = "RealisticPlane"

    mat_a = make_material("RealisticMatA", use_image=True)
    mat_b = make_material("RealisticMatB", use_image=False)
    mat_shared = make_material("SharedMat", use_image=True)

    cube.data.materials.append(mat_shared)
    sphere.data.materials.append(mat_shared)

    plane.data.materials.append(mat_a)
    plane.data.materials.append(mat_b)

    bpy.ops.object.select_all(action="DESELECT")
    for obj in (cube, sphere, plane):
        obj.select_set(True)
    bpy.context.view_layer.objects.active = cube


def save_temp_blend():
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "e2e_realistic_scene.blend"
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
    create_scene()
    save_temp_blend()
    run_grungit_bake()
    outputs = find_bake_output()
    print(f"E2E realistic OK: {len(outputs)} arquivos")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"E2E realistic FAIL: {exc}")
        sys.exit(1)
