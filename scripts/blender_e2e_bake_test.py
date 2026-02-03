"""E2E bake headless para o Grungit (Cycles)."""

# pyright: reportMissingImports=false

import sys
from pathlib import Path

import bpy

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


def create_test_mesh():
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    mat = bpy.data.materials.new(name="BakeMat")
    mat.use_nodes = True
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
    return obj


def save_temp_blend():
    repo_root = Path(__file__).resolve().parents[1]
    tmp_dir = repo_root / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    blend_path = tmp_dir / "e2e_bake_test.blend"
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
    if not exr_files:
        raise RuntimeError("Arquivo de bake não encontrado.")
    return exr_files[0]


def main():
    ensure_addon_enabled()
    reset_scene()
    create_test_mesh()
    save_temp_blend()
    run_grungit_bake()
    output = find_bake_output()
    print(f"E2E bake OK: {output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"E2E bake FAIL: {exc}")
        sys.exit(1)
